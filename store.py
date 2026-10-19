# store.py
import csv
from pathlib import Path
from config import RESULTS_CSV, SEED_CSV, PROPERTY_NAME
from molecule import Molecule, validate_smiles


RESULT_FIELDS = ["molecule_name", "formula", "smiles", "predicted_property", "predicted_value"]


def load_seed_molecules(path: Path = SEED_CSV) -> list[Molecule]:
    """Читает data/molecules_seed.csv -> список Molecule."""
    if not path.exists():
        raise FileNotFoundError(f"Seed-файл не найден: {path}")

    molecules = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"name", "formula", "smiles"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"В {path} нужны колонки: {required}")

        for i, row in enumerate(reader, start=2):
            smiles = (row.get("smiles") or "").strip()
            ok, canonical, err = validate_smiles(smiles)
            if not ok:
                print(f"[WARN] строка {i} пропущена: {err}")
                continue
            molecules.append(Molecule(
                name=row["name"].strip(),
                formula=row["formula"].strip(),
                smiles=canonical,
            ))
    return molecules


def save_results(molecules: list[Molecule], path: Path = RESULTS_CSV) -> None:
    """Сохраняет результаты в CSV (одна строка = молекула + свойство + значение)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        for mol in molecules:
            for prop, value in mol.predictions.items():
                writer.writerow({
                    "molecule_name": mol.name,
                    "formula": mol.formula,
                    "smiles": mol.smiles,
                    "predicted_property": prop,
                    "predicted_value": value,
                })
    print(f"[OK] Результаты сохранены: {path}")


def load_results(path: Path = RESULTS_CSV) -> list[dict]:
    """Читает CSV результатов -> список словарей."""
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))