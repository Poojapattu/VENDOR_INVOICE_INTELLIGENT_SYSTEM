from pydantic import BaseModel, Field


class InvoiceInput(BaseModel):
    invoice_quantity: float = Field(..., ge=0)
    invoice_dollars: float = Field(..., ge=0)
    days_po_to_invoice: float = Field(..., ge=0)
    days_to_pay: float = Field(..., ge=0)
    total_brands: float = Field(..., ge=0)
    item_quantity: float = Field(..., ge=0)
    receiving_delay: float = Field(..., ge=0)


class AnalyzeResponse(BaseModel):
    predicted_freight: float
    risk_label: str
    risk_score: float
    risk_reason: str
    freight_ratio: float
    payment_delay_status: str
    receiving_status: str
    business_insights: list[str]
    model_source: str
