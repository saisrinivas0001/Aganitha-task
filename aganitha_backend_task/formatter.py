import csv
import sys
from typing import List, Dict, Any 
from .models import Paper
DEBUG_MODE = False

def print_debug(message: str):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

def format_papers_to_dicts(papers: List[Paper]) -> List[Dict[str, Any]]: 
    """
    Converts a list of Paper objects into a list of dictionaries,
    suitable for CSV writing.
    """
    formatted_data = []
    for paper in papers:
        formatted_data.append({
            "PubmedID": paper.pubmed_id,
            "Title": paper.title,
            "Publication Date": paper.publication_date,
            "Non-academic Author(s)": ", ".join(paper.non_academic_authors) if paper.non_academic_authors else "N/A",
            "Company Affiliation(s)": ", ".join(sorted(paper.company_affiliations)) if paper.company_affiliations else "N/A",
            "Corresponding Author Email": paper.corresponding_author_email
        })
    print_debug(f"Formatted {len(formatted_data)} papers for output.")
    return formatted_data

def write_results_to_csv(data: List[Dict[str, Any]], output_file: str = None):
    """
    Writes the fetched paper data to a CSV file or prints to console.
    Assumes `data` is a list of dictionaries with appropriate keys.
    """
    if not data:
        print("No data to write.")
        return

    
    fieldnames = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    if output_file:
        print(f"Writing results to {output_file}...")
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Results successfully saved to {output_file}")
        except IOError as e:
            print(f"Error writing to file {output_file}: {e}")
    else:
        print("--- Results (Console Output) ---")
        print(",".join(fieldnames))
        for row in data:
            print(",".join(str(row.get(col, "")) for col in fieldnames))
        print("--- End of Results ---")