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




# =====================================================
# Group → Department Mapping
# =====================================================

GROUP_DEPARTMENT_MAP = {
    123456: ["general"],
    123457: ["hr"],
    123458: ["finance"],
    123459: ["engineering"],
    123460: ["research"]
}


# =====================================================
# Resolve Allowed Departments
# =====================================================

def resolve_departments(group_ids):

    departments = set()

    for gid in group_ids:

        if gid in GROUP_DEPARTMENT_MAP:

            for dept in GROUP_DEPARTMENT_MAP[gid]:
                departments.add(dept)

    return list(departments)