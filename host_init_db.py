# =================================================================
# PROJECT: Sovereign-Talent-Engine
# REPOSITORY: github.com/pwoodfine/Sovereign-Talent-Engine
# OWNER: PointSav Digital Systems AG ("PointSav Digital Systems")
# CUSTOMER: Woodfine Management Corp. ("MCorp")
# LICENSE: Apache 2.0 with Sovereign Addendum / Functional Access License
# -----------------------------------------------------------------
# DESCRIPTION: Initializes the structural Geography (COA) and the 
# Dynamic Pulse (Self-Healing Archetypes) for the talent ecosystem.
# TARGET HARDWARE: iMac 12.1 (Intel Core i5-2400S)
# =================================================================

import sqlite3
import os
import sys

DB_NAME = "sovereign_talent.db"

def initialize_engine():
    print(f"[*] Initializing Sovereign-Talent-Engine for PointSav Digital Systems...")
    
    if os.path.exists(DB_NAME):
        print(f"[!] Error: {DB_NAME} already exists. Initialization aborted to prevent data loss.")
        sys.exit(1)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. ENFORCE INTEGRITY
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 2. CREATE CHART OF ACCOUNTS (GEOGRAPHY) - ADJUSTABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chart_of_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile TEXT NOT NULL,
            domain TEXT NOT NULL,
            sub_domain TEXT,
            target_archetype_id INTEGER,
            FOREIGN KEY (target_archetype_id) REFERENCES archetypes(id)
        )
    ''')

    # 3. CREATE ARCHETYPES (THE PULSE) - DYNAMIC/SELF-HEALING
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archetypes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            signature_type TEXT NOT NULL,
            healing_trigger TEXT NOT NULL
        )
    ''')

    # 4. CREATE THE PEOPLE (THE TALENT NODE)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            legal_name TEXT NOT NULL,
            github_username TEXT,
            coa_id INTEGER NOT NULL,
            calculated_archetype_id INTEGER,
            last_audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (coa_id) REFERENCES chart_of_accounts(id),
            FOREIGN KEY (calculated_archetype_id) REFERENCES archetypes(id)
        )
    ''')

    # 5. POPULATE ARCHETYPES (The 11 Sovereign States)
    archetypes_data = [
        ('The Executive', 'Strategy Synthesis', 'Administrative Drift'),
        ('The Guardian', 'Risk Verification', 'Safety Frequency Drop'),
        ('The Fiduciary', 'Fiscal Precision', 'Subjective Variance'),
        ('The Architect', 'Systems Design', 'Isolated Task Focus'),
        ('The Engineer', 'Logic/Code/BIM', 'Social/Diplomatic Shift'),
        ('The Artisan', 'Visual Craft', 'Non-Visual/Rigid Logic'),
        ('The Constructor', 'Physical Build', 'Tangible Inactivity'),
        ('The Catalyst', 'Momentum/Deals', 'Velocity Stagnation'),
        ('The Envoy', 'Diplomacy/Public', 'Internal/Isolationist Shift'),
        ('The Steward', 'Maintenance/Logs', 'Strategic Unauthorized Drift'),
        ('The Sage', 'Theory/Research', 'Unverified Data Points')
    ]
    cursor.executemany("INSERT INTO archetypes (name, signature_type, healing_trigger) VALUES (?, ?, ?)", archetypes_data)

    # 6. POPULATE COA (The Geography mapped to Woodfine/MCorp needs)
    coa_data = [
        ('Compliance', 'Counsel', None, 2),
        ('Compliance', 'Accounting', None, 3),
        ('Real Estate', 'Leasing', 'Office/Industrial/Retail', 8),
        ('Real Estate', 'Tenants', 'Office/Industrial/Retail', 10),
        ('Construction', 'Collaborators', 'Architects/Space Planners', 4),
        ('Construction', 'Collaborators', 'Traffic Consultants', 5), # Updated
        ('Construction', 'Collaborators', 'Visualizers', 6), # Updated
        ('Construction', 'Collaborators', 'Civil/Structural Engineers', 5),
        ('Construction', 'Collaborators', 'Landscape Architects', 6),
        ('Construction', 'Trades', None, 7),
        ('IT Support', 'Contributors', 'Software Architect', 4),
        ('IT Support', 'Contributors', 'BIM/DevOps/Backend', 5),
        ('IT Support', 'Contributors', 'UI/UX/Visualizers', 6),
        ('Investor Relations', 'Finance', 'Portfolio Mgrs/Bankers', 3),
        ('Investor Relations', 'Media', 'Politicians/Press', 9),
        ('Personnel', 'Boards', 'Supervisory/Management', 1),
        ('Local Admin', 'Local Support', 'Accountants/Counsel', 3)
    ]
    cursor.executemany("INSERT INTO chart_of_accounts (profile, domain, sub_domain, target_archetype_id) VALUES (?, ?, ?, ?)", coa_data)

    conn.commit()
    conn.close()
    print(f"[+] SUCCESS: {DB_NAME} initialized on Sovereign hardware.")

if __name__ == "__main__":
    initialize_engine()
