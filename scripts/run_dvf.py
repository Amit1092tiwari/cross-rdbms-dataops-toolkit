#!/usr/bin/env python3
"""
Data Validation Framework (DVF) Batch Runner
Enterprise-grade runner to execute SQL validation tests within CI/CD or Batch (ETL/ELT) pipelines.
Supports: PostgreSQL, MySQL, and SQL Server via database CLI (psql, mysql, sqlcmd) or Python DB-API.
Exit code: 0 = All tests passed, 1 = One or more tests failed.
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime


def run_command(cmd, input_text=None):
    """Executes a shell command and captures stdout/stderr."""
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE if input_text else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )
        stdout, stderr = proc.communicate(input=input_text)
        return proc.returncode, stdout, stderr
    except Exception as exc:
        return 1, "", str(exc)


def execute_postgres(host, port, db, user, password, sql_file):
    """Executes SQL script using psql."""
    env = os.environ.copy()
    if password:
        env["PGPASSWORD"] = password
    cmd = f'psql -h {host} -p {port} -U {user} -d {db} -f "{sql_file}" -A -F "\t"'
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
        env=env,
    )
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout, stderr


def execute_mysql(host, port, db, user, password, sql_file):
    """Executes SQL script using mysql CLI."""
    pass_arg = f"-p{password}" if password else ""
    cmd = f'mysql -h {host} -P {port} -u {user} {pass_arg} {db} --batch < "{sql_file}"'
    return run_command(cmd)


def execute_mssql(host, port, db, user, password, sql_file):
    """Executes SQL script using sqlcmd CLI."""
    server = f"{host},{port}" if port else host
    auth_args = f"-U {user} -P {password}" if user else "-E"
    cmd = f'sqlcmd -S {server} -d {db} {auth_args} -i "{sql_file}" -s "\t" -W'
    return run_command(cmd)


def parse_basic_results(output):
    """
    Parses tab-delimited or tabular output from dv_basic_test_cases.sql.
    Looks for tst_id, status (P/FAIL/WARN/SKIP), and tst_descr.
    """
    passed = []
    failed = []
    warnings = []
    skipped = []

    # Regex matching patterns like "T001\tFAIL\t..." or "T001  FAIL  ..."
    pattern = re.compile(r"^(T\d{3,4})\s*[\t|]\s*(FAIL|P|WARN|SKIP)\s*[\t|]\s*(.*)$", re.MULTILINE)

    for match in pattern.finditer(output):
        tst_id, status, descr = match.groups()
        entry = {"id": tst_id, "status": status, "description": descr.strip()}
        if status == "P":
            passed.append(entry)
        elif status == "FAIL":
            failed.append(entry)
        elif status == "WARN":
            warnings.append(entry)
        elif status == "SKIP":
            skipped.append(entry)

    return passed, failed, warnings, skipped


def main():
    parser = argparse.ArgumentParser(description="Data Validation Framework (DVF) Pipeline Runner")
    parser.add_argument("--platform", required=True, choices=["postgresql", "mysql", "mssql"], help="Target database platform")
    parser.add_argument("--sql-file", required=True, help="Path to SQL validation script (basic or advanced)")
    parser.add_argument("--host", default=os.getenv("DB_HOST", "localhost"), help="Database hostname")
    parser.add_argument("--port", default=os.getenv("DB_PORT", ""), help="Database port")
    parser.add_argument("--db", default=os.getenv("DB_NAME", ""), help="Database name")
    parser.add_argument("--user", default=os.getenv("DB_USER", ""), help="Database username")
    parser.add_argument("--password", default=os.getenv("DB_PASSWORD", ""), help="Database password")
    parser.add_argument("--fail-on-warning", action="store_true", help="Treat WARN status as a failure")

    args = parser.parse_args()

    if not os.path.isfile(args.sql_file):
        print(f"[ERROR] SQL file not found: {args.sql_file}", file=sys.stderr)
        sys.exit(1)

    print(f"[{datetime.now().isoformat()}] Starting DVF Execution on {args.platform} ({args.db})...")

    # Set default ports if omitted
    port = args.port
    if not port:
        port = "5432" if args.platform == "postgresql" else ("3306" if args.platform == "mysql" else "1433")

    if args.platform == "postgresql":
        code, stdout, stderr = execute_postgres(args.host, port, args.db, args.user, args.password, args.sql_file)
    elif args.platform == "mysql":
        code, stdout, stderr = execute_mysql(args.host, port, args.db, args.user, args.password, args.sql_file)
    elif args.platform == "mssql":
        code, stdout, stderr = execute_mssql(args.host, port, args.db, args.user, args.password, args.sql_file)

    if code != 0 and not stdout:
        print(f"[ERROR] Query execution failed with code {code}:\n{stderr}", file=sys.stderr)
        sys.exit(code)

    passed, failed, warnings, skipped = parse_basic_results(stdout)
    total_tests = len(passed) + len(failed) + len(warnings) + len(skipped)

    print("\n" + "=" * 70)
    print("DATA VALIDATION TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests Executed : {total_tests}")
    print(f"Passed               : {len(passed)}")
    print(f"Failed               : {len(failed)}")
    print(f"Warnings             : {len(warnings)}")
    print(f"Skipped              : {len(skipped)}")
    print("=" * 70)

    if failed:
        print("\n[FAILED TESTS DETAILS]")
        for item in failed:
            print(f"  ❌ [{item['id']}] FAIL - {item['description']}")

    if warnings and args.fail_on_warning:
        print("\n[WARNING DETAILS (Treated as Failures)]")
        for item in warnings:
            print(f"  ⚠️ [{item['id']}] WARN - {item['description']}")

    # Exit code determination
    if failed or (warnings and args.fail_on_warning):
        print("\n>>> PIPELINE RESULT: FAILED (Circuit breaker triggered) <<<")
        sys.exit(1)
    else:
        print("\n>>> PIPELINE RESULT: PASSED <<<")
        sys.exit(0)


if __name__ == "__main__":
    main()
