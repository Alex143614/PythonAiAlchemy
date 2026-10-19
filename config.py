# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# CSV с результатами
RESULTS_CSV = OUTPUT_DIR / "chemistry_results.csv"

# Seed-файл с молекулами для анализа
SEED_CSV = DATA_DIR / "molecules_seed.csv"

# Модель Hugging Face (выбрана под растворимость в воде, logS)
MODEL_NAME = "mist-models/mist-28M-kcwb9le5-esol"

# Название предсказываемого свойства
PROPERTY_NAME = "aqueous_solubility_logS"

# Единица измерения (для отображения)
PROPERTY_UNIT = "log mol/L"

# Список свойств (если модель поддерживает несколько)
SUPPORTED_PROPERTIES = [PROPERTY_NAME]