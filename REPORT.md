Project Report: PubMed Paper Analysis Tool
1. Introduction and Objective
This project aims to develop a Python command-line interface (CLI) tool designed to interact with the PubMed API. The core objective is to search for research papers based on a user-defined query, retrieve their detailed summaries, and specifically identify authors affiliated with pharmaceutical or biotech companies. The processed information is then presented in a structured format, either directly to the console or saved to a CSV file.

2. Approach and Methodology
The development followed a modular and iterative approach, breaking down the problem into distinct components for clarity, maintainability, and easier debugging.

2.1 Modular Design:
The application is structured into the following key modules:

main.py: The central entry point for the CLI. It handles command-line argument parsing using argparse and orchestrates the flow by calling functions from other modules.

aganitha_backend_task/ (Python Package):

api.py: Manages all interactions with the PubMed ESearch and ESummary APIs, handling HTTP requests via the requests library and basic error checking for network and API responses.

parser.py: Responsible for parsing the raw XML data received from the PubMed ESummary API. It extracts relevant details such as PubMed ID, title, publication date, authors, and their affiliations using xml.etree.ElementTree.

identifier.py: Implements the core logic for identifying non-academic authors and company affiliations. It utilizes predefined lists of ACADEMIC_KEYWORDS (e.g., "university", "hospital") and COMPANY_KEYWORDS (e.g., "pharma", "biotech", "inc", "corp", specific company names). An author is currently flagged as "non-academic" if their affiliation string contains any of the COMPANY_KEYWORDS.

models.py: Defines data structures (dataclasses for Paper and Author) to ensure strong typing and clear representation of the extracted and processed data throughout the application.

formatter.py: Handles the final presentation of the processed paper data, converting Paper objects into a dictionary format suitable for output, and managing writing to the console or a CSV file using the csv module.

2.2 Development Process & Debugging:
The development was highly iterative, particularly in addressing various Python-specific errors. The process involved:

Typo Correction: Resolving ImportError and AttributeError caused by minor spelling mistakes in module names (formater vs formatter) and variable shadowing (parser object vs parser module).

Module Resolution: Debugging ModuleNotFoundError by correctly configuring the Poetry script entry point in pyproject.toml to reflect the main.py file's location (main:main instead of aganitha_backend_task.main:main).

Poetry Environment Management: Troubleshooting Poetry's command does not exist and Repository not defined errors by ensuring correct pyproject.toml configuration for scripts and repositories, and performing environment resets (poetry env remove python, poetry install).

Git/GitHub Integration: Managing unrelated histories errors during the final push to GitHub by understanding when git push --force is appropriate for initial project uploads.

2.3 Tools and Libraries:

Python 3.x: The primary programming language.

Poetry: Used extensively for project setup, dependency management (requests, lxml), virtual environment creation, and defining the get-papers-list executable command.

requests: For making HTTP requests to the PubMed API.

xml.etree.ElementTree: Python's built-in XML parsing library.

dataclasses: For creating structured data models (Paper, Author).

argparse: For building the command-line interface.

csv: For writing results to CSV files.

typing: Utilized for type hints across the codebase, enhancing readability and maintainability.

Google Gemini (This AI): Served as an invaluable assistant throughout the development, providing guidance, debugging assistance, code snippets, and explanations for various errors and concepts.

Git/GitHub: For version control and hosting the project repository.

3. Results
The development effort has resulted in a fully functional and well-structured application that meets the core requirements:

Successful API Interaction: The program reliably fetches PubMed IDs and detailed summaries from the NCBI E-utilities.

Robust Data Processing: XML responses are parsed, and relevant paper and author details are extracted into structured Python objects.

Affiliation Identification: The heuristic-based identification logic successfully processes author affiliations, though its effectiveness is dependent on the comprehensiveness of the keyword lists.

Flexible Output: Results can be printed directly to the console or saved to a specified CSV file.

User-Friendly CLI: The get-papers-list command allows users to easily query PubMed with debug options and file output.

Example Console Output:

[DEBUG] Starting paper fetching for query: 'vaccine clinical trial pharmaceutical'
[DEBUG] Sending ESearch request with params: {'db': 'pubmed', 'term': 'vaccine clinical trial pharmaceutical', 'retmax': 10, 'retmode': 'xml'}
[DEBUG] ESearch response status: 200
[DEBUG] Found 10 PubMed IDs.
[DEBUG] Sending ESummary request with params: {'db': 'pubmed', 'id': '40735070,40730836,40716144,40700358,40698536,40696259,40694515,40676801,40658400,40658388', 'retmode': 'xml'}
[DEBUG] ESummary response status: 200
[DEBUG] Parsed raw data for 10 papers.
[DEBUG] Processed 10 papers for affiliations.
[DEBUG] Formatted 10 papers for output.
[DEBUG] Fetched and processed details for 10 papers.
--- Results (Console Output) ---
PubmedID,Title,Publication Date,Non-academic Author(s),Company Affiliation(s),Corresponding Author Email
40735070,Immunotherapy in Glioblastoma: An Overview of Current Status.,2025,N/A,N/A,N/A
40730836,Safety and immunogenicity of fractional COVID-19 vaccine doses in Nigerian adults: A randomized non-inferiority trial.,2025 Jul 29,N/A,N/A,N/A 
40716144,Longitudinal Meta-cohort study protocol using systems biology to identify vaccine safety biomarkers.,2025 Jul 26,N/A,N/A,N/A
... (truncated for brevity) ...
--- End of Results ---
[DEBUG] Program finished.
Note: For the given sample query and top 10 results, no specific company affiliations were identified, resulting in "N/A" for those columns in this particular output.

Bonus Points Achieved:

Modular Program & CLI: The application is well-modularized and exposed via a robust CLI.

Poetry Integration: Fully utilizes Poetry for project management.

TestPyPI Publication: The project was successfully built and published to TestPyPI, demonstrating packaging and distribution capabilities.

4. Conclusion and Future Enhancements
The PubMed Paper Analysis Tool successfully addresses the problem statement, providing a functional solution for fetching and analyzing research papers. The modular design enhances its maintainability and extensibility.

Potential Future Enhancements:

Advanced Affiliation Heuristics: Implement more sophisticated regular expressions or NLP techniques for affiliation parsing to better capture complex company names and differentiate from academic departments.

Expanded Keyword Lists: Continuously update and expand ACADEMIC_KEYWORDS and COMPANY_KEYWORDS for better accuracy.

Configurable Keywords: Allow users to provide custom keyword lists via CLI arguments or a configuration file.

Robust Error Logging: Implement a more robust logging system (e.g., using Python's logging module) for better debugging and operational monitoring.

Pagination/Deeper Search: Implement logic to retrieve more than the top 10 results (e.g., retmax parameter handling with pagination).

Asynchronous Requests: For larger queries, consider asyncio and aiohttp for more efficient concurrent API calls.

Unit Tests: Develop comprehensive unit tests for each module to ensure reliability and prevent regressions.