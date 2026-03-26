# GROUP_DEPARTMENT_MAP = {
#     123456: "general",
#     123457: "hr",
#     123458: "finance",
#     123459: "engineering",
#     # 123460: "research",
# }


# def resolve_departments(group_ids):

#     departments = []

#     for gid in group_ids:

#         dept = GROUP_DEPARTMENT_MAP.get(gid)

#         if dept:
#             departments.append(dept)

#     # remove duplicates
#     departments = list(set(departments))

#     # ✅ ALWAYS include general (enterprise baseline access)
#     if "general" not in departments:
#         departments.append("general")

#     # fallback safety
#     if not departments:
#         departments = ["general"]

#     return departments


















# --------------------------------------------------
# GROUP → DEPARTMENT MAP
# --------------------------------------------------

GROUP_DEPARTMENT_MAP = {
    123456: "general",
    123457: "hr",
    123458: "finance",
    123459: "engineering",
}


# --------------------------------------------------
# RESOLVE DEPARTMENTS BASED ON ROLE
# --------------------------------------------------

def resolve_departments(user: dict):

    role = user.get("role", "user")
    group_ids = user.get("group_ids", [])

    # 🔥 ADMIN → FULL ACCESS
    if role == "admin":
        return list(set(GROUP_DEPARTMENT_MAP.values()))

    # 🔐 USER → LIMITED ACCESS
    allowed_departments = set()

    for gid in group_ids:
        dept = GROUP_DEPARTMENT_MAP.get(gid)
        if dept:
            allowed_departments.add(dept)

    return list(allowed_departments)