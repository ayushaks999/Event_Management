import streamlit as st
import pandas as pd

def view_all_attendees_events(cursor):
    cursor.execute('''
        SELECT EVENT_ID, EVENT_NAME, USER_ID, F_NAME, L_NAME 
        FROM ATTENDED_BY 
        NATURAL JOIN ATTENDEES 
        NATURAL JOIN EVENTS
    ''')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Event ID', 'Event Name', 'User ID', 'First Name', 'Last Name'])
    return df

def view_all_attendees(cursor):
    cursor.execute('SELECT * FROM ATTENDEES')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['User ID', 'First Name', 'Last Name', 'Mobile Number', 'Mail ID', 'DOB', 'City', 'State', 'Address'])
    return df

def view_all_hosts(cursor):
    cursor.execute('SELECT * FROM HOSTS')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Host ID', 'Host Name', 'Mobile Number', 'Mail ID'])
    return df

def view_all_events(cursor):
    cursor.execute('SELECT * FROM EVENTS')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Event ID', 'Event Name', 'Event Type', 'Start Date', 'End Date', 'Start Time', 'End Time', 'Venue', 'Host ID'])
    
    # Convert time fields to datetime only if data exists (prevents errors on empty tables)
    if not df.empty:
        df["Start Time"] = pd.to_datetime(df["Start Time"], errors='coerce')
        df["End Time"] = pd.to_datetime(df["End Time"], errors='coerce')
    return df

def view_all_bills(cursor):
    # SQLite doesn’t support CALL procedure. We'll do a direct SELECT instead.
    query = '''
        SELECT B.BILL_ID, S.SUPPLIER_NAME, H.HOST_NAME, E.EVENT_NAME, B.AMOUNT, B.PAYMENT_STATUS
        FROM BILLS B
        LEFT JOIN SUPPLIER S ON B.SUPPLIER_ID = S.SUPPLIER_ID
        LEFT JOIN HOSTS H ON B.HOST_ID = H.HOST_ID
        LEFT JOIN EVENTS E ON B.EVENT_ID = E.EVENT_ID
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Bill ID', 'Supplier Name', 'Host Name', 'Event Name', 'Amount', 'Payment Status'])
    return df

def view_all_suppliers(cursor):
    cursor.execute('SELECT * FROM SUPPLIER')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Supplier ID', 'Supplier Name', 'Department', 'Mail ID', 'Point of Contact', 'Mobile Number', 'Address'])
    return df
