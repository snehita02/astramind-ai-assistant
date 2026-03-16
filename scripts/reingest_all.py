# import os
# import sys
# from pathlib import Path

# # --------------------------------------------------
# # Fix Python path so "app" module is visible
# # --------------------------------------------------

# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# sys.path.append(str(PROJECT_ROOT))


# # --------------------------------------------------
# # Now imports will work
# # --------------------------------------------------

# from app.services.ingestion_service import ingest_pdf
# from app.services.url_ingestion_service import ingest_url
# from app.services.repo_ingestion_service import ingest_repo


# KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"


# # --------------------------------------------------
# # Detect department from folder name
# # --------------------------------------------------

# def detect_department(path):

#     parts = path.parts

#     if "hr" in parts:
#         return "hr"

#     if "engineering" in parts:
#         return "engineering"

#     if "finance" in parts:
#         return "finance"

#     if "research" in parts:
#         return "research"

#     return "general"


# # --------------------------------------------------
# # Ingest PDFs
# # --------------------------------------------------

# def ingest_all_pdfs():

#     print("\nScanning PDFs...\n")

#     for file in KNOWLEDGE_DIR.rglob("*.pdf"):

#         dept = detect_department(file)

#         print(f"Ingesting PDF: {file} | Department: {dept}")

#         try:
#             ingest_pdf(str(file), dept)
#         except Exception as e:
#             print(f"Failed: {file} | Error: {e}")


# # --------------------------------------------------
# # Ingest URLs
# # --------------------------------------------------

# def ingest_all_urls():

#     print("\nScanning URL files...\n")

#     for file in KNOWLEDGE_DIR.rglob("*urls.txt"):

#         dept = detect_department(file)

#         with open(file, "r") as f:
#             urls = f.readlines()

#         for url in urls:

#             url = url.strip()

#             if not url:
#                 continue

#             print(f"Ingesting URL: {url} | Department: {dept}")

#             try:
#                 ingest_url(url, dept)
#             except Exception as e:
#                 print(f"Failed: {url} | Error: {e}")


# # --------------------------------------------------
# # Ingest Repositories
# # --------------------------------------------------

# def ingest_all_repos():

#     print("\nScanning Repo files...\n")

#     for file in KNOWLEDGE_DIR.rglob("*repos.txt"):

#         dept = detect_department(file)

#         with open(file, "r") as f:
#             repos = f.readlines()

#         for repo in repos:

#             repo = repo.strip()

#             if not repo:
#                 continue

#             print(f"Ingesting Repo: {repo} | Department: {dept}")

#             try:
#                 ingest_repo(repo, dept)
#             except Exception as e:
#                 print(f"Failed: {repo} | Error: {e}")


# # --------------------------------------------------
# # Main
# # --------------------------------------------------

# if __name__ == "__main__":

#     print("\n========== AstraMind Full Re-Ingestion ==========\n")

#     ingest_all_pdfs()
#     ingest_all_urls()
#     ingest_all_repos()

#     print("\n========== Re-ingestion Completed ==========\n")



















import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.services.ingestion_service import ingest_pdf
from app.services.url_ingestion_service import ingest_url
from app.services.repo_ingestion_service import ingest_repo


KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"


# --------------------------------------------------
# Ingest PDFs
# --------------------------------------------------

def ingest_pdfs(department_path):

    pdf_dir = department_path / "pdf"

    if not pdf_dir.exists():
        return

    for pdf_file in pdf_dir.glob("*.pdf"):

        print(f"Ingesting PDF: {pdf_file}")

        try:
            ingest_pdf(str(pdf_file), department_path.name)
        except Exception as e:
            print(f"Failed: {pdf_file} | {e}")


# --------------------------------------------------
# Ingest URL files
# --------------------------------------------------

def ingest_urls(department_path):

    url_dir = department_path / "urls"

    if not url_dir.exists():
        return

    for url_file in url_dir.glob("*.txt"):

        with open(url_file) as f:
            urls = f.readlines()

        for url in urls:

            url = url.strip()

            if not url:
                continue

            print(f"Ingesting URL: {url}")

            try:
                ingest_url(url, department_path.name)
            except Exception as e:
                print(f"Failed: {url} | {e}")


# --------------------------------------------------
# Ingest Repo files
# --------------------------------------------------

def ingest_repos(department_path):

    repo_dir = department_path / "repos"

    if not repo_dir.exists():
        return

    for repo_file in repo_dir.glob("*.txt"):

        with open(repo_file) as f:
            repos = f.readlines()

        for repo in repos:

            repo = repo.strip()

            if not repo:
                continue

            print(f"Ingesting Repo: {repo}")

            try:
                ingest_repo(repo, department_path.name)
            except Exception as e:
                print(f"Failed: {repo} | {e}")


# --------------------------------------------------
# Main ingestion pipeline
# --------------------------------------------------

def ingest_all():

    print("\n=========== FULL KNOWLEDGE INGESTION ===========\n")

    for department_path in KNOWLEDGE_DIR.iterdir():

        if not department_path.is_dir():
            continue

        department = department_path.name

        print(f"\nProcessing department: {department}\n")

        ingest_pdfs(department_path)
        ingest_urls(department_path)
        ingest_repos(department_path)

    print("\n=========== INGESTION COMPLETE ===========\n")


if __name__ == "__main__":
    ingest_all()
