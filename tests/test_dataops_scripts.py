import os
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

ENGINES = ["postgresql", "mssql", "mysql", "oracle", "greenplum"]

def test_engine_directory_structure():
    """Verify that all 5 target relational engines have dedicated script directories."""
    for engine in ENGINES:
        engine_path = REPO_ROOT / engine
        assert engine_path.is_dir(), f"Missing directory for engine: {engine}"

def test_sql_scripts_exist_and_non_empty():
    """Verify that SQL files exist and contain non-trivial SQL logic."""
    sql_files = list(REPO_ROOT.glob("**/*.sql"))
    assert len(sql_files) >= 5, "Expected at least 5 core SQL utility scripts"
    
    for f in sql_files:
        content = f.read_text(encoding="utf-8", errors="ignore").strip()
        assert len(content) > 50, f"SQL file {f.name} is too short or empty"
        assert not content.startswith("ERROR"), f"SQL file {f.name} contains raw error string"

def test_docker_compose_configuration():
    """Verify docker-compose.yml defines postgres and mysql test services."""
    compose_path = REPO_ROOT / "docker-compose.yml"
    assert compose_path.exists(), "docker-compose.yml must be present"
    content = compose_path.read_text(encoding="utf-8")
    assert "postgres:" in content
    assert "mysql:" in content
    assert "5432:5432" in content
    assert "3306:3306" in content

def test_markdown_documentation_integrity():
    """Verify presence of core DataOps documentation manifestos."""
    required_docs = [
        "README.md",
        "data_dictionary_scripts.md",
        "data_validation_scripts.md",
        "schemadiff_scripts.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "LICENSE"
    ]
    for doc in required_docs:
        doc_path = REPO_ROOT / doc
        assert doc_path.exists(), f"Missing essential documentation file: {doc}"
        assert doc_path.stat().st_size > 0, f"Empty documentation file: {doc}"
