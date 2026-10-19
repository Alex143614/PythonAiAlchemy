# analyzer.py
from molecule import Molecule, validate_smiles
from predictor import predict_solubility
from config import PROPERTY_NAME


def analyze_molecule(mol: Molecule) -> Molecule:
    """Предсказывает свойство для одной молекулы, сохраняет в mol.predictions."""
    ok, canonical, err = validate_smiles(mol.smiles)
    if not ok:
        raise ValueError(f"[{mol.name}] {err}")
    mol.smiles = canonical
    try:
        value = predict_solubility(canonical)
        mol.predictions[PROPERTY_NAME] = round(value, 4)
    except RuntimeError as e:
        raise RuntimeError(f"[{mol.name}] {e}")
    return mol


def analyze_all(molecules: list[Molecule]) -> list[Molecule]:
    """Анализирует все молекулы, пропуская ошибочные."""
    results = []
    for mol in molecules:
        try:
            results.append(analyze_molecule(mol))
            print(f"[OK] {mol.name}: {mol.predictions.get(PROPERTY_NAME)}")
        except (ValueError, RuntimeError) as e:
            print(f"[ERR] {e}")
    return results


def sort_by_property(molecules: list[Molecule], reverse: bool = False) -> list[Molecule]:
    """Сортировка по предсказанному свойству."""
    return sorted(
        molecules,
        key=lambda m: m.predictions.get(PROPERTY_NAME, float("inf")),
        reverse=reverse,
    )


def find_by_name(molecules: list[Molecule], query: str) -> list[Molecule]:
    """Поиск по названию (регистронезависимый, частичное совпадение)."""
    q = query.strip().lower()
    return [m for m in molecules if q in m.name.lower()]


def compare(molecules: list[Molecule], names: list[str]) -> list[Molecule]:
    """Сравнение нескольких соединений по имени."""
    wanted = {n.strip().lower() for n in names}
    return [m for m in molecules if m.name.lower() in wanted]