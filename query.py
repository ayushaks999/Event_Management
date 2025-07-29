import streamlit as st
import pandas as pd
from functions import view_all_events

def query_page(conn, cursor):
    query = st.text_area('Enter your SQL query:')

    if st.button("Execute"):
        try:
            cursor.execute(query)

            # Only commit if the query modifies the DB
            if query.strip().lower().startswith(("insert", "update", "delete", "create", "drop", "alter")):
                conn.commit()
                st.success("✅ Query executed and changes committed.")
                return

            # Fetch data for SELECT queries
            data = cursor.fetchall()

            # If query is specifically for events table, use the function for formatting
            if query.strip().lower() == 'select * from events;':
                df = view_all_events(cursor)
            else:
                # Dynamically fetch column names from cursor.description
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                df = pd.DataFrame(data, columns=columns)

            st.dataframe(df)
            st.success("✅ Query executed successfully!")

        except Exception as e:
            st.error(f"❌ Error executing query: {e}")
