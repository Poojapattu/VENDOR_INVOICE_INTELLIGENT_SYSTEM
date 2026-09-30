from __future__ import annotations

from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestRegressor

from .config import (
    FREIGHT_FEATURE_ORDER,
    FREIGHT_MODEL_PATH,
    RISK_FEATURE_ORDER,
    RISK_MODEL_PATH,
)


class MLService:
    def __init__(self) -> None:
        self.freight_model: Any = None
        self.risk_model: Any = None
        self.freight_source = "fallback"
        self.risk_source = "fallback"
        self._load_existing_models()
        self._build_fallback_models()

    def _load_existing_models(self) -> None:
        if FREIGHT_MODEL_PATH.exists():
            try:
                self.freight_model = joblib.load(FREIGHT_MODEL_PATH)
                self.freight_source = "existing pickle"
            except Exception as exc:
                print(f"Could not load freight model: {exc}")

        if RISK_MODEL_PATH.exists():
            try:
                self.risk_model = joblib.load(RISK_MODEL_PATH)
                self.risk_source = "existing pickle"
            except Exception as exc:
                print(f"Could not load risk model: {exc}")

    def _build_fallback_models(self) -> None:
        rng = np.random.default_rng(42)
        n = 700
        df = pd.DataFrame({
            "invoice_quantity": rng.integers(1, 1000, n),
            "invoice_dollars": rng.uniform(500, 50000, n),
            "days_po_to_invoice": rng.integers(0, 30, n),
            "days_to_pay": rng.integers(1, 90, n),
            "total_brands": rng.integers(1, 15, n),
            "item_quantity": rng.integers(1, 1500, n),
            "receiving_delay": rng.integers(0, 20, n),
        })

        freight = (
            45
            + df["invoice_quantity"] * 0.18
            + df["invoice_dollars"] * 0.018
            + df["item_quantity"] * 0.05
            + df["receiving_delay"] * 4
            + rng.normal(0, 35, n)
        ).clip(lower=20)

        if self.freight_model is None:
            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1,
                max_depth=12,
            )
            model.fit(df[FREIGHT_FEATURE_ORDER], freight)
            self.freight_model = model

        if self.risk_model is None:
            model = IsolationForest(
                n_estimators=150,
                contamination=0.10,
                random_state=42,
            )
            model.fit(df[RISK_FEATURE_ORDER])
            self.risk_model = model

    @staticmethod
    def _frame(payload: dict, order: list[str]) -> pd.DataFrame:
        return pd.DataFrame([{key: float(payload[key]) for key in order}])

    def predict_freight(self, payload: dict) -> float:
        X = self._frame(payload, FREIGHT_FEATURE_ORDER)
        value = self.freight_model.predict(X)[0]
        return float(max(0.0, value))

    def predict_risk(self, payload: dict) -> tuple[str, float]:
        X = self._frame(payload, RISK_FEATURE_ORDER)
        model = self.risk_model
        prediction = model.predict(X)[0]

        # IsolationForest: -1 = anomaly, 1 = normal.
        if prediction in (-1, 1):
            try:
                raw = float(model.decision_function(X)[0])
                score = float(np.clip(50 - raw * 100, 0, 100))
            except Exception:
                score = 85.0 if prediction == -1 else 15.0
            label = "High Risk" if prediction == -1 else "Low Risk"
            return label, score

        label = "High Risk" if int(prediction) == 1 else "Low Risk"
        score = 50.0

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X)[0]
            classes = list(getattr(model, "classes_", []))
            if 1 in classes:
                score = float(probabilities[classes.index(1)] * 100)
            else:
                score = float(max(probabilities) * 100)

        return label, score

    @property
    def model_source(self) -> str:
        if self.freight_source == "existing pickle" and self.risk_source == "existing pickle":
            return "existing pickle models"
        if self.freight_source == "existing pickle":
            return "freight pickle + fallback risk model"
        if self.risk_source == "existing pickle":
            return "risk pickle + fallback freight model"
        return "fallback models"


ml_service = MLService()
