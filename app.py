import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(
    page_title="Invoice Intelligence System",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

.main{
    background-color:#0f172a;
    color:white;
}

.stButton>button{
    background:linear-gradient(
    to right,
    #7f1dff,
    #06b6d4
    );

    color:white;
    border:none;
    border-radius:10px;
    height:3em;
    width:100%;
    font-size:18px;
    font-weight:bold;
}

.metric-card{
    background-color:#1e293b;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 0px 10px rgba(0,0,0,0.5);
}

</style>
""",unsafe_allow_html=True)

st.title("📊 Invoice Intelligence System")

st.markdown("""
AI-powered freight analytics and invoice
risk flagging dashboard
""")
freight_model = joblib.load(
    r"C:\Users\pooja\OneDrive\Desktop\Data analyst(Pooja)\pooja_portfolio_2026\datascience_proj_SMM\invoive_intell_system_SMM\best_freight_model.pkl"
)

risk_model = joblib.load(
    r"C:\Users\pooja\OneDrive\Desktop\Data analyst(Pooja)\pooja_portfolio_2026\datascience_proj_SMM\invoive_intell_system_SMM\invoice_risk_flagging_model.pkl"
)

st.sidebar.header("Invoice Inputs")

invoice_quantity=st.sidebar.number_input(
    "Invoice Quantity",
    min_value=0.0
)

invoice_dollars=st.sidebar.number_input(
    "Invoice Dollars",
    min_value=0.0
)

days_po_to_invoice=st.sidebar.number_input(
    "Days PO To Invoice",
    min_value=0.0
)

days_to_pay=st.sidebar.number_input(
    "Days To Pay",
    min_value=0.0
)

total_brands=st.sidebar.number_input(
    "Total Brands",
    min_value=0.0
)

total_item_quantity=st.sidebar.number_input(
    "Total Item Quantity",
    min_value=0.0
)

total_item_dollars=st.sidebar.number_input(
    "Total Item Dollars",
    min_value=0.0
)

avg_receiving_delay=st.sidebar.number_input(
    "Average Receiving Delay",
    min_value=0.0
)

if st.sidebar.button("Analyze Invoice"):

    cost_per_unit=invoice_dollars/(invoice_quantity+1)

    freight_input=pd.DataFrame(
        [[
            invoice_quantity,
            invoice_dollars,
            cost_per_unit
        ]],
        columns=[
            'Quantity',
            'Dollars',
            'Cost_Per_Unit'
        ]
    )

    predicted_freight=np.expm1(
        freight_model.predict(freight_input)[0]
    )

    risk_input=pd.DataFrame(
        [[
            invoice_quantity,
            invoice_dollars,
            predicted_freight,
            days_po_to_invoice,
            days_to_pay,
            total_brands,
            total_item_quantity,
            total_item_dollars,
            avg_receiving_delay
        ]],
        columns=[
            'invoice_quantity',
            'invoice_dollars',
            'Freight',
            'days_po_to_invoice',
            'days_to_pay',
            'total_brands',
            'total_item_quantity',
            'total_item_dollars',
            'avg_receiving_delay'
        ]
    )

    risk_prediction=risk_model.predict(
        risk_input
    )[0]

    col1,col2=st.columns(2)

    with col1:

        st.markdown(f'''
        <div class="metric-card">
        <h2>Predicted Freight</h2>
        <h1>${predicted_freight:.2f}</h1>
        </div>
        ''',unsafe_allow_html=True)

    with col2:

        if risk_prediction==-1:

            st.markdown('''
            <div class="metric-card">
            <h2>Risk Status</h2>
            <h1 style="color:red;">
            HIGH RISK
            </h1>
            </div>
            ''',unsafe_allow_html=True)

        else:

            st.markdown('''
            <div class="metric-card">
            <h2>Risk Status</h2>
            <h1 style="color:lightgreen;">
            NORMAL
            </h1>
            </div>
            ''',unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
### 🚀 Features
- Freight Cost Prediction
- Invoice Risk Detection
- SQL Feature Engineering
- Isolation Forest Anomaly Detection
- Machine Learning Analytics
""")