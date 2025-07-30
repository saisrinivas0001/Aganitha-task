# PubMed Paper Analysis Tool

This project provides a Python command-line interface (CLI) tool to fetch research papers from PubMed based on a user-specified query. Its primary function is to identify papers with at least one author affiliated with a pharmaceutical or biotech company and return the relevant details, including non-academic authors and their company affiliations, as a CSV file or directly to the console.

## Code Organization

The project is structured into several modular Python files to ensure clear separation of concerns, readability, and maintainability:

* `main.py`: This is the primary entry point for the command-line interface. It handles argument parsing, orchestrates the workflow by calling functions from other modules, and manages debug logging.
* `aganitha_backend_task/` (Python Package Directory):
    * `__init__.py`: An empty file that signifies this directory as a Python package, allowing its modules to be imported.
    * `api.py`: Contains functions responsible for interacting with the PubMed API (ESearch for searching, ESummary for fetching paper details). It handles API requests, error handling for network issues and XML parsing, and returns raw XML data or PubMed IDs.
    * `parser.py`: Dedicated to parsing the raw XML responses received from the PubMed ESummary API. It extracts relevant information like PubMed ID, title, publication date, and authors with their affiliations, structuring them into an intermediate format (list of dictionaries containing `Author` objects).
    * `identifier.py`: Implements the core logic for identifying non-academic authors and pharmaceutical/biotech company affiliations. It uses predefined keyword lists (`ACADEMIC_KEYWORDS` and `COMPANY_KEYWORDS`) and applies heuristics to classify affiliations. It then processes the raw paper data to enrich `Paper` objects with identified non-academic authors and companies.
    * `formatter.py`: Handles the formatting of processed paper data into a structured format suitable for output. It can write the results to a CSV file or print them directly to the console.
    * `models.py`: Defines the data structures (dataclasses) used throughout the application, specifically `Paper` and `Author` objects, to ensure type safety and clarity of data representation.

## Installation

To set up and run this project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/saisrinivas0001/aganitha-backend-task.git](https://github.com/saisrinivas0001/aganitha-backend-task.git)
    cd aganitha-backend-task
    ```
2.  **Install dependencies using Poetry:**
    This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. If you don't have Poetry installed, follow their official installation guide.
    Once Poetry is installed, navigate to the project's root directory and install the dependencies:
    ```bash
    poetry install
    ```

## Usage

The program can be executed via a Poetry-defined script named `get-papers-list`.

**Basic Usage:**

To search for papers and print the results to the console:

```bash
poetry run get-papers-list "vaccine clinical trial pharmaceutical"

