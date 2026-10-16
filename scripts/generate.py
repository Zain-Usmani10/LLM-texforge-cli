import os
import json
import sys
import re

def clean_company_name(name):
    name = re.sub(r'(?i)\b(Inc|LLC|Corp|Corporation|ULC|Ltd|Limited|Canada|Technologies|Group)\b\.?', '', name)
    name = re.sub(r'[^\w\s-]', '', name)
    return name.strip().title()

def main():
    print("Reading metadata from standard input...")
    raw_metadata = sys.stdin.read().strip()
    
    if not raw_metadata:
        print("Fatal Error: No metadata received from PowerShell.")
        sys.exit(1)

    try:
        clean_json = raw_metadata.replace("```json", "").replace("```", "").strip()
        metadata = json.loads(clean_json)
    except json.JSONDecodeError as e:
        print(f"Fatal Error: Failed to parse JSON metadata from Claude {e}")
        print(f"Raw output received: {raw_metadata}")
        sys.exit(1)

    raw_company = metadata.get("Company", "").strip()
    position = metadata.get("Position", "").strip()
    req_id = metadata.get("ReqID", "").strip()

    company = clean_company_name(raw_company)

    if not company or not position:
        print("Fatal Error: Could not extract Company and Position from JSON.")
        sys.exit(1)
        
    print(f"Extracted: {company} | {position} | {req_id}")

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)

    naming_data = {
        "Company": company,
        "Position": position,
        "ReqID": req_id
    }

    naming_file = os.path.join(output_dir, "naming.json")
    with open(naming_file, 'w', encoding='utf-8') as f:
        json.dump(naming_data, f, indent=4)

    print(f"Success: Metadata saved to {naming_file}")

if __name__ == "__main__":
    main()