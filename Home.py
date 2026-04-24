import streamlit as st
import datetime
from database import supabase, apply_custom_design

st.set_page_config(page_title="Bezub's Academic Portal", layout="wide")
apply_custom_design()

if "username" not in st.session_state:
    st.session_state.username = None


def handle_auth():
    st.title("🔐 Academic Portal")
    choice = st.radio("Select Action:", ["Login", "Register"])
    user = st.text_input("Username").lower().strip()
    pwd = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Create Account"):
            check = supabase.table("users").select("*").eq("username", user).execute()
            if check.data:
                st.error("Username already taken!")
            elif len(user) < 4 or len(pwd) < 4:
                st.error("Username and Password must be at least 4 characters.")
            else:
                supabase.table("users").insert({"username": user, "password": pwd}).execute()
                st.success("Account created! You can now switch to Login.")
    else:
        if st.button("Login"):
            res = supabase.table("users").select("*").eq("username", user).eq("password", pwd).execute()
            if res.data:
                st.session_state.username = user
                st.rerun()
            else:
                st.error("Invalid username or password.")


if not st.session_state.username:
    handle_auth()
    st.stop()

# --- SIDEBAR WITH CONTACT ADMIN ---
with st.sidebar:
    st.success(f"👤 Logged in: **{st.session_state.username}**")

    st.divider()
    st.subheader("✉️ Support & Feedback")
    ticket_msg = st.text_area("Message Admin:", placeholder="Ask a question...", key="home_support")
    if st.button("Submit Ticket"):
        if ticket_msg:
            try:
                supabase.table("tickets").insert({
                    "username": st.session_state.username,
                    "message": ticket_msg,
                    "status": "open"
                }).execute()
                st.toast("Ticket submitted successfully!", icon="🚀")
            except:
                st.error("Ticket system offline. Please email admin@bezub.com")
        else:
            st.warning("Message cannot be empty.")

    # --- SOCIAL SECTION ---
    st.sidebar.divider()
    st.sidebar.subheader("💬 Direct Contact")

    # This HTML creates a clickable Telegram Logo
    telegram_html = """
        <div style="display: flex; align-items: center; gap: 10px;">
            <a href="https://t.me/bezabr9" target="_blank" style="text-decoration: none;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" width="40" height="40" style="border-radius: 50%;">
            </a>
            <span style="font-size: 16px; font-weight: bold;">Telegram</span>
        </div>
    """

    st.sidebar.markdown(telegram_html, unsafe_allow_html=True)

    st.divider()
    if st.button("Logout"):
        st.session_state.username = None
        st.rerun()

# --- LOGGED-IN CONTENT ---
st.title("🎓 Bezub's Academic Portal")

st.markdown(f"""
<div style="background-color: #E1D5F5; padding: 25px; border-radius: 15px; border-left: 8px solid #4A148C; margin-bottom: 20px;">
    <h3 style="color: #4A148C; margin-top: 0;">Welcome back, {st.session_state.username.capitalize()}!</h3>
    <p style="color: #4A148C; font-style: italic; font-size: 18px; margin: 0;">
        "The beautiful thing about learning is that no one can take it away from you." – B.B. King
    </p>
</div>
""", unsafe_allow_html=True)

# Feature Boxes
st.subheader("Your Academic Suite")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """<div style="background-color: white; padding: 20px; border-radius: 10px; height: 190px; border: 1px solid #E1D5F5; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);"><h4 style="color: #4A148C;">🧮 Fast GPA</h4><p style="color: #666; font-size: 14px;">Input grades and credits for instant semester calculation.</p></div>""",
        unsafe_allow_html=True)
with col2:
    st.markdown(
        """<div style="background-color: white; padding: 20px; border-radius: 10px; height: 190px; border: 1px solid #E1D5F5; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);"><h4 style="color: #4A148C;">📈 Analytics</h4><p style="color: #666; font-size: 14px;">Visualize your journey with interactive performance charts.</p></div>""",
        unsafe_allow_html=True)
with col3:
    st.markdown(
        """<div style="background-color: white; padding: 20px; border-radius: 10px; height: 190px; border: 1px solid #E1D5F5; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);"><h4 style="color: #4A148C;">🎯 Goal Roadmap</h4><p style="color: #666; font-size: 14px;">Calculate exact grades needed to reach your target CGPA.</p></div>""",
        unsafe_allow_html=True)

st.divider()
st.info("**Why Bezub?** We don't just calculate numbers; we help you plan your future.")

st.write("---")

# 1. Define the HTML in a variable first (Cleaner way)
# --- THE "STAY RENDERED" FIX ---

layout_code = """
<div style="background-color: #F3EAFD; padding: 25px; border-radius: 15px; border: 2px solid #D1B3FF; text-align: center; font-family: sans-serif;">
    <h2 style="color: #4A148C; margin: 0 0 10px 0;">Beyond Calculation. This is Strategy.</h2>
    <p style="color: #4A148C; font-size: 16px; font-weight: bold;">Why Ambitious Students Choose Bezub Pro</p>
    <div style="text-align: left; display: inline-block; color: #4A148C; margin-top: 15px;">
        <p>🛡 <b>The Cloud Vault:</b> Secure your entire academic history.</p>
        <p>📄 <b>Instant Transcripts:</b> Internship-ready PDFs in one click.</p>
        <p>🎯 <b>Goal Roadmap:</b> Exact grades needed to hit your targets.</p>
        <p>✨ <b>Ad-Free:</b> Focus on your future, not distractions.</p>
    </div>
</div>
"""

# CRITICAL: Make sure the line below is EXACTLY like this
st.markdown(layout_code, unsafe_allow_html=True)

st.write("")
if st.button("🚀 UPGRADE TO BEZUB PRO", use_container_width=True):
    st.balloons()
    st.toast("Pro features are coming soon!", icon="🎓")

st.markdown(
    "<p style='text-align: center; color: #4A148C; font-size: 12px; margin-top: 50px; opacity: 0.6;'>© 2026 Bezub Academic Systems.</p>",
    unsafe_allow_html=True)
