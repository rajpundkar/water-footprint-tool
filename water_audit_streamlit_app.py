
import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64

st.set_page_config(page_title="💧 Water Footprint Audit Tool", layout="centered")

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Industrial Water Footprint Audit Tool")
st.subheader("🌍 Empowering Sustainable Practices through Smart Water Monitoring")

st.info("Adjust the sliders below to estimate your facility's water usage across daily operations.")

# User Inputs
col1, col2, col3 = st.columns(3)
with col1:
    cleaning = st.slider("🧼 Cleaning Units per Day", 0, 100, 10)
with col2:
    cooling = st.slider("❄️ Cooling Cycles per Day", 0, 50, 5)
with col3:
    batches = st.slider("🏭 Production Batches per Day", 0, 100, 20)

# Calculations
usage = {
    "Cleaning": cleaning * 10,
    "Cooling": cooling * 20,
    "Production": batches * 15
}
usage["Total"] = sum(usage.values())

# Display summary
st.markdown("---")
st.subheader("📊 Estimated Water Usage Breakdown (Litres/Day)")
st.metric("Cleaning", f"{usage['Cleaning']} L")
st.metric("Cooling", f"{usage['Cooling']} L")
st.metric("Production", f"{usage['Production']} L")
st.metric("💧 Total Usage", f"{usage['Total']} L")

st.markdown("### 📈 Visual Representation")
fig, ax = plt.subplots()
labels = [k for k in usage.keys() if k != "Total"]
values = [usage[k] for k in labels]
ax.bar(labels, values, color=["#3498db", "#2ecc71", "#e74c3c"])
ax.set_ylabel("Litres")
ax.set_title("Water Usage per Activity")
st.pyplot(fig)


# PDF report generator
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Water Footprint Audit Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    for k, v in data.items():
        pdf.cell(200, 10, txt=f"{k}: {v} Litres", ln=True)
    pdf_file = "Water_Audit_Report.pdf"
    pdf.output(pdf_file)
    return pdf_file

if st.button("📄 Generate PDF Report"):
    pdf_path = create_pdf(usage)
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="Water_Audit_Report.pdf">📥 Click here to download your report</a>'
        st.markdown(href, unsafe_allow_html=True)
