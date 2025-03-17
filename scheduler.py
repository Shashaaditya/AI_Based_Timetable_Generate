import streamlit as st
import pandas as pd

st.title("📅 AI-Based Weekly Student Timetable Scheduler")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
time_slots = ["9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-1:00", "1:00-2:00 (Lunch)", "2:00-3:00", "3:00-4:00", "4:00-5:00"]

# Initialize empty timetable entries for each day and time slot
timetable_entries = {day: {slot: [] for slot in time_slots} for day in days}

st.subheader("Enter Timetable Details")

num_entries = st.number_input("Enter the number of subjects you want to schedule:", min_value=1, max_value=20, value=1)

for i in range(num_entries):
    st.subheader(f"Entry {i+1}")
    subject = st.text_input(f"Enter Subject {i+1}:", key=f"subject_{i}")
    faculty = st.text_input(f"Enter Faculty for {subject}:", key=f"faculty_{i}")
    classroom = st.selectbox(f"Select Classroom for {subject}", ["Room 101", "Room 102", "Room 103", "Room 104", "Room 105"], key=f"classroom_{i}")
    selected_days = st.multiselect(f"Select Days for {subject}", days, key=f"days_{i}")
    selected_time_slots = st.multiselect(f"Select Time Slots for {subject}", [slot for slot in time_slots if "Lunch" not in slot], key=f"time_slots_{i}")
    
    if subject and faculty and classroom and selected_days and selected_time_slots:
        sorted_days = sorted(selected_days, key=lambda x: days.index(x))
        sorted_time_slots = sorted(selected_time_slots, key=lambda x: time_slots.index(x))
        
        # Match days and time slots in the correct order
        max_entries = max(len(sorted_days), len(sorted_time_slots))
        
        # If days and time slots don't match, fill the shorter list with default values
        if len(sorted_days) < max_entries:
            sorted_days += [sorted_days[-1]] * (max_entries - len(sorted_days))  # Repeat last day
        if len(sorted_time_slots) < max_entries:
            sorted_time_slots += [sorted_time_slots[-1]] * (max_entries - len(sorted_time_slots))  # Repeat last time slot
        
        # Add subject details to timetable entries
        for day, time_slot in zip(sorted_days, sorted_time_slots):
            timetable_entries[day][time_slot].append(f"{subject}\n{faculty}\n{classroom}")

# Generate the timetable button
if st.button("Generate Weekly Timetable"):
    if any(any(entries for entries in timetable_entries[day].values()) for day in timetable_entries):
        df = pd.DataFrame(index=days, columns=time_slots)
        
        # Populate the dataframe with the timetable entries
        for day in days:
            for slot in time_slots:
                if timetable_entries[day][slot]:
                    df.at[day, slot] = "\n".join(timetable_entries[day][slot])
                else:
                    df.at[day, slot] = "-"
        
        st.subheader("📅 Generated Weekly Timetable")
        st.dataframe(df)

        # Make sure the timetable size stays fixed
        csv = df.to_csv(index=True).encode('utf-8')
        st.download_button("📥 Download Timetable", data=csv, file_name="weekly_timetable.csv", mime="text/csv")
    else:
        st.warning("Please fill in all fields!")
