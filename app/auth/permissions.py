# GROUP_DEPARTMENT_MAP = {
#     123456: "general",
#     123457: "engineering",
#     123458: "finance",
#     123459: "hr",
#     123460: "research"
# }


# def resolve_departments(group_ids):
#     """
#     Convert user group IDs into allowed departments
#     """

#     departments = []

#     for gid in group_ids:
#         if gid in GROUP_DEPARTMENT_MAP:
#             departments.append(GROUP_DEPARTMENT_MAP[gid])

#     return departments


# def has_department_access(group_ids, department):
#     """
#     Check if user can access a specific department
#     """

#     allowed_departments = resolve_departments(group_ids)

#     return department in allowed_departments


























# # --------------------------------------------------
# # Department mapping for enterprise access control
# # --------------------------------------------------

# GROUP_DEPARTMENT_MAP = {

#     123456: "general",
#     123457: "engineering",
#     123458: "finance",
#     123459: "hr",
#     123460: "research"

# }


# # --------------------------------------------------
# # Resolve allowed departments for a user
# # --------------------------------------------------

# def resolve_departments(group_ids):

#     departments = []

#     for gid in group_ids:

#         dept = GROUP_DEPARTMENT_MAP.get(gid)

#         if dept:
#             departments.append(dept)

#     return departments


# # --------------------------------------------------
# # Check access to a department
# # --------------------------------------------------

# def has_department_access(group_ids, department):

#     allowed_departments = resolve_departments(group_ids)

#     return department in allowed_departments









# # --------------------------------------------------
# # Department mapping for enterprise access control
# # --------------------------------------------------

# GROUP_DEPARTMENT_MAP = {

#     123456: "general",
#     123457: "engineering",
#     123458: "finance",
#     123459: "hr",
#     123460: "research"

# }


# # --------------------------------------------------
# # All departments
# # --------------------------------------------------

# ALL_DEPARTMENTS = [
#     "general",
#     "engineering",
#     "finance",
#     "hr",
#     "research"
# ]


# # --------------------------------------------------
# # Resolve allowed departments for a user
# # --------------------------------------------------

# def resolve_departments(group_ids):

#     if not group_ids:
#         return []

#     departments = []

#     for gid in group_ids:

#         try:
#             gid = int(gid)
#         except:
#             continue

#         dept = GROUP_DEPARTMENT_MAP.get(gid)

#         if dept:
#             departments.append(dept)

#     # Remove duplicates
#     departments = list(set(departments))

#     return departments


# # --------------------------------------------------
# # Check access to a department
# # --------------------------------------------------

# def has_department_access(group_ids, department):

#     allowed_departments = resolve_departments(group_ids)

#     return department in allowed_departments













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

#     # fallback safety
#     if not departments:
#         departments = ["general"]

#     return departments

























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

#     # fallback safety
#     if not departments:
#         departments = ["general"]

#     return departments





GROUP_DEPARTMENT_MAP = {
    123456: "general",
    123457: "hr",
    123458: "finance",
    123459: "engineering",
    # 123460: "research",
}


def resolve_departments(group_ids):

    departments = []

    for gid in group_ids:

        dept = GROUP_DEPARTMENT_MAP.get(gid)

        if dept:
            departments.append(dept)

    # remove duplicates
    departments = list(set(departments))

    # ✅ ALWAYS include general (enterprise baseline access)
    if "general" not in departments:
        departments.append("general")

    # fallback safety
    if not departments:
        departments = ["general"]

    return departments