# def classify_query(query: str):

#     q = query.lower()

#     if any(word in q for word in ["leave", "vacation", "benefits"]):
#         return "hr"

#     if any(word in q for word in ["expense", "reimbursement", "invoice"]):
#         return "finance"

#     if any(word in q for word in ["deploy", "api", "code"]):
#         return "engineering"

#     return "general"














def classify_query(query: str):
    """
    Very simple rule based query classifier
    Maps user questions to departments
    """

    q = query.lower()

    if any(word in q for word in ["salary", "leave", "policy", "benefits"]):
        return "hr"

    if any(word in q for word in ["expense", "invoice", "reimbursement", "payment"]):
        return "finance"

    if any(word in q for word in ["code", "api", "deployment", "engineering"]):
        return "engineering"

    if any(word in q for word in ["research", "paper", "experiment"]):
        return "research"

    return "general"