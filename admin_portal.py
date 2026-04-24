import streamlit as st
import pandas as pd
from database import supabase, apply_custom_design

apply_custom_design()

st.title("🛡️ Admin Support Dashboard")
st.write("Review and manage user support tickets below.")

# Fetch tickets from Supabase
with st.spinner("Fetching tickets..."):
    response = supabase.table("tickets").select("*").order("created_at", desc=True).execute()

if not response.data:
    st.info("No support tickets found. Everything is quiet!")
else:
    # Convert to DataFrame for a nice UI
    tickets_df = pd.DataFrame(response.data)

    # Clean up the column names and dates for display
    tickets_df['created_at'] = pd.to_datetime(tickets_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')

    # Display the tickets
    st.dataframe(
        tickets_df[['username', 'message', 'created_at', 'status']],
        use_container_width=True,
        hide_index=True
    )

    # Simple "Resolve" logic
    st.divider()
    st.subheader("✅ Resolve a Ticket")
    ticket_id = st.number_input("Enter Ticket ID to close:", min_value=0, step=1)
    if st.button("Mark as Resolved"):
        supabase.table("tickets").update({"status": "resolved"}).eq("id", ticket_id).execute()
        st.success(f"Ticket #{ticket_id} updated!")
        st.rerun()