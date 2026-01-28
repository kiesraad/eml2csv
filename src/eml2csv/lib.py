# SPDX-FileCopyrightText: 2025-present Chris Mostert <15890652+chrismostert@users.noreply.github.com>
#
# SPDX-License-Identifier: EUPL-1.2
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional
from xml.etree.ElementTree import Element as XmlElement

from eml2csv.util import NAMESPACE as ns
from eml2csv.util import (
    _get_attrib,
    _get_mandatory_attrib,
    _get_mandatory_text,
    _get_text,
    parse_xml,
)

SB_REGEX = re.compile("^((Stembureau )|(Briefstembureau ))+")
SB_ID_REGEX = re.compile(r"^\d+::SB")
ZIP_REGEX = re.compile(r" \(postcode: (\d{4} \w{2})\)")
NON_LETTERS_REGEX = re.compile(r"[^0-9a-zA-Z]")


class InvalidInputException(Exception):
    pass


def normalise(str_to_normalise: str) -> str:
    return NON_LETTERS_REGEX.sub("", str_to_normalise).lower()


@dataclass
class _Output:
    content: str
    buffer: List[str]

    def __init__(self):
        self.content = ""
        self.buffer = []

    def append(self, li: List[str]):
        self.buffer += li

    def flush(self):
        for idx, elem in enumerate(self.buffer):
            elem = elem.replace('"', '""')
            self.content += f'"{elem}"' if elem != "" else ""
            if idx != len(self.buffer) - 1:
                self.content += ";"
        self.buffer = []
        self.content += "\n"

    def push(self, li: List[str]):
        self.append(li)
        self.flush()

    def write_to_file(self, filename: str):
        with open(filename, "w", encoding="utf-8-sig") as out:
            out.write(self.content[:-1])


@dataclass(frozen=True)
class _AffiliationIdentifier:
    id: str
    name: str


@dataclass(frozen=True)
class _CandidateIdentifier:
    id: str
    name: str


