import streamlit as st
import pandas as pd 
import functions

def supplier_page(conn, cursor):
    Supplier_menu = ["Add Supplier", "View All Suppliers", "View Supplier", "Edit Supplier", "Remove Supplier"]
    Supplier_choice = st.sidebar.selectbox("Menu", Supplier_menu)

    match Supplier_choice:
        case "Add Supplier":
            s_name = st.text_input("Supplier Name:")
            dept = st.text_input("Department:")
            mail_id = st.text_input("Mail ID:")
            poc_name = st.text_input("Point of Contact:")
            m_number = st.text_input("Mobile Number:")
            address = st.text_input("Address:")

            if st.button("Add Supplier"):
                query = '''INSERT INTO Supplier 
                           (SUPPLIER_NAME, DEPARTMENT, MAIL_ID, POINT_OF_CONTACT, MOBILE_NO, ADDRESS) 
                           VALUES (?, ?, ?, ?, ?, ?)'''
                values = (s_name, dept, mail_id, poc_name, m_number, address)
                cursor.execute(query, values)
                conn.commit()
                st.success(f"✅ Successfully added Supplier: {s_name}")

        case "View All Suppliers":
            df = functions.view_all_suppliers(cursor)
            st.dataframe(df)

        case "View Supplier":
            df = functions.view_all_suppliers(cursor)
            list_of_Supplier = [i for i in df.iloc[:, 1]]
            selected_Supplier = st.selectbox("Select Supplier", list_of_Supplier)

            if st.button("View Supplier"):
                cursor.execute('SELECT * FROM Supplier WHERE SUPPLIER_NAME = ?', (selected_Supplier,))
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['Supplier ID', 'Supplier Name', 'Department', 'Mail ID', 'Point of Contact', 'Mobile Number', 'Address'])
                st.dataframe(df)

        case "Edit Supplier":
            edit_menu = ['Supplier Name', 'Department', 'Mail ID', 'Point of Contact', 'Mobile Number', 'Address']
            edit_choice = st.selectbox("Select Field to Edit", edit_menu)

            df = functions.view_all_suppliers(cursor)
            list_of_Supplier = [i for i in df.iloc[:, 1]]
            selected_Supplier = st.selectbox("Select Supplier", list_of_Supplier)

            new_value = st.text_input(f"Enter new {edit_choice}:")
            if st.button("Update"):
                field_name = edit_choice.replace(" ", "_").upper()
                query = f'UPDATE Supplier SET {field_name} = ? WHERE SUPPLIER_NAME = ?'
                cursor.execute(query, (new_value, selected_Supplier))
                conn.commit()
                st.success(f"✅ Successfully updated {edit_choice} for {selected_Supplier}")

        case "Remove Supplier": 
            df = functions.view_all_suppliers(cursor)
            with st.expander('View all Suppliers'):
                st.dataframe(df)
            
            list_of_Supplier = [i for i in df.iloc[:, 1]]
            selected_Supplier = st.selectbox("Select Supplier to Delete", list_of_Supplier)
            if st.button("Delete Supplier"):
                cursor.execute('DELETE FROM Supplier WHERE SUPPLIER_NAME = ?', (selected_Supplier,))
                conn.commit()
                st.success(f"🗑 Supplier {selected_Supplier} has been deleted successfully")





















