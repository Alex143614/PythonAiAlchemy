# predictor.py
from functools import lru_cache
from transformers import AutoModel
from config import MODEL_NAME


@lru_cache(maxsize=1)
def _load_model():
    """Загружает модель один раз и кэширует."""
    try:
        model = AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True)
        model.eval()
        return model
    except Exception as e:
        raise RuntimeError(f"Не удалось загрузить модель '{MODEL_NAME}': {e}")


def predict_solubility(smiles: str) -> float:
    if not smiles or not smiles.strip():
        raise ValueError("SMILES не может быть пустым")

    model = _load_model()
    try:
        results = model.predict([smiles.strip()])
        # модель возвращает список (батч), берём первый элемент
        value = results[0]
        # на случай, если вернётся tensor или список
        if hasattr(value, "item"):
            value = value.item()
        return float(value)
    except Exception as e:
        raise RuntimeError(f"Ошибка предсказания для SMILES '{smiles}': {e}")