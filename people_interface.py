import os
import time
import people_init
import people_ingest
import people_governance
import people_core
import people_node  # <--- NEW IMPORT

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear()
        print("--- SOVEREIGN TALENT ENGINE (2030) ---")
        print("Host: iMac 12.1 | Substrate: people.db\n")
        
        print(" [1] INITIALIZE  (Wipe & Rebuild World)")
        print(" [2] INGEST      (Docs, Emails, LinkedIn)")
        print(" [3] GOVERN      (Import/Export COA)")
        print(" [4] HEAL        (Force Identity Merge)")
        print(" [5] HUNTER      (Verify Targets)")  # <--- NEW OPTION
        print(" [Q] QUIT")
        
        choice = input("\nCommand > ").upper().strip()
        
        if choice == '1':
            confirm = input("Are you sure? This deletes people.db (Y/N): ")
            if confirm.upper() == 'Y':
                people_init.initialize_world()
                input("\nPress Enter...")
        
        elif choice == '2':
            path = input("Enter Path (File or Folder): ").strip()
            people_ingest.router(path)
            people_core.self_heal_network()
            input("\nPress Enter...")
            
        elif choice == '3':
            people_governance.main_menu()
            
        elif choice == '4':
            people_core.self_heal_network()
            input("\nPress Enter...")

        elif choice == '5':         # <--- NEW LOGIC
            people_node.start_hunt()
            input("\nPress Enter...")
            
        elif choice == 'Q':
            print("System Offline.")
            break

if __name__ == "__main__":
    main()
