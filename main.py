import streamlit as st
from events import event_page 
from attendees import attendees_page
from hosts import host_page
from bills import bills_page
from supplier import supplier_page

from attendee_event import attendee_event
from query import query_page

import sqlite3


conn = sqlite3.connect("event_project.db")
cursor = conn.cursor()


def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HOSTS (
        HOST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        HOST_NAME TEXT,
        MOBILE_NUMBER TEXT,
        MAIL_ID TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EVENTS (
        EVENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        EVENT_NAME TEXT,
        EVENT_TYPE TEXT,
        EVENT_DATE_START DATE,
        EVENT_DATE_END DATE,
        EVENT_TIME_START TIME,
        EVENT_TIME_END TIME,
        VENUE TEXT,
        HOST_ID INTEGER,
        FOREIGN KEY (HOST_ID) REFERENCES HOSTS(HOST_ID)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SUPPLIER (
        SUPPLIER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SUPPLIER_NAME TEXT,
        DEPARTMENT TEXT,
        MAIL_ID TEXT,
        POINT_OF_CONTACT TEXT,
        MOBILE_NO TEXT,
        ADDRESS TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BILLS (
        BILL_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SUPPLIER_ID INTEGER,
        HOST_ID INTEGER,
        EVENT_ID INTEGER,
        AMOUNT INTEGER,
        PAYMENT_STATUS TEXT,
        FOREIGN KEY (EVENT_ID) REFERENCES EVENTS(EVENT_ID),
        FOREIGN KEY (HOST_ID) REFERENCES HOSTS(HOST_ID),
        FOREIGN KEY (SUPPLIER_ID) REFERENCES SUPPLIER(SUPPLIER_ID)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SUPPLIED_FOR (
        EVENT_ID INTEGER,
        SUPPLIER_ID INTEGER,
        FOREIGN KEY (EVENT_ID) REFERENCES EVENTS(EVENT_ID),
        FOREIGN KEY (SUPPLIER_ID) REFERENCES SUPPLIER(SUPPLIER_ID)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ATTENDEES (
        USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        F_NAME TEXT,
        L_NAME TEXT,
        MOBILE_NUMBER TEXT,
        MAIL_ID TEXT,
        DOB DATE,
        CITY TEXT,
        STATE TEXT,
        ADDRESS TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ATTENDED_BY (
        USER_ID INTEGER,
        EVENT_ID INTEGER,
        FOREIGN KEY (USER_ID) REFERENCES ATTENDEES(USER_ID),
        FOREIGN KEY (EVENT_ID) REFERENCES EVENTS(EVENT_ID)
    )''')

    conn.commit()

def main():
    create_table()

    st.title("Event Management")

    table_menu = ["Attendees", "Hosts", "Events", "Bills", "Supplier", "Attend an Event", "Write your own query"]
    table_choice = st.sidebar.selectbox("Table", table_menu)

    match table_choice:
        case "Events":
            event_page(conn, cursor)
        case "Attendees":
            attendees_page(conn, cursor)
        case "Hosts":
            host_page(conn, cursor)
        case "Bills":
            bills_page(conn, cursor)
        case "Supplier":
            supplier_page(conn, cursor)
        case "Attend an Event":
            attendee_event(conn, cursor)
        case "Write your own query":
            query_page(conn, cursor)

    conn.close()

if __name__ == '__main__':
    main()
