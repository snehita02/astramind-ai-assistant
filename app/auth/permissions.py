# # --------------------------------------------------
# # Group → Department Permission Map
# # --------------------------------------------------

# GROUP_DEPARTMENT_MAP = {
#     123456: ["general"],
#     123457: ["hr"],
#     123458: ["finance"],
#     123459: ["engineering"],
#     123460: ["research"]
# }


# # --------------------------------------------------
# # Resolve Departments From User Groups
# # --------------------------------------------------

# def resolve_departments(group_ids):

#     departments = set()

#     for gid in group_ids:

#         if gid in GROUP_DEPARTMENT_MAP:

#             departments.update(GROUP_DEPARTMENT_MAP[gid])

#     return list(departments)













GROUP_DEPARTMENT_MAP = {
    123456: "general",
    123457: "engineering",
    123458: "finance",
    123459: "hr",
    123460: "research"
}


def resolve_departments(group_ids):

    departments = []

    for gid in group_ids:

        if gid in GROUP_DEPARTMENT_MAP:
            departments.append(GROUP_DEPARTMENT_MAP[gid])

    return departments