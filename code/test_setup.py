from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"


def test_repository_structure():
    assert (ROOT / "README.md").exists()
    assert (ROOT / "problem_statement.md").exists()
    assert (ROOT / "AGENTS.md").exists()
    assert DATASET.exists()