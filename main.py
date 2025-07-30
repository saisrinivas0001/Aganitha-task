import argparse
import sys

from aganitha_backend_task import api
from aganitha_backend_task import parser # This is your module for parsing XML
from aganitha_backend_task import identifier
from aganitha_backend_task import formatter
from aganitha_backend_task import models

def main():
    cli_parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed based on a query and identify authors from pharmaceutical/biotech companies."
    )

    cli_parser.add_argument(
        "query",
        type=str,
        help="The search query for PubMed (e.g., 'COVID-19 vaccine clinical trials')."
    )

    cli_parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Print debug information during execution."
    )

    cli_parser.add_argument(
        "-f", "--file",
        type=str,
        help="Specify the filename to save the results (e.g., 'results.csv'). If not provided, output is printed to console."
    )

    args = cli_parser.parse_args()

    # Set debug flag for all modules
    api.DEBUG_MODE = args.debug
    parser.DEBUG_MODE = args.debug # This 'parser' refers to your imported module, which is correct
    identifier.DEBUG_MODE = args.debug
    formatter.DEBUG_MODE = args.debug

    def print_debug(message: str):
        if args.debug:
            print(f"[DEBUG] {message}")

    print_debug(f"Starting paper fetching for query: '{args.query}'")
    
    pubmed_ids = api.search_pubmed(args.query)

    papers_data_for_output = []
    if pubmed_ids:
        esummary_root = api.get_pubmed_summaries(pubmed_ids)
        
        if esummary_root is not None:
            raw_papers = parser.parse_esummary_xml(esummary_root) 
            processed_papers = identifier.process_papers_for_affiliations(raw_papers)
            papers_data_for_output = formatter.format_papers_to_dicts(processed_papers)
            
            print_debug(f"Fetched and processed details for {len(processed_papers)} papers.")
        else:
            print_debug("No ESummary XML received or parsed.")
    else:
        print("No PubMed IDs found for the given query.")

    formatter.write_results_to_csv(papers_data_for_output, args.file)

    print_debug("Program finished.")

if __name__ == "__main__":
    main()
