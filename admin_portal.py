import streamlit as st
import pandas as pd
from database import supabase, apply_custom_design

apply_custom_design()

st.title("🛡️ Admin Support Dashboard")
st.write("Review and manage user support tickets below.")

with st.spinner("Fetching tickets..."):
    response = supabase.table("tickets").select("*").order("created_at", desc=True).execute()

if not response.data:
    st.info("No support tickets found. Everything is quiet!")
else:
    tickets_df = pd.DataFrame(response.data)
    tickets_df['created_at'] = pd.to_datetime(tickets_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')

    st.dataframe(
        tickets_df[['username', 'message', 'created_at', 'status']],
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("✅ Resolve a Ticket")
    ticket_id = st.number_input("Enter Ticket ID to close:", min_value=0, step=1)
    if st.button("Mark as Resolved"):
        supabase.table("tickets").update({"status": "resolved"}).eq("id", ticket_id).execute()
        st.success(f"Ticket #{ticket_id} updated!")
        st.rerun()

st.markdown(
    "<p style='text-align: center; color: #4A148C; font-size: 12px; margin-top: 50px; opacity: 0.6;'>© 2026 Bezub Academic Systems.</p>",
    unsafe_allow_html=True)
