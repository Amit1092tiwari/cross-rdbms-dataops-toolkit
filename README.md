# Database Platform Utility (`database-platform-utility-000a01bc`)

Production-tested SQL scripts for **MS SQL Server**, **MySQL**, **Oracle**, **PostgreSQL**, and **Greenplum**. Useful utilities for data analysts, data engineers, QA testers, and database administrators.

---

## Quick Navigation

| Database Platform | Data Dictionary | Data Validation | SchemaDiff |
| :--- | :---: | :---: | :---: |
| **PostgreSQL** | [Script](postgresql/data_dictionary/data_dict_dump.sql) | [Tests & Docs](postgresql/data_validation/how_to_use_basic_script.md) | [Diff Script](postgresql/schemadiff/simple_schema_dump.sql) |
| **MySQL** | [Script](mysql/data_dictionary/data_dict_dump.sql) | [Tests & Docs](mysql/data_validation/how_to_use_basic_script.md) | [Diff Script](mysql/schemadiff/simple_schema_dump.sql) |
| **MS SQL Server** | [Script](mssql/data_dictionary/data_dict_dump.sql) | [Tests & Docs](mssql/data_validation/how_to_use_basic_script.md) | [Diff Script](mssql/schemadiff/simple_schema_dump.sql) |
| **Oracle** | [Script](oracle/data_dictionary/data_dict_dump.sql) | [Tests & Docs](oracle/data_validation/how_to_use_basic_script.md) | [Diff Script](oracle/schemadiff/simple_schema_dump.sql) |
| **Greenplum** | [Script](greenplum/data_dictionary/data_dict_dump.sql) | — | [Diff Script](greenplum/schemadiff/simple_schema_dump.sql) |

---

## Core Frameworks & Tools

### 1. [Data Dictionary](data_dictionary_scripts.md)

<img align="right" src="img/02_data_dictionary_in_xl.png" alt="Data Dictionary in Excel" width="300px">

The Data Dictionary script and tutorials enable you to easily document an existing database schema.
- Extracts tables, views, column properties, data types, lengths, precision, nullability, and key constraints.
- Includes table and column descriptions/comments where supported.
- Export directly to Excel or CSV for formatting, searching, filtering, and team documentation baselines.

<br clear="right"/>

### 2. [Data Validation Framework (DVF)](data_validation_scripts.md)

<img align="right" src="img/04_data_validation_scripts.png" alt="Data Validation Framework" width="300px">

A test automation framework providing 66 sample test cases across 9 rule sets:
- **Test Categories**: Row counts, key integrity, heuristic thresholds, date/numeric boundaries, text validation, regular expressions, diff checks, and defect regression.
- **Basic Script**: Executes all 66 validation tests and outputs concise single-line statuses (`PASS`/`FAIL`) for quick verification.
- **Advanced Script**: Pushes results to a tracking table with execution durations, detailed failure reasons, expected vs. actual values, and generated SQL queries to immediately inspect rejected rows.

<br clear="right"/>

### 3. [SchemaDiff](schemadiff_scripts.md)

<img align="right" src="img/01_schemadiff_side_by_side.png" alt="SchemaDiff Side-by-Side" width="300px">

Track database changes over time or between environments:
- Exports consistent metadata snapshots of tables, columns, indexes, and constraints.
- Run snapshots before and after release deployments or compare environments (`DEV` vs `TEST` vs `PROD`) using text diff tools (VS Code, DiffMerge, Beyond Compare).
- Pinpoint unexpected schema drift and eliminate troubleshooting guesswork.

<br clear="right"/>

---

## Operational Architecture & Automation

For comprehensive production deployment patterns, refer to the **[Operational Architecture Guide](docs/OPERATIONAL_ARCHITECTURE.md)**.

| Deployment Target | Recommended Frameworks | Implementation / Runner |
| :--- | :--- | :--- |
| **CI/CD Gating (PR & Deploy)** | **SchemaDiff** (migration drift) + **DVF Basic** (in-memory BVT) | [`.github/workflows/db-ci.yml`](.github/workflows/db-ci.yml) |
| **Batch Ingestion (ETL/ELT)** | **DVF Advanced** (circuit-breaker post-load assertions) | [`scripts/run_dvf.py`](scripts/run_dvf.py) / [`scripts/run_dvf.sh`](scripts/run_dvf.sh) |
| **Daily Schedule (Off-Peak)** | **SchemaDiff** (drift audit) + **DVF Advanced** (full regression) + **Data Dictionary** (catalog sync) | [`.github/workflows/daily-db-audit.yml`](.github/workflows/daily-db-audit.yml) |

---

## Community & Resources

- ⭐️ **Star this repository** if you find these scripts useful!
- 📺 **Video Tutorials:** [DataResearchLabs on YouTube](https://www.youtube.com/channel/UCQciXv3xaBykeUFc04GxSXA)
- 📄 **License:** [Creative Commons Zero (CC0 1.0)](LICENSE)
