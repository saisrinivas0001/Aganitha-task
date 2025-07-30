import requests
import xml.etree.ElementTree as ET
from typing import List

# PubMed API endpoint for ESearch (searching)
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
# PubMed API endpoint for ESummary (getting summaries/details for UIDs)
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

DEBUG_MODE = False

def print_debug(message: str):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

def search_pubmed(query: str) -> List[str]:
    """
    Searches PubMed for a given query and returns a list of PubMed IDs (UIDs).
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 10,
        "retmode": "xml"
    }
    print_debug(f"Sending ESearch request with params: {params}")
    try:
        response = requests.get(ESEARCH_URL, params=params)
        response.raise_for_status() 
        print_debug(f"ESearch response status: {response.status_code}")
        root = ET.fromstring(response.content)

        pubmed_ids = [id_elem.text for id_elem in root.findall(".//Id")]
        print_debug(f"Found {len(pubmed_ids)} PubMed IDs.")
        return pubmed_ids

    except requests.exceptions.RequestException as e:
        print(f"Error searching PubMed: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing ESearch XML response: {e}")
        print_debug(f"Problematic XML: {response.content.decode()}")
        return []

def get_pubmed_summaries(pubmed_ids: List[str]) -> ET.Element: 
    """
    Fetches XML summaries for a list of PubMed IDs using ESummary.
    Returns the root element of the XML response.
    """
    if not pubmed_ids:
        return None

    id_list = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": id_list,
        "retmode": "xml"
    }
    print_debug(f"Sending ESummary request with params: {params}")
    try:
        response = requests.get(ESUMMARY_URL, params=params)
        response.raise_for_status()
        print_debug(f"ESummary response status: {response.status_code}")
        root = ET.fromstring(response.content)
        return root
    except requests.exceptions.RequestException as e:
        print(f"Error fetching paper details from ESummary: {e}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing ESummary XML response: {e}")
        print_debug(f"Problematic XML: {response.content.decode()}")
        return None