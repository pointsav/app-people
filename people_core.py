import sqlite3
import re
import uuid
import os
import warnings

# Silence technical noise
warnings.filterwarnings('ignore')

DB_NAME = "people.db"

# --- UNIVERSAL GRAVITY SETTINGS ---
# The Single Source of Truth for "Noise"
NOISE_PATTERNS = [
    r'^\d+$', r'^\d+%$', r'^Page \d+', r'^http', r'^\W+$',
    r'unsubscribe', r'privacy policy', r'view in browser',
    r'copyright', r'all rights reserved', r'mailing address',
    r'submit a story', r'advertise', r'read more', r'click here',
    r'font-family', r'padding-', r'margin-', r'border-',
    r'received this email', r'opted in', r'send to a friend'
]

# Corporate Markers for Auto-Classification
ORG_SUFFIXES = [
    ' LLC', ' Inc', ' Ltd', ' Corp', ' Group', ' Holdings', ' Partners',
    ' Foundation', ' University', ' Capital', ' Ventures', ' Associates',
    ' Systems', ' Management', ' Advisors', ' Bank', ' Trust', 'LP', 'AG'
]

EMAIL_REGEX = re.compile(r'[^@\s]+@[^@\s]+\.[^@\s]+')

def calculate_gravity(text):
    """
    Universal Math: Is this string a valid Entity?
    Returns: Boolean
    """
    text = text.strip()
    if len(text) < 3 or len(text) > 80: return False
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE): return False
    if not re.search(r'[a-zA-Z]', text): return False
    if text.islower(): return False # Reject lazy text
    return True

def classify_entity(text):
    """
    Decides if a Name is an Organization or Individual based on Suffixes.
    """
    for suffix in ORG_SUFFIXES:
        if suffix.lower() in text.lower():
            return 'Organization'
    return 'Individual'

def ingest_signal(value, signal_type, context, source_module):
    """
    The Universal Socket.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    value = value.strip()
    
    if signal_type == 'email':
        value = value.lower()
        sov_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, value))[:8]
        display_name = value.split('@')[0]
        entity_type = 'Individual'
    else:
        # Named Entity
        sov_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, value.lower()))[:8]
        display_name = value
        entity_type = classify_entity(value)

    try:
        cursor.execute('''
            INSERT INTO entities (sovereign_id, display_name, entity_type, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(sovereign_id) DO UPDATE SET status = status
        ''', (sov_id, display_name, entity_type, 'Discovery'))
        
        details = f"{sov_id} :: Type: {signal_type} | Value: {value} | Context: {context}"
        cursor.execute('''
            INSERT INTO metadata_logs (action, module, details)
            VALUES (?, ?, ?)
        ''', ('SIGNAL_MINED', source_module, details))
        conn.commit()
        return True
    except: 
        return False
    finally:
        conn.close()

def self_heal_network():
    """
    The Merger. Collapses duplicate emails into single Sovereign IDs.
    """
    if not os.path.exists(DB_NAME): return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("\n  [🧠 Core] Running Self-Healing Logic...")
    
    # Merge Logic (Simplified for 2030)
    cursor.execute('''
        SELECT substr(details, instr(details, 'Value: ') + 7, 
               instr(substr(details, instr(details, 'Value: ') + 7), ' |') - 1) as email_val,
               GROUP_CONCAT(DISTINCT substr(details, 1, instr(details, ' ::') - 1)) as ids
        FROM metadata_logs
        WHERE details LIKE '%Type: email%'
        GROUP BY email_val
        HAVING COUNT(DISTINCT substr(details, 1, instr(details, ' ::') - 1)) > 1
    ''')
    
    merges = cursor.fetchall()
    count = 0
    for email, id_list in merges:
        ids = id_list.split(',')
        primary_id = ids[0]
        for dup_id in ids[1:]:
            cursor.execute("UPDATE metadata_logs SET details = REPLACE(details, ?, ?) WHERE details LIKE ?", 
                           (dup_id, primary_id, f"{dup_id}%"))
            cursor.execute("DELETE FROM entities WHERE sovereign_id = ?", (dup_id,))
            count += 1
    
    if count > 0:
        print(f"  [+] Healed {count} fractured identities.")
    
    conn.commit()
    conn.close()
def log_action(action, details):
    """
    Standardized logging for the Hunter Node.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO metadata_logs (action, module, details)
        VALUES (?, ?, ?)
    ''', (action, 'people_node', details))
    conn.commit()
    conn.close()

# --- CORE: MENU FETCHERS ---
def get_archetypes():
    """Returns list of (id, name) for the Hunter Menu."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name FROM archetypes ORDER BY id")
        return cursor.fetchall()
    except: return []
    finally: conn.close()

def get_domains():
    """Returns list of unique Domains for the Hunter Menu."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT domain FROM chart_of_accounts ORDER BY domain")
        return [row[0] for row in cursor.fetchall()]
    except: return []
    finally: conn.close()
