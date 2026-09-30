
# Invoice Intelligence — Simple React + FastAPI Version

A clean, simple React frontend with a Python FastAPI backend for:

- Freight cost prediction
- Invoice risk detection
- Business insights

## Run backend

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Backend: http://127.0.0.1:8000

## Run frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Use your real trained models

Copy:

```text
best_freight_model.pkl
invoice_risk_flagging_model.pkl
```

into:

```text
backend/models/
```

The backend loads them automatically.

If they are not present, fallback models are generated so the app can still run for UI/API testing.

## Input fields

1. Invoice Quantity
2. Invoice Dollars
3. Days PO to Invoice
4. Days to Pay
5. Total Brands
6. Item Quantity
7. Receiving Delay

## Main output

The dashboard shows:

- Invoice Value
- Predicted Freight
- Freight Ratio
- Risk Level
- Risk Score / 100
- Reason for the risk result
- Business insights
- Operational checks
- <img width="1611" height="800" alt="image" src="https://github.com/user-attachments/assets/4df42ad4-1355-4628-aed0-584da03b3f47" />

