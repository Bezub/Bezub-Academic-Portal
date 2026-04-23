import streamlit as st
import pandas as pd
from database import supabase, check_auth, apply_custom_design
from fpdf import FPDF

apply_custom_design()

st.set_page_config(page_title="Academic Transcript", layout="wide")

if "Home" not in st.session_state:
    check_auth()

username = st.session_state.username

st.header("📜 Unofficial Academic Transcript & CGPA")
st.info(f"Welcome back, **{username}**! Your history is retrieved automatically.")

# PDF GENERATOR FUNCTION
def create_pdf(df, user, cgpa):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Title
    pdf.cell(200, 10, txt=f"Unofficial Academic Transcript: {user}", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"Overall CGPA: {round(cgpa, 2)}", ln=True, align='C')
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, "Date", 1)
    pdf.cell(60, 10, "GPA", 1)
    pdf.cell(60, 10, "ECTS", 1)
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", "", 12)
    for index, row in df.iterrows():
        pdf.cell(60, 10, str(row['Date Recorded']), 1)
        pdf.cell(60, 10, str(row['Semester GPA']), 1)
        pdf.cell(60, 10, str(row['Credits (ECTS)']), 1)
        pdf.ln()

    return pdf.output()

# DATA RETRIEVAL (Runs automatically)
with st.spinner("Accessing cloud records..."):
    # Filter strictly by the logged-in username
    response = supabase.table("gpa_records").select("*").eq("username", username).execute()

    if not response.data:
        st.warning(f"Hello {username}, we couldn't find any records yet.")
        st.write("Go to the **GPA Calculator** page to calculate and save your first semester!")
    else:
        df = pd.DataFrame(response.data)
        df['created_at'] = pd.to_datetime(df['created_at']).dt.date

        total_quality_points = (df['gpa'] * df['total_ects']).sum()
        grand_total_ects = df['total_ects'].sum()
        cgpa = round(total_quality_points / grand_total_ects, 2) if grand_total_ects > 0 else 0

        st.divider()

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Cumulative GPA", value=f"{cgpa:.3f}")
        col2.metric(label="Total Credits Earned", value=int(grand_total_ects))
        col3.metric(label="Semesters Recorded", value=len(df))

        st.subheader("Semester Breakdown")

        display_df = df[['created_at', 'gpa', 'total_ects']].sort_values(by='created_at', ascending=False)
        display_df.columns = ['Date Recorded', 'Semester GPA', 'Credits (ECTS)']

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        pdf_data = create_pdf(display_df, username, cgpa).getvalue()
        st.download_button(
            label="📑 Download Unofficial PDF Transcript",
            data=pdf_data,
            file_name=f"{username}_unofficial_transcript.pdf",
            mime="application/pdf"
        )


