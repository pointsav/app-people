# Host Authority: Sovereign-Talent-Engine
# Location: iMac 12.1 Host (i5-2400S)

## I. System Initialization
- **host_init_db.py**: Architects the 'people.db' SQLite substrate. Creates relational tables for Entities, Affiliations (Elastic Bonds), and Metadata logs.
- **host_init_coa.py**: Initializes the 'Chart of Archetypes' (COA). Defines the 20-point Digital Twin labels and weights.

## II. Data Ingestion & Provenance
- **host_extract_main.py**: Primary intake for high-volume Personnel spreadsheets. Assigns Sovereign IDs and Personnel attribution.
- **host_extract_linkedin.py**: Specialized intake for "Connections.csv" exports, mapping external fields to internal 20-point weights.

## III. Network & Intelligence Governance
- **host_bridge_api.py**: Mission control gateway. Manages the priority queue for Nodes based on 'Information Gain' needs.
- **host_audit_stats.py**: Stakeholder dashboard. Reports on substrate volume, maturation rates, and global system health.
