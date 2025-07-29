import streamlit as st
import pandas as pd 
import functions

def host_page(conn, cursor):
    Host_menu = ["Add Host", "View All Hosts", "View Host", "Edit Host", "Remove Host"]
    Host_choice = st.sidebar.selectbox("Menu", Host_menu)

    match Host_choice:
        case "Add Host":
            h_name = st.text_input("Host Name:")
            num = st.text_input("Mobile Number:")
            mail_id = st.text_input("Mail ID:")

            if st.button("Add Host"):
                query = 'INSERT INTO HOSTS (HOST_NAME, MOBILE_NUMBER, MAIL_ID) VALUES (?, ?, ?)'
                values = (h_name, num, mail_id)
                cursor.execute(query, values)
                conn.commit()
                st.success(f"Successfully added Host: {h_name}")

        case "View All Hosts":
            df = functions.view_all_hosts(cursor)
            st.dataframe(df)

        case "View Host":
            h_name = st.text_input("Host Name:")

            if st.button("View Host"):
                query = 'SELECT * FROM HOSTS WHERE HOST_NAME = ?'
                cursor.execute(query, (h_name,))
                data = cursor.fetchall()
                if data:
                    df = pd.DataFrame(data, columns=['Host ID', 'Host Name', 'Mobile Number', 'Mail ID'])
                    st.dataframe(df)
                else:
                    st.warning("No host found with that name.")

        case "Edit Host":
            edit_menu = ['Host Name', 'Mobile Number', 'Mail ID']
            edit_choice = st.selectbox("Menu", edit_menu)
            Host_id = st.text_input("Host ID:")

            if edit_choice == 'Host Name':
                h_name = st.text_input("New Host Name:")
                if st.button("Update"):
                    query = 'UPDATE HOSTS SET HOST_NAME = ? WHERE HOST_ID = ?'
                    values = (h_name, Host_id)
                    cursor.execute(query, values)
                    conn.commit()
                    st.success("Successfully Updated Host Name")

            elif edit_choice == 'Mobile Number':
                m_number = st.text_input("New Mobile Number:")
                if st.button("Update"):
                    query = 'UPDATE HOSTS SET MOBILE_NUMBER = ? WHERE HOST_ID = ?'
                    values = (m_number, Host_id)
                    cursor.execute(query, values)
                    conn.commit()
                    st.success("Successfully Updated Mobile Number")

            elif edit_choice == 'Mail ID':
                mail_id = st.text_input("New Mail ID:")
                if st.button("Update"):
                    query = 'UPDATE HOSTS SET MAIL_ID = ? WHERE HOST_ID = ?'
                    values = (mail_id, Host_id)
                    cursor.execute(query, values)
                    conn.commit()
                    st.success("Successfully Updated Mail ID")

        case "Remove Host":
            df = functions.view_all_hosts(cursor)
            with st.expander('View all Hosts'):
                st.dataframe(df)

            list_of_Hosts = [i for i in df.iloc[:, 0]]
            selected_Host = st.selectbox("Select Host ID to Delete", list_of_Hosts)

            if st.button("Delete Host"):
                query = 'DELETE FROM HOSTS WHERE HOST_ID = ?'
                cursor.execute(query, (selected_Host,))
                conn.commit()
                st.success("Host has been deleted successfully")
