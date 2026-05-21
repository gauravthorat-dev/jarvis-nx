from __future__ import annotations

import pickle
from pathlib import Path


class IntentClassifier:
    def __init__(self, model_path: str | Path, vectorizer_path: str | Path) -> None:
        self.model = None
        self.vectorizer = None
        model_path = Path(model_path)
        vectorizer_path = Path(vectorizer_path)
        try:
            with open(model_path, 'rb') as mf:
                self.model = pickle.load(mf)
            with open(vectorizer_path, 'rb') as vf:
                self.vectorizer = pickle.load(vf)
        except Exception:
            self.model = None
            self.vectorizer = None

    def predict(self, text: str) -> str | None:
        if not self.model or not self.vectorizer:
            return None
        try:
            vector = self.vectorizer.transform([text])
            return self.model.predict(vector)[0]
        except Exception:
            return None
