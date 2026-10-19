# molecule.py
from dataclasses import dataclass, field
from typing import Optional
from rdkit import Chem


@dataclass
class Molecule:
    name: str
    formula: str
    smiles: str
    predictions: dict = field(default_factory=dict)  # {property_name: value}

    def post_init(self):
        self.smiles = self.smiles.strip()


def validate_smiles(smiles: str) -> tuple[bool, Optional[str], Optional[str]]:
    if not smiles or not smiles.strip():
        return False, None, "SMILES пустая"
    try:
        mol = Chem.MolFromSmiles(smiles.strip())
        if mol is None:
            return False, None, f"RDKit не смог распарсить SMILES: '{smiles}'"
        canonical = Chem.MolToSmiles(mol, canonical=True)
        return True, canonical, None
    except Exception as e:
        return False, None, f"Ошибка валидации SMILES: {e}"