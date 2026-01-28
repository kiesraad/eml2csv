# SPDX-FileCopyrightText: 2025-present Chris Mostert <15890652+chrismostert@users.noreply.github.com>
#
# SPDX-License-Identifier: EUPL-1.2
from typing import IO
from xml.etree.ElementTree import Element as XmlElement

from defusedxml import ElementTree

NAMESPACE = {
    "eml": "urn:oasis:names:tc:evs:schema:eml",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
    "kr": "http://www.kiesraad.nl/extensions",
    "xal": "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0",
    "xnl": "urn:oasis:names:tc:ciq:xsdschema:xNL:2.0",
}


def parse_xml(file_name: str | IO[bytes]) -> XmlElement | None:
    """Fetch the root node of an EML XML DOM-tree given a filepath.

    Args:
        file_name: Path to the EML file to parse.

    Returns:
        Root node of the EML file.
    """
    tree = ElementTree.parse(file_name)
    return tree.getroot()


def _get_text(xml_element: XmlElement | None) -> str | None:
    return xml_element.text if xml_element is not None else None


def _get_mandatory_text(xml_element: XmlElement | None) -> str:
    if xml_element is None:
        raise ValueError("Could not find specified XML element")

    text = xml_element.text
    if text is None:
        raise AttributeError(f"Element {xml_element} did not have text but was mandatory")

    return text


def _get_attrib(xml_element: XmlElement | None, attrib_name: str) -> str | None:
    return xml_element.attrib.get(attrib_name) if xml_element is not None else None


def _get_mandatory_attrib(xml_element: XmlElement | None, attrib_name: str) -> str:
    if xml_element is None:
        raise ValueError("Could not find specified XML element")

    attrib = xml_element.attrib.get(attrib_name)
    if attrib is None:
        raise AttributeError(f"Element {xml_element} did not have attribute {attrib_name} but was mandatory")

    return attrib
