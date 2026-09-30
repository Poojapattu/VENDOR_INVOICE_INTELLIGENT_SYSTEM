
import { useEffect, useState } from "react";
import {
  AlertTriangle,
  BarChart3,
  CheckCircle2,
  Clock3,
  Package,
  RefreshCcw,
  ShieldCheck,
  Truck
} from "lucide-react";

const API = "http://127.0.0.1:8000";

const initialForm = {
  invoice_quantity: 100,
  invoice_dollars: 18500,
  days_po_to_invoice: 5,
  days_to_pay: 30,
  total_brands: 4,
  item_quantity: 120,
  receiving_delay: 2
};

function Field({ label, name, value, onChange, icon: Icon }) {
  return (
    <label className="field">
      <span><Icon size={14} />{label}</span>
      <input
        type="number"
        min="0"
        step="any"
        value={value}
        onChange={(e) => onChange(name, Number(e.target.value))}
      />
    </label>
  );
}

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [online, setOnline] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/health`)
      .then((r) => r.ok && setOnline(true))
      .catch(() => setOnline(false));
  }, []);

  const update = (name, value) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const analyze = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });

      if (!response.ok) throw new Error("Analysis failed");

      const data = await response.json();
      setResult(data);
      setOnline(true);
    } catch {
      setOnline(false);
      alert("Backend is not running. Start it using python run.py");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setForm(initialForm);
    setResult(null);
  };

  const highRisk = result?.risk_label === "High Risk";
  const mediumRisk = result && result.risk_score >= 50 && !highRisk;

  const riskClass = highRisk ? "high" : mediumRisk ? "medium" : "low";

  return (
    <div className="page">
      <header className="header">
        <div className="brand">
          <div className="logo"><Truck size={22} /></div>
          <div>
            <h1>Invoice Intelligence</h1>
            <p>Freight prediction & invoice risk analysis</p>
          </div>
        </div>

        <div className="header-actions">
          <span className={`connection ${online ? "online" : ""}`}>
            <span />
            {online ? "Model Online" : "API Offline"}
          </span>
          <button className="reset" onClick={reset}>
            <RefreshCcw size={15} />
            Reset
          </button>
        </div>
      </header>

      <main>
        <section className="intro">
          <div>
            <p className="label">INVOICE ANALYSIS</p>
            <h2>Analyze an invoice</h2>
            <p className="description">
              Enter the invoice details below to predict freight cost and
              identify unusual invoice patterns.
            </p>
          </div>
        </section>

        <section className="layout">
          <div className="card input-card">
            <div className="card-title">
              <div>
                <p className="label">INPUT DETAILS</p>
                <h3>Invoice information</h3>
              </div>
              <Package size={20} />
            </div>

            <div className="fields">
              <Field label="Invoice Quantity" name="invoice_quantity"
                value={form.invoice_quantity} onChange={update} icon={Package} />
              <Field label="Invoice Dollars" name="invoice_dollars"
                value={form.invoice_dollars} onChange={update} icon={BarChart3} />
              <Field label="Days PO to Invoice" name="days_po_to_invoice"
                value={form.days_po_to_invoice} onChange={update} icon={Clock3} />
              <Field label="Days to Pay" name="days_to_pay"
                value={form.days_to_pay} onChange={update} icon={Clock3} />
              <Field label="Total Brands" name="total_brands"
                value={form.total_brands} onChange={update} icon={BarChart3} />
              <Field label="Item Quantity" name="item_quantity"
                value={form.item_quantity} onChange={update} icon={Package} />
              <Field label="Receiving Delay" name="receiving_delay"
                value={form.receiving_delay} onChange={update} icon={Clock3} />
            </div>

            <button className="analyze" onClick={analyze} disabled={loading}>
              {loading ? "Analyzing invoice..." : "Analyze Invoice"}
            </button>
          </div>

          <div className="results">
            <div className="card summary">
              <p className="label">ANALYSIS RESULT</p>
              <h3>Invoice overview</h3>

              <div className="stats">
                <div>
                  <span>Invoice Value</span>
                  <strong>${Number(form.invoice_dollars).toLocaleString()}</strong>
                </div>
                <div>
                  <span>Predicted Freight</span>
                  <strong>
                    {result ? `$${result.predicted_freight.toLocaleString(undefined, { maximumFractionDigits: 2 })}` : "—"}
                  </strong>
                </div>
                <div>
                  <span>Freight Ratio</span>
                  <strong>{result ? `${result.freight_ratio.toFixed(1)}%` : "—"}</strong>
                </div>
              </div>
            </div>

            <div className={`card risk ${result ? riskClass : ""}`}>
              <div className="risk-top">
                <div>
                  <p className="label">RISK ASSESSMENT</p>
                  <h3>Invoice risk</h3>
                </div>
                {result && (
                  highRisk
                    ? <AlertTriangle className="risk-icon" size={28} />
                    : <CheckCircle2 className="risk-icon" size={28} />
                )}
              </div>

              {result ? (
                <>
                  <div className="risk-result">
                    <div className="risk-status">
                      {highRisk ? "HIGH RISK" : mediumRisk ? "REVIEW" : "LOW RISK"}
                    </div>
                    <div className="score">
                      <strong>{result.risk_score.toFixed(0)}</strong>
                      <span>/ 100</span>
                    </div>
                  </div>

                  <div className="risk-bar">
                    <div
                      style={{ width: `${Math.min(result.risk_score, 100)}%` }}
                    />
                  </div>

                  <p className="reason">{result.risk_reason}</p>
                </>
              ) : (
                <div className="waiting">
                  <ShieldCheck size={32} />
                  <span>Run the analysis to see the invoice risk.</span>
                </div>
              )}
            </div>

            {result && (
              <div className="card insights">
                <div className="card-title">
                  <div>
                    <p className="label">BUSINESS INSIGHTS</p>
                    <h3>What should you check?</h3>
                  </div>
                  <ShieldCheck size={20} />
                </div>

                <div className="insights-list">
                  {result.business_insights.map((item, index) => (
                    <div className="insight" key={index}>
                      <CheckCircle2 size={16} />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>

                <div className="checks">
                  <div>
                    <span>PO → Invoice</span>
                    <strong>{form.days_po_to_invoice} days</strong>
                  </div>
                  <div>
                    <span>Payment</span>
                    <strong>{form.days_to_pay} days</strong>
                  </div>
                  <div>
                    <span>Receiving</span>
                    <strong>{form.receiving_delay} days</strong>
                  </div>
                  <div>
                    <span>Brands</span>
                    <strong>{form.total_brands}</strong>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        <footer>
          Invoice Intelligence System • React + FastAPI + Machine Learning
        </footer>
      </main>
    </div>
  );
}
