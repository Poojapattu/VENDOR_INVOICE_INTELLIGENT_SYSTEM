from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"

FREIGHT_MODEL_PATH = MODEL_DIR / "best_freight_model.pkl"
RISK_MODEL_PATH = MODEL_DIR / "invoice_risk_flagging_model.pkl"

FEATURE_ORDER = [
    "invoice_quantity",
    "invoice_dollars",
    "days_po_to_invoice",
    "days_to_pay",
    "total_brands",
    "item_quantity",
    "receiving_delay",
]

# Change these if the original pickles were trained in another column order.
FREIGHT_FEATURE_ORDER = FEATURE_ORDER.copy()
RISK_FEATURE_ORDER = FEATURE_ORDER.copy()
