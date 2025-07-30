import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class Paper:
    """Represents a research paper fetched from PubMed."""
    pubmed_id: str
    title: str
    publication_date: str
    non_academic_authors: List[str]
    company_affiliations: List[str]
    corresponding_author_email: str # Placeholder, as email is not typically in ESummary

@dataclasses.dataclass
class Author:
    """Represents an author of a paper with their affiliation."""
    name: str
    affiliation: str