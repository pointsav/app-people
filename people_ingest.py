import os
import pandas as pd
import PyPDF2
from docx import Document
import email
from email import policy
import people_core as core # The Brain

def process_linkedin(path):
    print(f"  [LinkedIn Mode] Parsing {path}...")
    # Specialized Logic for LinkedIn Connections
    try:
        df = pd.read_csv(path, skiprows=3) # Standard LinkedIn skip
        count = 0
        for _, row in df.iterrows():
            # LinkedIn Mapping
            fname = str(row.get('First Name', ''))
            lname = str(row.get('Last Name', ''))
            full_name = f"{fname} {lname}".strip()
            email_addr = str(row.get('Email Address', ''))
            company = str(row.get('Company', ''))
            
            # Ingest Name
            if full_name:
                core.ingest_signal(full_name, 'entity_name', 'LinkedIn Export', 'people_ingest')
                count += 1
            # Ingest Email
            if '@' in email_addr:
                core.ingest_signal(email_addr, 'email', f"LinkedIn: {full_name}", 'people_ingest')
                count += 1
            # Ingest Company
            if company and len(company) > 2:
                core.ingest_signal(company, 'entity_name', f"LinkedIn Employer: {full_name}", 'people_ingest')
                count += 1
        print(f"  [+] Extracted {count} signals from Graph.")
    except Exception as e:
        print(f"  [!] LinkedIn Error: {e}")

def process_document(path):
    print(f"  [Gravity Mode] Scanning {os.path.basename(path)}...")
    text = ""
    ext = path.lower().split('.')[-1]
    
    try:
        if ext == 'pdf':
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages: text += page.extract_text() + "\n"
        elif ext == 'docx':
            doc = Document(path)
            for para in doc.paragraphs: text += para.text + "\n"
        
        # Run Core Gravity
        signals = 0
        for line in text.split('\n'):
            line = line.strip()
            if not line: continue
            
            emails = core.EMAIL_REGEX.findall(line)
            if emails:
                for e in emails:
                    if core.ingest_signal(e, 'email', f"Doc: {os.path.basename(path)}", 'people_ingest'):
                        signals += 1
            elif core.calculate_gravity(line):
                if core.ingest_signal(line, 'entity_name', f"Doc: {os.path.basename(path)}", 'people_ingest'):
                    signals += 1
        print(f"  [+] Mined {signals} signals.")
    except Exception as e:
        print(f"  [!] Doc Error: {e}")

def process_maildir(path):
    print(f"  [Deep Miner] Crawling Maildir {path}...")
    count = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                with open(os.path.join(root, f), 'rb') as f_obj:
                    msg = email.message_from_binary_file(f_obj, policy=policy.default)
                    subject = str(msg.get('Subject', 'No Subject'))
                    sender = str(msg.get('From', ''))
                    
                    # Mine Header
                    for e in core.EMAIL_REGEX.findall(sender):
                        core.ingest_signal(e, 'email', f"Header: {subject[:30]}", 'people_ingest')
                        count += 1
                    
                    # Mine Body (Simplified Text Extract)
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body += part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    # Gravity Scan on Body
                    if body:
                        for line in body.split('\n'):
                            if core.calculate_gravity(line):
                                core.ingest_signal(line, 'entity_name', f"Email Body: {subject[:30]}", 'people_ingest')
                                count += 1
            except: continue
    print(f"  [+] Mined {count} signals from Correspondence.")

def router(target_path):
    if os.path.isdir(target_path):
        # Assume Maildir if directory
        process_maildir(target_path)
    elif os.path.isfile(target_path):
        fname = os.path.basename(target_path).lower()
        if 'connections.csv' in fname:
            process_linkedin(target_path)
        elif fname.endswith(('.pdf', '.docx')):
            process_document(target_path)
        elif fname.endswith('.csv') or fname.endswith('.xlsx'):
            print("  [Universal Spreadsheet] Logic would go here (using pandas)...")
    else:
        print("  [!] Invalid Path.")
