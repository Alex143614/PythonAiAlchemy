# main.py
import sys
from config import PROPERTY_NAME, PROPERTY_UNIT
from molecule import Molecule, validate_smiles
from predictor import predict_solubility
from store import load_seed_molecules, save_results, load_results
from analyzer import analyze_all, sort_by_property, find_by_name, compare


def print_molecules(molecules: list[Molecule]) -> None:
    if not molecules:
        print("  (пусто)")
        return
    print(f"  {'#':<3}{'Название':<20}{'Формула':<12}{'SMILES':<28}{PROPERTY_NAME}")
    for i, m in enumerate(molecules, 1):
        val = m.predictions.get(PROPERTY_NAME, "—")
        print(f"  {i:<3}{m.name:<20}{m.formula:<12}{m.smiles:<28}{val}")


def menu_add(molecules: list[Molecule]) -> None:
    print("\n--- Добавление молекулы ---")
    name = input("Название: ").strip()
    formula = input("Формула: ").strip()
    smiles = input("SMILES: ").strip()

    ok, canonical, err = validate_smiles(smiles)
    if not ok:
        print(f"[ERR] {err}")
        return

    mol = Molecule(name=name, formula=formula, smiles=canonical)
    try:
        mol.predictions[PROPERTY_NAME] = round(predict_solubility(canonical), 4)
        molecules.append(mol)
        print(f"[OK] Добавлено: {name} -> {mol.predictions[PROPERTY_NAME]} {PROPERTY_UNIT}")
    except RuntimeError as e:
        print(f"[ERR] {e}")


def menu_analyze_seed(molecules: list[Molecule]) -> None:
    print("\n--- Анализ seed-молекул ---")
    try:
        seed = load_seed_molecules()
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERR] {e}")
        return
    print(f"Загружено {len(seed)} молекул, запускаю прогноз...")
    analyzed = analyze_all(seed)
    molecules.extend(analyzed)
    print(f"[OK] Проанализировано: {len(analyzed)}")


def menu_show(molecules: list[Molecule]) -> None:
    print("\n--- Все молекулы ---")
    print_molecules(molecules)


def menu_save(molecules: list[Molecule]) -> None:
    save_results(molecules)


def menu_sort(molecules: list[Molecule]) -> None:
    order = input("По возрастанию? (y/n, по умолч. y): ").strip().lower()
    reverse = order == "n"
    print_molecules(sort_by_property(molecules, reverse=reverse))


def menu_find(molecules: list[Molecule]) -> None:
    q = input("Часть названия: ").strip()
    print_molecules(find_by_name(molecules, q))


def menu_compare(molecules: list[Molecule]) -> None:
    raw = input("Названия через запятую: ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    found = compare(molecules, names)
    print_molecules(found)
    if len(found) >= 2:
        vals = [m.predictions[PROPERTY_NAME] for m in found if PROPERTY_NAME in m.predictions]
        if vals:
            print(f"  min={min(vals)}, max={max(vals)}, avg={sum(vals)/len(vals):.3f}")


def menu_plot(molecules: list[Molecule]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[ERR] matplotlib не установлен")
        return
    data = [(m.name, m.predictions[PROPERTY_NAME])
            for m in molecules if PROPERTY_NAME in m.predictions]
    if not data:
        print("Нет данных для графика")
        return
    names, vals = zip(*data)
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(names)), vals)
    plt.xticks(range(len(names)), names, rotation=45, ha="right")
    plt.ylabel(f"{PROPERTY_NAME}, {PROPERTY_UNIT}")
    plt.title("Предсказанная растворимость")
    plt.tight_layout()
    plt.show()


def main() -> None:
    molecules: list[Molecule] = []
    print("=== AI Chemistry Lab ===")
    print(f"Модель: {import('config').MODEL_NAME}")
    print(f"Свойство: {PROPERTY_NAME} ({PROPERTY_UNIT})")

    actions = {
        "1": ("Анализ seed-молекул (10+)", menu_analyze_seed),
        "2": ("Добавить молекулу вручную", menu_add),
        "3": ("Показать все молекулы", menu_show),
        "4": ("Сохранить в chemistry_results.csv", menu_save),
        "5": ("Сортировать по свойству", menu_sort),
        "6": ("Найти по названию", menu_find),
        "7": ("Сравнить молекулы", menu_compare),
        "8": ("Построить график", menu_plot),
        "0": ("Выход", None),
    }

    while True:
        print("\n--- Меню ---")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        choice = input("Выбор: ").strip()

        if choice == "0":
            print("Пока!")
            sys.exit(0)
        action = actions.get(choice)
        if not action:
            print("[ERR] Неверный выбор")
            continue
        try:
            action[1](molecules)
        except Exception as e:
            print(f"[ERR] {e}")


if name == "main":
    main()