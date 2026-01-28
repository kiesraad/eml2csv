import os
from pathlib import Path

import pytest

from eml2csv import eml2csv
from eml2csv.lib import InvalidInputError

tests_path = Path("tests")


def test_tk25_output_csv_matches_oracle_file(tmp_path):
    output_csv = "osv4-3_telling_tk2025_gemeente_westmaasenwaal.csv"
    eml2csv(
        counts_eml_path="tests/Telling_TK2025_gemeente_West_Maas_en_Waal.eml.xml",
        candidates_eml_path="tests/Kandidatenlijsten_TK2025_Nijmegen.eml.xml",
        output_csv_path=str(tmp_path / output_csv),
    )

    with open(tmp_path / output_csv) as actual, open(tests_path / output_csv) as expected:
        assert actual.readlines() == expected.readlines(), f"Output file differences: {tmp_path / output_csv}"


def test_gr22_output_csv_matches_oracle_file(tmp_path):
    output_csv = "osv4-3_telling_gr2022_gemeente_westmaasenwaal.csv"
    eml2csv(
        counts_eml_path="tests/Telling_GR2022_WestMaasenWaal.eml.xml",
        candidates_eml_path="tests/Kandidatenlijsten_GR2022_WestMaasenWaal.eml.xml",
        output_csv_path=str(tmp_path / output_csv),
    )

    with open(tmp_path / output_csv) as actual, open(tests_path / output_csv) as expected:
        assert actual.readlines() == expected.readlines(), f"Output file differences: {tmp_path / output_csv}"


@pytest.fixture
def change_to_tmp_path(tmp_path):
    # Output csv is written to current directory,
    # so we have to change the current directory to the temp directory
    # while still having a valid path to our input files.
    cwd = Path.cwd()
    os.chdir(tmp_path)
    yield cwd, tmp_path
    os.chdir(cwd)


@pytest.mark.parametrize(("output_filename", "counts_eml_filename", "candidates_eml_filename"),
[
    ("osv4-3_telling_tk2025_gemeente_westmaasenwaal.csv", "Telling_TK2025_gemeente_West_Maas_en_Waal.eml.xml", "Kandidatenlijsten_TK2025_Nijmegen.eml.xml" ),
    ("osv4-3_telling_gr2022_gemeente_westmaasenwaal.csv", "Telling_GR2022_WestMaasenWaal.eml.xml", "Kandidatenlijsten_GR2022_WestMaasenWaal.eml.xml" ),
], ids= ["tk25", "gr22"])
def test_output_csv_file_generated(change_to_tmp_path, output_filename, counts_eml_filename, candidates_eml_filename):
    output_csv = output_filename
    old_path, new_path = change_to_tmp_path

    assert os.listdir(new_path) == []

    eml2csv(
        counts_eml_path=str(
            old_path / "tests" / counts_eml_filename
        ),
        candidates_eml_path=str(
            old_path / "tests" / candidates_eml_filename
        ),
        output_csv_path=None,
    )

    assert os.listdir(new_path) == [output_csv]

    with open(new_path / output_csv) as actual, open(old_path / "tests" / output_csv) as expected:
        assert actual.readlines() == expected.readlines(), f"Output file differences: {new_path / output_csv}"


def test_counts_file_is_not_an_eml_510b():
    with pytest.raises(
        InvalidInputError, match=r"was not an EML counts file \(510b\)"
    ):
        eml2csv(
            counts_eml_path="tests/Kandidatenlijsten_TK2025_Nijmegen.eml.xml",
            candidates_eml_path="tests/Kandidatenlijsten_TK2025_Nijmegen.eml.xml",
            output_csv_path=None,
        )


def test_candidates_file_is_not_an_eml_230b():
    with pytest.raises(
        InvalidInputError, match=r"was not an EML candidates file \(230b\)"
    ):
        eml2csv(
            counts_eml_path="tests/Telling_TK2025_gemeente_West_Maas_en_Waal.eml.xml",
            candidates_eml_path="tests/Telling_TK2025_gemeente_West_Maas_en_Waal.eml.xml",
            output_csv_path=None,
        )


def test_contest_ids_do_not_match():
    with pytest.raises(
        InvalidInputError,
        match=r"Contest ids did not match! Counts file was 6 while candidates file was 10",
    ):
        eml2csv(
            counts_eml_path="tests/Telling_TK2025_gemeente_West_Maas_en_Waal.eml.xml",
            candidates_eml_path="tests/Kandidatenlijsten_TK2025_Haarlem.eml.xml",
            output_csv_path=None,
        )


def test_election_ids_do_not_match():
    with pytest.raises(
        InvalidInputError,
        match=r"Election ids did not match! Counts file was TK2025 while candidates file was GR2022_WestMaasenWaal",
    ):
        eml2csv(
            counts_eml_path="tests/Telling_TK2025_gemeente_West_Maas_en_Waal.eml.xml",
            candidates_eml_path="tests/Kandidatenlijsten_GR2022_WestMaasenWaal.eml.xml",
            output_csv_path=None,
        )
