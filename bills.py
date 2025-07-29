import streamlit as st
import pandas as pd 
import functions

def bills_page(conn, cursor):
    bills_menu = ["Add Bill", "View All Bills", "View Bill", "Edit Bill", "Get Pending Bills", "Remove Bill"]
    bills_choice = st.sidebar.selectbox("Menu", bills_menu)

    match bills_choice:
        case "Add Bill":
            df1 = functions.view_all_suppliers(cursor)
            list_of_Supplier = [i for i in df1['Supplier Name']] if not df1.empty else []
            selected_Supplier = st.selectbox("Select Supplier", list_of_Supplier)

            supplier = None
            if selected_Supplier:
                supplier_df = df1.loc[df1['Supplier Name'] == selected_Supplier]
                if not supplier_df.empty:
                    supplier = str(supplier_df['Supplier ID'].values[0])
                else:
                    st.warning("⚠️ Selected Supplier not found.")
                    return

            df2 = functions.view_all_hosts(cursor)
            list_of_hosts = [i for i in df2['Host Name']] if not df2.empty else []
            selected_host = st.selectbox("Select Host", list_of_hosts)

            host_id = None
            if selected_host:
                host_df = df2.loc[df2['Host Name'] == selected_host]
                if not host_df.empty:
                    host_id = str(host_df['Host ID'].values[0])
                else:
                    st.warning("⚠️ Selected Host not found.")
                    return

            df3 = functions.view_all_events(cursor)
            list_of_events = [i for i in df3['Event Name']] if not df3.empty else []
            selected_event = st.selectbox("Select Event", list_of_events)

            event_id = None
            if selected_event:
                event_df = df3.loc[df3['Event Name'] == selected_event]
                if not event_df.empty:
                    event_id = str(event_df['Event ID'].values[0])
                else:
                    st.warning("⚠️ Selected Event not found.")
                    return

            amt = st.text_input("Amount:")
            payment_status = ['Pending', 'Completed']
            status = st.selectbox("Payment Status", payment_status)

            if st.button("Add Bill"):
                query = '''INSERT INTO BILLS (SUPPLIER_ID, HOST_ID, EVENT_ID, AMOUNT, PAYMENT_STATUS) 
                           VALUES (?, ?, ?, ?, ?)'''
                values = (supplier, host_id, event_id, amt, status)
                cursor.execute(query, values)
                conn.commit()
                st.success(f"✅ Successfully added Bill for Event: {selected_event}")

        case "View All Bills":
            df = functions.view_all_bills(cursor)
            st.dataframe(df)

        case "View Bill":
            df = functions.view_all_bills(cursor)
            list_of_events = list(set(df['Event Name'])) if not df.empty else []
            selected_event = st.selectbox("Select Event", list_of_events)

            if st.button("View Bills"):
                if df.empty:
                    st.warning("⚠️ No bills found.")
                else:
                    st.dataframe(df.loc[df['Event Name'] == selected_event])

        case "Edit Bill":
            df = functions.view_all_bills(cursor)
            with st.expander('View all Bills'):
                st.dataframe(df)

            edit_menu = ['Select Option', 'Supplier Name', 'Host Name', 'Event Name', 'Amount', 'Payment Status']
            edit_choice = st.selectbox("Menu", edit_menu)

            Bill_id = st.text_input("Bill ID:")

            if edit_choice == 'Supplier Name':
                df_sup = functions.view_all_suppliers(cursor)
                list_of_supplier = [i for i in df_sup['Supplier Name']] if not df_sup.empty else []
                selected_Supplier = st.selectbox("Select Supplier", list_of_supplier)

                if selected_Supplier and st.button("Update"):
                    supplier_df = df_sup.loc[df_sup['Supplier Name'] == selected_Supplier]
                    if supplier_df.empty:
                        st.warning("⚠️ Selected Supplier not found.")
                    else:
                        supplier = str(supplier_df['Supplier ID'].values[0])
                        query = 'UPDATE BILLS SET SUPPLIER_ID = ? WHERE BILL_ID = ?'
                        cursor.execute(query, (supplier, Bill_id))
                        conn.commit()
                        st.success("✅ Successfully Updated Bill")

            if edit_choice == 'Host Name':
                df_hosts = functions.view_all_hosts(cursor)
                list_of_hosts = [i for i in df_hosts['Host Name']] if not df_hosts.empty else []
                selected_host = st.selectbox("Select Host", list_of_hosts)

                if selected_host and st.button("Update"):
                    host_df = df_hosts.loc[df_hosts['Host Name'] == selected_host]
                    if host_df.empty:
                        st.warning("⚠️ Selected Host not found.")
                    else:
                        host_id = str(host_df['Host ID'].values[0])
                        query = 'UPDATE BILLS SET HOST_ID = ? WHERE BILL_ID = ?'
                        cursor.execute(query, (host_id, Bill_id))
                        conn.commit()
                        st.success("✅ Successfully Updated Bill")

            if edit_choice == 'Event Name':
                df_events = functions.view_all_events(cursor)
                list_of_events = [i for i in df_events['Event Name']] if not df_events.empty else []
                selected_event = st.selectbox("Select Event", list_of_events)

                if selected_event and st.button("Update"):
                    event_df = df_events.loc[df_events['Event Name'] == selected_event]
                    if event_df.empty:
                        st.warning("⚠️ Selected Event not found.")
                    else:
                        event_id = str(event_df['Event ID'].values[0])
                        query = 'UPDATE BILLS SET EVENT_ID = ? WHERE BILL_ID = ?'
                        cursor.execute(query, (event_id, Bill_id))
                        conn.commit()
                        st.success("✅ Successfully Updated Bill")

            if edit_choice == 'Amount':
                amt = st.text_input("Amount:")
                if st.button("Update"):
                    query = 'UPDATE BILLS SET AMOUNT = ? WHERE BILL_ID = ?'
                    cursor.execute(query, (amt, Bill_id))
                    conn.commit()
                    st.success("✅ Successfully Updated Bill")

            if edit_choice == 'Payment Status':
                status = ['Pending', 'Completed']
                selected_status = st.selectbox("Payment Status", status)
                if st.button("Update"):
                    query = 'UPDATE BILLS SET PAYMENT_STATUS = ? WHERE BILL_ID = ?'
                    cursor.execute(query, (selected_status, Bill_id))
                    conn.commit()
                    st.success("✅ Successfully Updated Bill")

        case "Remove Bill":
            df = functions.view_all_bills(cursor)
            with st.expander('View all Bills'):
                st.dataframe(df)

            list_of_Bills = [i for i in df['Bill ID']] if not df.empty else []
            selected_Bill = st.selectbox("Select Bill ID to Delete", list_of_Bills)

            if st.button("Delete Bill"):
                cursor.execute('DELETE FROM BILLS WHERE BILL_ID = ?', (selected_Bill,))
                conn.commit()
                st.success("✅ Bill has been deleted successfully")

        case "Get Pending Bills":
            df = functions.view_all_bills(cursor)
            event_names = [i for i in df['Event Name']] if not df.empty else []
            event_names.insert(0, "Select Event")
            e_name_choice = st.selectbox("Event Name", event_names)

            if e_name_choice != "Select Event":
                df1 = df.loc[df["Event Name"] == e_name_choice]
                df2 = df.loc[df["Payment Status"] == "Pending"]
                df_pending = pd.merge(df1, df2, how='inner')

                if df_pending.empty:
                    st.success("✅ No Pending Bills!")
                else:

                    st.dataframe(df_pending)
