from __future__ import annotations


REFERENCE_CONCEPTS = {
    "Machine Learning": (
        "Machine learning is a branch of artificial intelligence where systems learn "
        "patterns from data and improve performance on tasks without being explicitly "
        "programmed for every rule."
    ),
    "Cloud Computing": (
        "Cloud computing provides computing resources such as storage, servers, and "
        "applications over the internet with scalability, availability, and pay-as-you-use access."
    ),
    "Database Management System": (
        "A database management system stores, organizes, secures, and retrieves data efficiently "
        "using structured models, queries, transactions, and access control."
    ),
    "Computer Network": (
        "A computer network connects devices so they can exchange data and share resources using "
        "communication protocols, addressing, routing, and transmission media."
    ),
}


def get_concept_reference(concept_name: str) -> str:
    return REFERENCE_CONCEPTS.get(concept_name, next(iter(REFERENCE_CONCEPTS.values())))