def eml2csv(
    counts_eml_path: str, candidates_eml_path: str, output_csv_path: Optional[str]
):
    ## Init output
    output = _Output()

    ## Read in file
    counts_eml = parse_xml(counts_eml_path)
    candidates_eml = parse_xml(candidates_eml_path)

    # Check if parsing succeeded
    if counts_eml is None:
        raise InvalidInputException(f"Could not parse {counts_eml_path}")
    if candidates_eml is None:
        raise InvalidInputException(f"Could not parse {candidates_eml_path}")

    # Check if the supplied files match and are the expected EML id
    counts_id = _get_attrib(counts_eml, "Id")
    candidates_id = _get_attrib(candidates_eml, "Id")
    if counts_id != "510b" or counts_eml.tag != f"{{{ns['eml']}}}EML":
        raise InvalidInputException(
            f"{counts_eml_path} was not an EML counts file (510b)!"
        )
    if candidates_id != "230b" or candidates_eml.tag != f"{{{ns['eml']}}}EML":
        raise InvalidInputException(
            f"{candidates_eml_path} was not an EML candidates file (230b)!"
        )

    # Check if election id and contest id match
    counts_election_id = _get_attrib(
        counts_eml.find(".//eml:ElectionIdentifier", namespaces=ns), "Id"
    )
    candidates_election_id = _get_attrib(
        candidates_eml.find(".//eml:ElectionIdentifier", namespaces=ns), "Id"
    )
    if (
        counts_election_id is None
        or candidates_election_id is None
        or counts_election_id != candidates_election_id
    ):
        raise InvalidInputException(
            f"Election ids did not match! Counts file was {counts_election_id} while candidates file was {candidates_election_id}"
        )

    counts_contest_id = _get_attrib(
        counts_eml.find(".//eml:ContestIdentifier", namespaces=ns), "Id"
    )
    candidates_contest_id = _get_attrib(
        candidates_eml.find(".//eml:ContestIdentifier", namespaces=ns), "Id"
    )
    if (
        counts_contest_id is None
        or candidates_contest_id is None
        or counts_contest_id != candidates_contest_id
    ):
        raise InvalidInputException(
            f"Contest ids did not match! Counts file was {counts_contest_id} while candidates file was {candidates_contest_id}"
        )

    ## HEADER
    output.push(
        [
            "Verkiezing",
            "",
            _get_mandatory_text(counts_eml.find(".//eml:ElectionName", namespaces=ns)),
        ]
    )

    output.push(
        [
            "Datum",
            "",
            _get_mandatory_text(counts_eml.find(".//kr:ElectionDate", namespaces=ns)),
        ]
    )

    authority_name = _get_mandatory_text(
        counts_eml.find(".//eml:AuthorityIdentifier", namespaces=ns)
    )
    authority_type = (
        "Openbaar lichaam"
        if authority_name in ["Bonaire", "Saba", "Sint Eustatius"]
        else "Gemeente"
    )
    output.push(
        [
            "Gebied",
            "",
            f"{authority_type} {authority_name}",
        ]
    )

    authority_id = _get_mandatory_attrib(
        counts_eml.find(".//eml:AuthorityIdentifier", namespaces=ns), "Id"
    )
    output.push(
        [
            "Nummer",
            "",
            authority_id,
        ]
    )
    output.flush()

    ## REPORTING UNIT INFO
    reporting_units = counts_eml.findall(
        ".//eml:ReportingUnitIdentifier", namespaces=ns
    )
    reporting_unit_names = list(_get_mandatory_text(elem) for elem in reporting_units)
    reporting_unit_ids = list(
        _extract_reporting_unit_id(_get_mandatory_attrib(elem, "Id"))
        for elem in reporting_units
    )
    reporting_unit_zips = list(
        _extract_zip_from_name(name) for name in reporting_unit_names
    )

    # Main header with polling stations and zip codes
    output.push(
        ["Lijstnummer", "Aanduiding", "Volgnummer", "Naam kandidaat", "Totaal"]
        + list(_clean_name(name) for name in reporting_unit_names)
    )
    output.push(["Gebiednummer", "", "", "", ""] + reporting_unit_ids)
    output.push(["Postcode", "", "", "", ""] + reporting_unit_zips)

    ## METADATA INFO
    output.push(_generate_metadata_row(counts_eml, "opgeroepenen", ".//eml:Cast"))
    output.push(
        _generate_metadata_row(
            counts_eml,
            "geldige stempas",
            ".//eml:UncountedVotes[@ReasonCode = 'geldige stempassen']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "geldig volmachtbewijs",
            ".//eml:UncountedVotes[@ReasonCode = 'geldige volmachtbewijzen']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "geldige kiezerspas",
            ".//eml:UncountedVotes[@ReasonCode = 'geldige kiezerspassen']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "toegelaten kiezers",
            ".//eml:UncountedVotes[@ReasonCode = 'toegelaten kiezers']",
        )
    )
    geldig = _generate_metadata_row(
        counts_eml,
        "geldige stembiljetten",
        ".//eml:TotalCounted",
    )
    output.push(geldig)

    blanco = _generate_metadata_row(
        counts_eml,
        "blanco stembiljetten",
        ".//eml:RejectedVotes[@ReasonCode = 'blanco']",
    )
    output.push(blanco)

    ongeldig = _generate_metadata_row(
        counts_eml,
        "ongeldige stembiljetten",
        ".//eml:RejectedVotes[@ReasonCode = 'ongeldig']",
    )
    output.push(ongeldig)

    # Calculate total votes
    aangetroffen = ["", "aangetroffen stembiljetten", "", ""] + [
        str(int(geldig) + int(ongeldig) + int(blanco))
        for (geldig, ongeldig, blanco) in zip(
            geldig[4:], ongeldig[4:], blanco[4:], strict=True
        )
    ]
    output.push(aangetroffen)

    output.push(
        _generate_metadata_row(
            counts_eml,
            "meer stembiljetten dan toegelaten kiezers",
            ".//eml:UncountedVotes[@ReasonCode = 'meer getelde stembiljetten']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "minder stembiljetten dan toegelaten kiezers",
            ".//eml:UncountedVotes[@ReasonCode = 'minder getelde stembiljetten']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "kiezers met stembiljet hebben niet gestemd",
            ".//eml:UncountedVotes[@ReasonCode = 'meegenomen stembiljetten']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "er zijn te weinig stembiljetten uitgereikt",
            ".//eml:UncountedVotes[@ReasonCode = 'te weinig uitgereikte stembiljetten']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "er zijn te veel stembiljetten uitgereikt",
            ".//eml:UncountedVotes[@ReasonCode = 'te veel uitgereikte stembiljetten']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "geen verklaring",
            ".//eml:UncountedVotes[@ReasonCode = 'geen verklaring']",
        )
    )
    output.push(
        _generate_metadata_row(
            counts_eml,
            "andere verklaring",
            ".//eml:UncountedVotes[@ReasonCode = 'andere verklaring']",
        )
    )

    ## CANDIDATE INFO
    candidate_info = _get_candidate_info(candidates_eml)
    votes = _get_votecount_matrix(counts_eml)

    for affiliation in candidate_info.keys():
        # Push affiliation total votes
        output.push(
            [affiliation.id, affiliation.name, "", ""] + votes[(affiliation.id, None)]
        )
        # Push candidate votes
        for candidate in candidate_info[affiliation]:
            output.push(
                ["", "", candidate.id, candidate.name]
                + votes[(affiliation.id, candidate.id)]
            )

    # If no output file name is specified, construct one automatically
    if output_csv_path is None:
        # Normalise the election id and take the first six characters.
        # This is because for example for GR elections the ID is GR2080_Juinen
        # and we add the authorityname already.
        election_id = normalise(
            _get_mandatory_attrib(
                counts_eml.find(".//eml:ElectionIdentifier", namespaces=ns), "Id"
            )
        )[:6]
        output_csv_path = f"osv4-3_telling_{election_id}_{authority_type.lower().replace(' ', '_')}_{normalise(authority_name)}.csv"

    output.write_to_file(output_csv_path)


