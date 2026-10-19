import streamlit as st
import pandas as pd
from database import run_sql, apply_custom_design

apply_custom_design()

st.title("🛡️ Admin Support Dashboard")
st.write("Review and manage user support tickets below.")

with st.spinner("Fetching tickets..."):
    tickets = run_sql("select * from tickets order by created_at desc")

if not tickets:
    st.info("No support tickets found. Everything is quiet!")
else:
    tickets_df = pd.DataFrame(tickets)
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
        run_sql("update tickets set status = 'resolved' where id = %s", (int(ticket_id),), fetch=False)
        st.success(f"Ticket #{ticket_id} updated!")
        st.rerun()

st.markdown(
    "<p style='text-align: center; color: #4A148C; font-size: 12px; margin-top: 50px; opacity: 0.6;'>© 2026 Bezub Academic Systems.</p>",
    unsafe_allow_html=True)
