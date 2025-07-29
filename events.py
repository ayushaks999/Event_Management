import streamlit as st
import pandas as pd 
import functions

def event_page(conn, cursor):
    Event_menu = ["Add Event", "View All Events", "View Event", "Edit Event", "Remove Event"]
    Event_choice = st.sidebar.selectbox("Menu", Event_menu)

    match Event_choice:
        case "Add Event":
            e_name = st.text_input("Event Name:")
            e_type = st.text_input("Event Type:")
            e_date_start = st.date_input("Event Start Date:")
            e_date_end = st.date_input("Event End Date:")
            venue = st.text_input("Venue:")
            start_time = st.time_input("Event Start Time:")
            end_time = st.time_input("Event End Time:")
            host_id = st.text_input("Host ID:")

            if st.button("Add Event"):
                e_date_start_str = e_date_start.strftime('%Y-%m-%d')
                e_date_end_str = e_date_end.strftime('%Y-%m-%d')
                start_time_str = start_time.strftime('%H:%M:%S')
                end_time_str = end_time.strftime('%H:%M:%S')

                query = '''
                    INSERT INTO Events 
                    (EVENT_NAME, EVENT_TYPE, EVENT_DATE_START, EVENT_DATE_END, EVENT_TIME_START, EVENT_TIME_END, VENUE, HOST_ID) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                values = (e_name, e_type, e_date_start_str, e_date_end_str, start_time_str, end_time_str, venue, host_id)
                cursor.execute(query, values)
                conn.commit()
                st.success(f"Successfully added Event: {e_name}")

        case "View All Events":            
            df = functions.view_all_events(cursor)
            st.dataframe(df)

        case "View Event":
            e_name = st.text_input("Event Name:")

            if st.button("View Event"):
                query = 'SELECT * FROM Events WHERE EVENT_NAME = ?'
                cursor.execute(query, (e_name,))
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['Event ID', 'Event Name', 'Event Type', 'Start Date', 'End Date', 'Start Time', 'End Time', 'Venue', 'Host ID'])
                st.dataframe(df)

        case "Edit Event":
            edit_menu = ['Event Name', 'Event Type', 'Start Date', 'End Date', 'Start Time', 'End Time', 'Venue', 'Host ID']
            edit_choice = st.selectbox("Menu", edit_menu)

            if edit_choice == 'Event Name':
                Event_id = st.text_input("Event ID:")
                e_name = st.text_input("New Event Name:")
                if st.button("Update"):
                    cursor.execute('UPDATE Events SET EVENT_NAME = ? WHERE EVENT_ID = ?', (e_name, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

            if edit_choice == 'Event Type':
                Event_id = st.text_input("Event ID:")
                e_type = st.text_input("New Event Type:")
                if st.button("Update"):
                    cursor.execute('UPDATE Events SET EVENT_TYPE = ? WHERE EVENT_ID = ?', (e_type, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

            if edit_choice == 'Start Date':
                Event_id = st.text_input("Event ID:")
                start = st.date_input("New Start Date:")
                if st.button("Update"):
                    start_str = start.strftime('%Y-%m-%d')
                    cursor.execute('UPDATE Events SET EVENT_DATE_START = ? WHERE EVENT_ID = ?', (start_str, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

            if edit_choice == 'End Date':
                Event_id = st.text_input("Event ID:")
                end = st.date_input("New End Date:")
                if st.button("Update"):
                    end_str = end.strftime('%Y-%m-%d')
                    cursor.execute('UPDATE Events SET EVENT_DATE_END = ? WHERE EVENT_ID = ?', (end_str, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

            if edit_choice == 'Start Time':
                Event_id = st.text_input("Event ID:")
                start_t = st.time_input("New Start Time:")
                if st.button("Update"):
                    start_t_str = start_t.strftime('%H:%M:%S')
                    cursor.execute('UPDATE Events SET EVENT_TIME_START = ? WHERE EVENT_ID = ?', (start_t_str, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

            if edit_choice == 'End Time':
                Event_id = st.text_input("Event ID:")
                end_t = st.time_input("New End Time:")
                if st.button("Update"):
                    end_t_str = end_t.strftime('%H:%M:%S')
                    cursor.execute('UPDATE Events SET EVENT_TIME_END = ? WHERE EVENT_ID = ?', (end_t_str, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

            if edit_choice == 'Venue':
                Event_id = st.text_input("Event ID:")
                venue = st.text_input("New Venue:")
                if st.button("Update"):
                    cursor.execute('UPDATE Events SET VENUE = ? WHERE EVENT_ID = ?', (venue, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

            if edit_choice == 'Host ID':
                Event_id = st.text_input("Event ID:")
                h_id = st.text_input("New Host ID:")
                if st.button("Update"):
                    cursor.execute('UPDATE Events SET HOST_ID = ? WHERE EVENT_ID = ?', (h_id, Event_id))
                    conn.commit()
                    st.success("Successfully Updated Event")

        case "Remove Event":
            df = functions.view_all_events(cursor)
            with st.expander('View all Events'):
                st.dataframe(df)
            
            list_of_Event = [i for i in df.iloc[:, 0]]
            selected_Event = st.selectbox("Select Event ID to Delete", list_of_Event)

            if st.button("Delete Event"):
                cursor.execute('DELETE FROM Events WHERE EVENT_ID = ?', (selected_Event,))
                conn.commit()
                st.success("Event has been deleted successfully")
