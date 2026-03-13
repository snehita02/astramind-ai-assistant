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


























# --------------------------------------------------
# Department mapping for enterprise access control
# --------------------------------------------------

GROUP_DEPARTMENT_MAP = {

    123456: "general",
    123457: "engineering",
    123458: "finance",
    123459: "hr",
    123460: "research"

}


# --------------------------------------------------
# Resolve allowed departments for a user
# --------------------------------------------------

def resolve_departments(group_ids):

    departments = []

    for gid in group_ids:

        dept = GROUP_DEPARTMENT_MAP.get(gid)

        if dept:
            departments.append(dept)

    return departments


# --------------------------------------------------
# Check access to a department
# --------------------------------------------------

def has_department_access(group_ids, department):

    allowed_departments = resolve_departments(group_ids)

    return department in allowed_departments