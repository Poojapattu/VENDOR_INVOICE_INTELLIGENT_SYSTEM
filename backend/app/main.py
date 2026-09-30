from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .ml_service import ml_service
from .schemas import AnalyzeResponse, InvoiceInput

app = FastAPI(
    title="Invoice Intelligence API",
    description="FastAPI backend for freight prediction and invoice risk detection.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "invoice-intelligence-api",
        "model_source": ml_service.model_source,
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(invoice: InvoiceInput):
    payload = invoice.model_dump()
    predicted_freight = ml_service.predict_freight(payload)
    risk_label, risk_score = ml_service.predict_risk(payload)

    freight_ratio = (
        predicted_freight / invoice.invoice_dollars * 100
        if invoice.invoice_dollars > 0
        else 0
    )

    payment_delay_status = (
        "Extended payment cycle"
        if invoice.days_to_pay > 45
        else "Normal payment cycle"
    )

    receiving_status = (
        "Receiving delay requires attention"
        if invoice.receiving_delay > 7
        else "Receiving timing looks normal"
    )

    reasons = []
    if invoice.receiving_delay > 7:
        reasons.append("receiving delay is relatively high")
    if invoice.days_po_to_invoice > 15:
        reasons.append("PO-to-invoice processing time is relatively high")
    if invoice.days_to_pay > 45:
        reasons.append("payment cycle is extended")
    if freight_ratio > 10:
        reasons.append("predicted freight represents a relatively high invoice share")

    if risk_label == "High Risk" and not reasons:
        reasons.append("the invoice pattern is outside the model's learned normal range")

    risk_reason = (
        "; ".join(reasons)
        if reasons
        else "No major operational warning was identified from the submitted inputs."
    )

    insights = [
        f"Expected freight is approximately ${predicted_freight:,.2f}.",
        f"Freight represents about {freight_ratio:.1f}% of the invoice value.",
        (
            "Prioritize this invoice for manual review."
            if risk_label == "High Risk"
            else "The submitted invoice pattern appears suitable for normal processing."
        ),
    ]

    if invoice.receiving_delay > 7:
        insights.append("Check receiving records because the receiving delay is elevated.")
    if invoice.total_brands >= 10:
        insights.append("Multiple brands are involved; verify line-item aggregation.")
    if invoice.item_quantity > invoice.invoice_quantity * 1.5:
        insights.append("Item quantity is substantially higher than invoice quantity; verify quantities.")

    return AnalyzeResponse(
        predicted_freight=predicted_freight,
        risk_label=risk_label,
        risk_score=round(risk_score, 1),
        risk_reason=risk_reason,
        freight_ratio=round(freight_ratio, 2),
        payment_delay_status=payment_delay_status,
        receiving_status=receiving_status,
        business_insights=insights,
        model_source=ml_service.model_source,
    )
