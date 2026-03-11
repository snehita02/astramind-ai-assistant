# import os
# from pathlib import Path

# from app.services.ingestion_service import ingest_pdf
# from app.services.ingestion_service import ingest_url
# from app.services.ingestion_service import ingest_repo


# KNOWLEDGE_PATH = Path("knowledge")


# def get_departments():
#     """Return department folders inside knowledge/"""
#     return [
#         d for d in KNOWLEDGE_PATH.iterdir()
#         if d.is_dir()
#     ]


# def get_files_by_type(department_path, folder_name):
#     """Return files inside pdf / urls / repos folders"""

#     folder = department_path / folder_name

#     if not folder.exists():
#         return []

#     return [
#         f for f in folder.iterdir()
#         if f.is_file()
#     ]


# def read_txt_file(file_path):
#     """Read URL or repo link from .txt"""

#     with open(file_path, "r") as f:
#         return f.read().strip()


# def ingest_department(department_path):

#     department = department_path.name

#     print("\n------------------------------------")
#     print(f"INGESTING DEPARTMENT: {department}")
#     print("------------------------------------")

#     pdf_files = get_files_by_type(department_path, "pdf")
#     url_files = get_files_by_type(department_path, "urls")
#     repo_files = get_files_by_type(department_path, "repos")

#     # -------------------------
#     # PDF INGESTION
#     # -------------------------

#     for pdf in pdf_files:

#         try:
#             print(f"📄 Ingesting PDF: {pdf.name}")

#             ingest_pdf(
#                 file_path=str(pdf),
#                 department=department,
#                 metadata={
#                     "source": pdf.name,
#                     "knowledge_type": "pdf"
#                 }
#             )

#         except Exception as e:
#             print(f"❌ Failed PDF ingestion: {pdf.name}")
#             print(e)

#     # -------------------------
#     # URL INGESTION
#     # -------------------------

#     for url_file in url_files:

#         try:
#             url = read_txt_file(url_file)

#             print(f"🌐 Ingesting URL: {url}")

#             ingest_url(
#                 url=url,
#                 department=department,
#                 metadata={
#                     "source": url_file.name,
#                     "knowledge_type": "url"
#                 }
#             )

#         except Exception as e:
#             print(f"❌ Failed URL ingestion: {url_file.name}")
#             print(e)

#     # -------------------------
#     # REPO INGESTION
#     # -------------------------

#     for repo_file in repo_files:

#         try:
#             repo_url = read_txt_file(repo_file)

#             print(f"📦 Ingesting Repo: {repo_url}")

#             ingest_repo(
#                 repo_url=repo_url,
#                 department=department,
#                 metadata={
#                     "source": repo_file.name,
#                     "knowledge_type": "repository"
#                 }
#             )

#         except Exception as e:
#             print(f"❌ Failed Repo ingestion: {repo_file.name}")
#             print(e)


# def run_ingestion():

#     print("\n====================================")
#     print("ASTRAMIND KNOWLEDGE INGESTION STARTED")
#     print("====================================")

#     departments = get_departments()

#     for dept in departments:
#         ingest_department(dept)

#     print("\n====================================")
#     print("INGESTION COMPLETED")
#     print("====================================")


# if __name__ == "__main__":
#     run_ingestion()


import os
from pathlib import Path

from app.services.ingestion_service import ingest_pdf
from app.services.ingestion_service import ingest_url
from app.services.ingestion_service import ingest_repo


KNOWLEDGE_PATH = Path("knowledge")


def get_departments():
    """Return department folders inside knowledge/"""
    return [
        d for d in KNOWLEDGE_PATH.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]


def get_files_by_type(department_path, folder_name):
    """Return files inside pdf / urls / repos folders"""

    folder = department_path / folder_name

    if not folder.exists():
        return []

    return [
        f for f in folder.iterdir()
        if f.is_file() and not f.name.startswith(".")
    ]


def read_txt_file(file_path):
    """Read URL or repo link from .txt"""

    with open(file_path, "r") as f:
        return f.read().strip()


def ingest_department(department_path):

    department = department_path.name

    print("\n------------------------------------")
    print(f"INGESTING DEPARTMENT: {department}")
    print("------------------------------------")

    pdf_files = get_files_by_type(department_path, "pdf")
    url_files = get_files_by_type(department_path, "urls")
    repo_files = get_files_by_type(department_path, "repos")

    # -------------------------
    # PDF INGESTION
    # -------------------------

    for pdf in pdf_files:

        try:
            print(f"📄 Ingesting PDF: {pdf.name}")

            ingest_pdf(
                file_path=str(pdf),
                department=department
            )

        except Exception as e:
            print(f"❌ Failed PDF ingestion: {pdf.name}")
            print(e)

    # -------------------------
    # URL INGESTION
    # -------------------------

    for url_file in url_files:

        try:
            url = read_txt_file(url_file)

            print(f"🌐 Ingesting URL: {url}")

            ingest_url(
                url=url,
                department=department
            )

        except Exception as e:
            print(f"❌ Failed URL ingestion: {url_file.name}")
            print(e)

    # -------------------------
    # REPO INGESTION
    # -------------------------

    for repo_file in repo_files:

        try:
            repo_url = read_txt_file(repo_file)

            print(f"📦 Ingesting Repo: {repo_url}")

            ingest_repo(
                repo_url=repo_url,
                department=department
            )

        except Exception as e:
            print(f"❌ Failed Repo ingestion: {repo_file.name}")
            print(e)


def run_ingestion():

    print("\n====================================")
    print("ASTRAMIND KNOWLEDGE INGESTION STARTED")
    print("====================================")

    departments = get_departments()

    for dept in departments:
        ingest_department(dept)

    print("\n====================================")
    print("INGESTION COMPLETED")
    print("====================================")


if __name__ == "__main__":
    run_ingestion()