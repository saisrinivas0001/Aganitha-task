import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from .models import Paper, Author 

# Global debug flag (will be set by main.py)
DEBUG_MODE = False

def print_debug(message: str):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

def parse_esummary_xml(xml_root: ET.Element) -> List[Dict[str, Any]]:
    """
    Parses the ESummary XML response and extracts relevant paper data.
    Returns a list of dictionaries, each representing a paper.
    Note: This parser extracts raw data; identification of non-academic authors
    and company affiliations will be handled in 'identifier.py'.
    """
    papers_raw_data = []
    if xml_root is None:
        return []

    for doc_sum in xml_root.findall(".//DocSum"):
        pubmed_id = doc_sum.find("Id").text if doc_sum.find("Id") is not None else "N/A"
        title = doc_sum.find(".//Item[@Name='Title']").text if doc_sum.find(".//Item[@Name='Title']") is not None else "N/A"
        pub_date = doc_sum.find(".//Item[@Name='PubDate']").text if doc_sum.find(".//Item[@Name='PubDate']") is not None else "N/A"

        authors: List[Author] = []
        author_list_elem = doc_sum.find(".//Item[@Name='AuthorList']")
        if author_list_elem is not None:
            for author_item in author_list_elem.findall(".//Item[@Name='Author']"):
                author_name_elem = author_item.find(".//Item[@Name='Name']")
                author_name = author_name_elem.text if author_name_elem is not None else "N/A"

                affiliation_elem = author_item.find(".//Item[@Name='Affiliation']")
                affiliation = affiliation_elem.text if affiliation_elem is not None else "N/A"

                if author_name != "N/A":
                    authors.append(Author(name=author_name, affiliation=affiliation))

        papers_raw_data.append({
            "pubmed_id": pubmed_id,
            "title": title,
            "publication_date": pub_date,
            "authors": authors, # List of Author objects
            "corresponding_author_email": "N/A" # ESummary doesn't typically provide email directly
        })
    print_debug(f"Parsed raw data for {len(papers_raw_data)} papers.")
    return papers_raw_data