def _generate_metadata_row(eml: XmlElement, name: str, eml_elem: str) -> list[str]:
    return ["", name, "", ""] + list(
        _get_mandatory_text(elem) for elem in eml.findall(eml_elem, namespaces=ns)
    )


def _extract_zip_from_name(reporting_unit_name: Optional[str]) -> str:
    if reporting_unit_name is None:
        return ""
    search_result = re.search(ZIP_REGEX, reporting_unit_name)
    if search_result is None:
        return ""
    search_groups = search_result.groups()
    if len(search_groups) != 1:
        return ""
    return search_groups[0]


def _clean_name(reporting_unit_name: Optional[str]) -> str:
    return (
        re.sub(ZIP_REGEX, "", re.sub(SB_REGEX, "", reporting_unit_name))
        if reporting_unit_name is not None
        else ""
    )


def _extract_reporting_unit_id(reporting_unit_id: str) -> str:
    return re.sub(SB_ID_REGEX, "", reporting_unit_id)


def _get_candidate_info(candidates_eml: XmlElement):
    candidate_info = defaultdict(list)
    for aff in candidates_eml.findall(".//eml:Affiliation", namespaces=ns):
        aff_id = aff.find("./eml:AffiliationIdentifier", namespaces=ns)
        if aff_id is None:
            raise Exception("Affiliation without identifier in candidate list!")
        id = _get_mandatory_attrib(aff_id, "Id")
        name = _get_mandatory_text(aff_id.find("./eml:RegisteredName", namespaces=ns))
        aff_key = _AffiliationIdentifier(id, name)

        for cand in aff.findall("./eml:Candidate", namespaces=ns):
            cand_id = _get_mandatory_attrib(
                cand.find("./eml:CandidateIdentifier", namespaces=ns), "Id"
            )
            cand_initials = _get_mandatory_text(
                cand.find(".//xnl:NameLine[@NameType = 'Initials']", namespaces=ns)
            )
            cand_prefix = _get_text(cand.find(".//xnl:NamePrefix", namespaces=ns))
            cand_lastname = _get_mandatory_text(
                cand.find(".//xnl:LastName", namespaces=ns)
            )

            cand_name = (
                (f"{cand_prefix} " if cand_prefix is not None else "")
                + cand_lastname
                + f", {cand_initials}"
            )

            candidate_info[aff_key].append(
                _CandidateIdentifier(id=cand_id, name=cand_name)
            )
    return candidate_info


def _get_votecount_matrix(counts_eml: XmlElement):
    votes: defaultdict = defaultdict(list)
    _votecount_matrix(counts_eml, votes, reporting_units=False)
    _votecount_matrix(counts_eml, votes, reporting_units=True)
    return votes


def _votecount_matrix(
    counts_eml: XmlElement,
    votes,
    reporting_units: bool,
):
    affid_cur = None
    candid_cur = None

    for selection in counts_eml.findall(
        f".//eml:{'TotalVotes' if not reporting_units else 'ReportingUnitVotes'}/eml:Selection",
        namespaces=ns,
    ):
        affid = selection.find("./eml:AffiliationIdentifier", namespaces=ns)
        if affid is not None:
            affid_cur = _get_mandatory_attrib(affid, "Id")
            candid_cur = None
        else:
            candid_cur = _get_mandatory_attrib(
                selection.find(".//eml:CandidateIdentifier", namespaces=ns), "Id"
            )
        votes[(affid_cur, candid_cur)].append(
            _get_mandatory_text(selection.find("./eml:ValidVotes", namespaces=ns))
        )
