# 🏛️ Sovereign-People-Interface (v2030)
**Host:** iMac 12.1 (Linux Mint) | **Substrate:** people.db | **License:** Sovereign Addendum

## 📜 1. Strategic Mandate
The **Sovereign-People-Interface** is a proprietary intelligence platform designed to convert fragmented professional signals into a **Deterministic Personnel Substrate**.

Unlike traditional CRMs that rely on manual entry, this system uses **"Blind Ingest"** and **"Universal Gravity"** to mine raw data (PDFs, Emails, CSVs) without bias. It aggregates these signals into a self-healing SQLite vault (`people.db`), where Human Surveyors (Nodes) apply the final layer of truth using the **20-Point Digital Twin** model.

**Core Philosophy:**
> *"There is no external Source of Truth. The Truth is manufactured by the Sovereign Host."*

---

## 🏗️ 2. The 2030 Architecture
The system has been unified into a single logical environment. It operates on a **Host/Node** model using a shared filesystem.

### **The Substrate (`people.db`)**
The passive, relational vault containing four key tables:
1.  **`entities`**: The immutable Anchors (Sovereign IDs).
2.  **`affiliations`**: The elastic bonds (Relationships).
3.  **`metadata_logs`**: The provenance chain (Evidence).
4.  **`chart_of_accounts`**: The "Physics" of the world (11 Archetypes, 55 Domains).

### **The Modules (The Python Fleet)**
All scripts leverage `people_core.py` for shared logic.

| Script Name | Role | Function |
| :--- | :--- | :--- |
| **`people_interface.py`** | **The Commander** | The master CLI menu. The only script you need to execute. |
| **`people_core.py`** | **The Brain** | Holds "Gravity Math," "Magnet Filters," and "Self-Healing" logic. |
| **`people_init.py`** | **The Architect** | Builds the database and seeds the Chart of Archetypes (COA). |
| **`people_ingest.py`** | **The Harvester** | File-agnostic miner. Detects PDF/Email/CSV and extracts raw signals. |
| **`people_survey.py`** | **The Surveyor** | The "Glance-and-Tap" verification loop for Human Nodes. |
| **`people_governance.py`** | **The Governor** | Manages CSV Import/Export for logic tuning. |

---

## 🕹️ 3. Operational Workflow

### **Phase I: The Host (iMac 12.1)**
*The Host manages the physical files and network permissions.*

**1. Initialization**
Builds the empty world.
```bash
python3 people_interface.py
> Select [1] INITIALIZE
