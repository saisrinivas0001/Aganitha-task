from typing import List, Set, Tuple, Dict, Any # Ensure List, Dict, Any are imported here
from .models import Paper, Author # Relative import for models

# Keywords to identify academic affiliations (case-insensitive)
ACADEMIC_KEYWORDS = {
    "university", "college", "institute", "school", "dept", "department",
    "hospital", "medical center", "research center", "academy", "clinic",
    "laboratories", "lab", "health system", "foundation", "charity",
    "phd", "md", "faculty", "professor", "student", "fellow", "postdoc",
    "center for disease control", "cdc", "nih", "fda", "who" # Common public health organizations
}

# Expanded Keywords to identify common corporate/company affiliations (case-insensitive)
COMPANY_KEYWORDS = {
    "pharma", "pharmaceutical", "biotech", "company", "inc", "ltd", "corp",
    "corporation", "s.p.a.", "gmbh", "ag", "co.", "llc", "plc", "sa",
    "rnd", "research and development", "clinical development",
    "diagnostics", "manufacturing", "solutions", "therapeutics", "sciences",
    "innovations", "health", "life sciences", "group", "labs",
    # Specific company names (case-insensitive due to .lower() later)
    "pfizer", "merck", "astrazeneca", "gilead", "novartis", "roche", "bayer",
    "johnson & johnson", "sanofi", "eli lilly", "abbvie", "amgen", "biogen",
    "genentech", "takeda", "moderna", "biontech", "glaxosmithkline", "gsk",
    "boehringer ingelheim", "regeneron", "vertex", "celgene", "bristol myers squibb", "bms",
    "novavax", "janssen", "daiichi sankyo", "servier", "cubist", "shionogi",
    "syngenta", "basf", "monsanto", "dupont", # Agri-biotech, less likely but still biotech
    "samsung bioepis", "biosimilar", "celltrion", "teva", "mylan", "grifols"
}

# Global debug flag (will be set by main.py)
DEBUG_MODE = False

def print_debug(message: str):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

def identify_affiliations(authors: List[Author]) -> Tuple[List[str], List[str]]:
    """
    Processes a list of Author objects to identify non-academic authors and company affiliations.
    Returns a tuple: (list of non-academic author names, list of company affiliation strings).
    """
    non_academic_authors: List[str] = []
    company_affiliations: Set[str] = set() # Use a set to avoid duplicate company names

    for author in authors:
        affiliation_lower = author.affiliation.lower()
        
        is_academic = False
        for keyword in ACADEMIC_KEYWORDS:
            if keyword in affiliation_lower:
                is_academic = True
                break
        
        is_company = False
        for keyword in COMPANY_KEYWORDS:
            if keyword in affiliation_lower:
                is_company = True
                break

        # An author is considered non-academic if their affiliation contains a company keyword
        # OR if it doesn't contain an academic keyword but contains a non-empty, non-"N/A" string.
        # This heuristic still needs refinement as discussed.
        if is_company: # Prioritize company affiliation if found
            if author.name not in non_academic_authors: # Avoid adding same author multiple times
                non_academic_authors.append(author.name)
            
            # Extract a more precise company name if possible, otherwise use the full affiliation
            found_company = False
            for keyword in COMPANY_KEYWORDS:
                if keyword in affiliation_lower:
                    # Simple heuristic: try to capitalize the keyword found in the affiliation
                    # and add it. This is a very basic attempt.
                    company_affiliations.add(author.affiliation.strip()) # Add full affiliation for now
                    found_company = True
                    break
            # If no specific company keyword was matched, but it was still marked as company-affiliated
            # based on broader rules, add the affiliation as-is.
            if not found_company and is_company:
                 company_affiliations.add(author.affiliation.strip())
        
        print_debug(f"Author: {author.name}, Affiliation: '{author.affiliation}' (Academic: {is_academic}, Company: {is_company})")

    return non_academic_authors, list(company_affiliations)

def process_papers_for_affiliations(raw_papers_data: List[Dict[str, Any]]) -> List[Paper]:
    """
    Takes raw paper data (from parser) and applies identification heuristics.
    Returns a list of structured Paper objects.
    """
    processed_papers: List[Paper] = []
    for raw_paper in raw_papers_data:
        non_academic_authors_list, company_affiliations_list = \
            identify_affiliations(raw_paper["authors"])

        # Create a Paper object
        paper = Paper(
            pubmed_id=raw_paper["pubmed_id"],
            title=raw_paper["title"],
            publication_date=raw_paper["publication_date"],
            non_academic_authors=non_academic_authors_list,
            company_affiliations=company_affiliations_list,
            corresponding_author_email=raw_paper["corresponding_author_email"]
        )
        processed_papers.append(paper)
    
    print_debug(f"Processed {len(processed_papers)} papers for affiliations.")
    return processed_papers