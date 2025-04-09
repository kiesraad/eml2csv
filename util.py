from typing import IO, Optional, Union
from xml.etree.ElementTree import Element as XmlElement

from defusedxml import ElementTree as ET

NAMESPACE = {
    "eml": "urn:oasis:names:tc:evs:schema:eml",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
    "kr": "http://www.kiesraad.nl/extensions",
    "xal": "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0",
    "xnl": "urn:oasis:names:tc:ciq:xsdschema:xNL:2.0",
}


def parse_xml(file_name: Union[str, IO[bytes]]) -> Optional[XmlElement]:
    """Fetch the root node of an EML XML DOM-tree given a filepath.

    Args:
        file_name: Path to the EML file to parse.

    Returns:
        Root node of the EML file.
    """
    tree = ET.parse(file_name)
    tree_root = tree.getroot()

    return tree_root


def get_eml_type(root: XmlElement) -> Optional[str]:
    """Fetches the EML ID.

    Args:
        root: The root node to query.

    Returns:
        The ID of the EML file (e.g. `"510b"` for municipality counts).
    """
    root_element = root.find(".")
    if root_element and root_element.tag == f"{{{NAMESPACE.get('eml')}}}EML":
        return _get_attrib(root_element, "Id")

    return None


def _get_text(xml_element: Optional[XmlElement]) -> Optional[str]:
    return xml_element.text if xml_element is not None else None


def _get_mandatory_text(xml_element: Optional[XmlElement]) -> str:
    if xml_element is None:
        raise ValueError("Could not find specified XML element")

    text = xml_element.text
    if text is None:
        raise AttributeError(
            f"Element {xml_element} did not have text but was mandatory"
        )

    return text


def _get_attrib(xml_element: Optional[XmlElement], attrib_name: str) -> Optional[str]:
    return xml_element.attrib.get(attrib_name) if xml_element is not None else None


def _get_mandatory_attrib(xml_element: Optional[XmlElement], attrib_name: str) -> str:
    if xml_element is None:
        raise ValueError("Could not find specified XML element")

    attrib = xml_element.attrib.get(attrib_name)
    if attrib is None:
        raise AttributeError(
            f"Element {xml_element} did not have attribute {attrib_name} but was mandatory"
        )

    return attrib
