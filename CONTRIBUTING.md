# Contributing Guidelines

Thank you for contributing to the Database Platform Utility & DataOps toolkit.

## Target Engines
Contributions are welcome for the supported database platforms:
- PostgreSQL
- Microsoft SQL Server
- Oracle Database
- MySQL / MariaDB
- Pivotal Greenplum / Cloudberry

## Submission Standards
1. **Idempotence**: Administrative and metadata extraction scripts should be safe to run against production and staging environments without destructive side effects.
2. **Dialect Integrity**: Keep dialect-specific syntax in its appropriate directory (`postgresql/`, `mssql/`, `oracle/`, `mysql/`, `greenplum/`).
3. **Documentation**: Scripts should include inline comments describing prerequisites, required database privileges, and expected schema outputs.
