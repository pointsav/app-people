import sqlite3
import os
import people_core as core

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def get_context(cursor, sov_id):
    """Fetches the most recent 'Evidence'."""
    try:
        cursor.execute("SELECT details FROM metadata_logs WHERE details LIKE ? ORDER BY id DESC LIMIT 1", (f"{sov_id}%",))
        result = cursor.fetchone()
        return result[0].split(' :: ')[-1] if result else "No Context"
    except: return "No Context"

def menu_select(options, prompt):
    """Generic CLI Menu Selector."""
    print(f"\n  --- {prompt} ---")
    for idx, opt in enumerate(options, 1):
        print(f"  [{idx}] {opt}")
    
    while True:
        try:
            choice = input("\n  Select # > ").strip()
            if not choice: return None # Skip
            idx = int(choice) - 1
            if 0 <= idx < len(options): return options[idx]
        except: pass

def start_hunt():
    conn = sqlite3.connect(core.DB_NAME)
    cursor = conn.cursor()
    
    # 1. Fetch Discovery Queue
    cursor.execute("SELECT sovereign_id, display_name FROM entities WHERE status = 'Discovery'")
    targets = cursor.fetchall()
    
    if not targets:
        print("\n  [All Clear] No targets pending verification.")
        conn.close()
        return

    # Pre-fetch Menus (Cache)
    archetypes_raw = core.get_archetypes()
    archetypes = [a[1] for a in archetypes_raw]
    domains = core.get_domains()
    
    print(f"\n--- HUNTER PROTOCOL ACTIVATED ({len(targets)} Targets) ---")
    
    for sov_id, name in targets:
        clear()
        context = get_context(cursor, sov_id)
        
        print("-" * 60)
        print(f"TARGET: {name}")
        print(f"PROOF:  {context}")
        print("-" * 60)
        
        # --- Q1: IDENTITY (The Gate) ---
        print("\n[Q1] IDENTITY MATCH?")
        action = input("  [ENTER]=Verify | [X]=Burn | [S]=Skip > ").lower().strip()
        
        if action == 'x':
            cursor.execute("UPDATE entities SET status = 'Burned' WHERE sovereign_id = ?", (sov_id,))
            print("  [x] Burned.")
            continue
        elif action == 's':
            print("  [~] Skipped.")
            continue
        
        # --- Q2: DOMAIN (The Geography) ---
        domain = menu_select(domains, "Q2: PRIMARY DOMAIN")
        
        # --- Q3: ARCHETYPE (The Pulse) ---
        primary = menu_select(archetypes, "Q3: PRIMARY ARCHETYPE")
        
        # --- Q4: SHADOW (The Nuance) ---
        # Filter out the primary choice to avoid duplicates
        shadow_opts = [a for a in archetypes if a != primary]
        secondary = menu_select(shadow_opts, "Q4: SECONDARY ARCHETYPE (SHADOW)")
        
        # --- Q5: EDGE (The Network) ---
        print("\n  --- Q5: AFFILIATION (The Edge) ---")
        edge = input("  Who is this person connected to? (Name/Company) > ").strip()
        
        # --- COMMIT THE TWIN ---
        # 1. Update Status
        cursor.execute("UPDATE entities SET status = 'Verified' WHERE sovereign_id = ?", (sov_id,))
        
        # 2. Log the Digital Twin Profile
        profile_str = f"Domain:{domain} | Pulse:{primary} | Shadow:{secondary} | Connected:{edge}"
        core.log_action('NODE_MATURE', f"{sov_id} :: {profile_str}")
        
        # 3. Create the Edge (if provided)
        if edge:
            core.ingest_signal(edge, 'entity_name', f"Edge from {name}", 'people_node')
            
        conn.commit()
        print(f"\n  [+] Target {name} Fully Maturated.")
        input("  Press Enter for next target...")

    conn.close()
    print("\n--- HUNT COMPLETE ---")
