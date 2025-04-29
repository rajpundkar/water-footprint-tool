
import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(page_title="Water Footprint Audit Tool", layout="centered")

st.title("🌊 Industrial Water Footprint Audit Tool")

st.markdown("Enter your estimated usage below to calculate your water footprint.")

# Input sliders
cleaning = st.slider("Cleaning Units per day", 0, 100, 10)
cooling = st.slider("Cooling Cycles per day", 0, 50, 5)
batches = st.slider("Production Batches per day", 0, 100, 20)

# Calculation
usage = {
    "cleaning": cleaning * 10,
    "cooling": cooling * 20,
    "production": batches * 15
}
usage["total"] = sum(usage.values())

st.subheader("💧 Water Usage Summary")
st.write(f"Cleaning: {usage['cleaning']} Litres")
st.write(f"Cooling: {usage['cooling']} Litres")
st.write(f"Production: {usage['production']} Litres")
st.write(f"**Total Usage: {usage['total']} Litres**")

# Bar chart
st.subheader("📊 Water Usage Breakdown")
fig, ax = plt.subplots()
ax.bar(["Cleaning", "Cooling", "Production"], 
       [usage["cleaning"], usage["cooling"], usage["production"]],
       color=["#3498db", "#2ecc71", "#e74c3c"])
ax.set_ylabel("Litres")
st.pyplot(fig)

# PDF Report
if st.button("📄 Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Water Footprint Audit Report", ln=True, align='C')
    for k, v in usage.items():
        pdf.cell(200, 10, txt=f"{k.capitalize()}: {v} Litres", ln=True)
    pdf.output("Water_Audit_Report.pdf")
    with open("Water_Audit_Report.pdf", "rb") as f:
        st.download_button("Download Report", f, file_name="Water_Audit_Report.pdf")
