GROUP_DEPARTMENT_MAP = {

    123456: "general",
    123457: "hr",
    123458: "finance",
    123459: "engineering",
    123460: "research"

}


def resolve_departments(group_ids):

    departments = []

    for gid in group_ids:

        dept = GROUP_DEPARTMENT_MAP.get(gid)

        if dept:
            departments.append(dept)

    return departments