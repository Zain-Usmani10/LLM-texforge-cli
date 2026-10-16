import os
import shutil
import subprocess
import json
import sys

def main():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_dir = os.path.join(PROJECT_ROOT, "output")
    archive_root = os.path.join(PROJECT_ROOT, "archive")
    
    tex_file = os.path.join(output_dir, "Zain_Usmani_Resume.tex")
    pdf_file = os.path.join(output_dir, "Zain_Usmani_Resume.pdf")
    naming_file = os.path.join(output_dir, "naming.json")
    job_listing = os.path.join(PROJECT_ROOT, "job_listing.txt")
    cls_source = os.path.join(PROJECT_ROOT, "template", "template.cls")
    cls_dest = os.path.join(output_dir, "template.cls")

    if not os.path.exists(naming_file):
        print("Fatal Error: naming.json not found. Run generate pipeline first.")
        sys.exit(1)

    with open(naming_file, 'r', encoding='utf-8') as f:
        naming_data = json.load(f)

    company = naming_data.get("Company", "")
    position = naming_data.get("Position", "")
    req_id = naming_data.get("ReqID", "")

    if not os.path.exists(tex_file):
        print("Fatal Error: Zain_Usmani_Resume.tex not found in output folder.")
        sys.exit(1)

    if os.path.exists(cls_source):
        shutil.copy(cls_source, cls_dest)

    print("Executing pdflatex compilation...")
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Compilation failed due to LaTeX syntax errors.")
        print(result.stdout)
        sys.exit(1)

    base_name = f"{company}_{req_id}_{position}" if req_id else f"{company}_{position}"
    archive_dir = os.path.join(archive_root, company, base_name)
    os.makedirs(archive_dir, exist_ok=True)

    shutil.copy(pdf_file, os.path.join(archive_dir, f"{base_name}.pdf"))
    shutil.copy(tex_file, os.path.join(archive_dir, f"{base_name}.tex"))
    
    if os.path.exists(job_listing):
        shutil.copy(job_listing, os.path.join(archive_dir, "job_listing.txt"))

    junk_extensions = [".aux", ".log", ".out"]
    for ext in junk_extensions:
        junk_file = os.path.join(output_dir, f"Zain_Usmani_Resume{ext}")
        if os.path.exists(junk_file):
            os.remove(junk_file)

    print(f"Success: Files routed to {archive_dir}. Resume files retained in output folder.")

if __name__ == "__main__":
    main()