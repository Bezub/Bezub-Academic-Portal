import streamlit as st

home_page = st.Page("Home.py", title="Home", icon="🏠", default=True)
calc_page = st.Page("pages/gpa_calculator.py", title="GPA Calculator", icon="🧮")
trans_page = st.Page("pages/transcript_and_cgpa.py", title="Transcript", icon="📜")
admin_page = st.Page("admin_portal.py", title="Admin Panel", icon="🛡️")

my_pages = [home_page, calc_page, trans_page]

if st.session_state.get("username") == "mememe":
    my_pages.append(admin_page)

pg = st.navigation(my_pages)
pg.run()
