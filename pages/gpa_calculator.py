import streamlit as st
import pandas as pd
import datetime
from database import supabase, check_auth, apply_custom_design

apply_custom_design()

st.set_page_config(page_title="GPA Calculator", layout="wide")

# This stops the page if not logged in
if "Home" not in st.session_state:
    check_auth()

# Use the logged-in name automatically
username = st.session_state.username


def gfec(score):
    if score >= 85:
        return 4.0
    elif score >= 80:
        return 3.75
    elif score >= 75:
        return 3.5
    elif score >= 68:
        return 3.0
    elif score >= 65:
        return 2.75
    elif score >= 60:
        return 2.5
    elif score >= 50:
        return 2.0
    elif score >= 45:
        return 1.75
    elif score >= 40:
        return 1.0
    else:
        return 0.0


st.header("Semester GPA Calculator")

# Error Handling for input
num_courses = st.number_input("Number of courses", min_value=1, max_value=15, value=5)

data = []
for i in range(int(num_courses)):
    with st.expander(f"Course {i + 1}", expanded=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        title = c1.text_input("Course Title", key=f"t{i}", placeholder="e.g. Discrete Math")
        score = c2.number_input(
            "Score", min_value=0.0, max_value=100.0, value=None,
            placeholder="e.g. 85", key=f"s{i}"
        )
        ects = c3.number_input("ECTS", 1, 20, key=f"e{i}")
        score_val = score if score is not None else 0.0
        data.append({"Title": title, "Score": score_val, "ECTS": ects, "Point": gfec(score_val)})

if st.button("Calculate GPA"):
    df = pd.DataFrame(data)
    total_points = (df["Point"] * df["ECTS"]).sum()
    total_ects = df["ECTS"].sum()
    gpa = round(total_points / total_ects, 2) if total_ects > 0 else 0

    st.session_state.current_gpa = gpa
    st.session_state.current_ects = total_ects

    st.divider()
    st.subheader("Results")
    st.table(df[["Title", "Score", "ECTS", "Point"]])
    st.success(f"Final Semester GPA: {gpa:.2f}")

st.divider()
st.subheader("💾 Save My Progress")

if st.button("Confirm and Save"):
    if "current_gpa" not in st.session_state:
        st.error("Please calculate your GPA first!")
    else:
        with st.spinner("Checking for duplicate records..."):
            today = str(datetime.date.today())

            # Check if this user already saved a record today
            existing = supabase.table("gpa_records") \
                .select("*") \
                .eq("username", username) \
                .eq("created_at", today) \
                .execute()

            if existing.data:
                st.warning(f"⚠️ You have already saved a GPA record for today ({today}).")
                st.info(
                    "To avoid duplicate entries, you can only save one record per day. If this was a mistake, contact your admin.")
            else:
                try:
                    clean_gpa = float(st.session_state.current_gpa)
                    clean_ects = int(st.session_state.current_ects)

                    supabase.table("gpa_records").insert({
                        "username": username,  # Locked to logged-in user
                        "gpa": clean_gpa,
                        "total_ects": clean_ects,
                        "created_at": today
                    }).execute()

                    st.success(f"✅ Successfully saved to the cloud for {username}!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error saving data: {e}")

st.markdown(
    "<p style='text-align: center; color: #4A148C; font-size: 12px; margin-top: 50px; opacity: 0.6;'>© 2026 Bezub Academic Systems.</p>",
    unsafe_allow_html=True)
