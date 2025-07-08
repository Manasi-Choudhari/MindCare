import streamlit as st
import pandas as pd
import os

def gratitude_journal():
    st.title("🌻 Gratitude Journal")
    entry = st.text_area("Write something you're grateful for:")
    if st.button("Save Entry"):
        if entry:
            df = pd.read_csv("gratitude_journal.csv") if os.path.exists("gratitude_journal.csv") else pd.DataFrame(columns=["Date", "Entry"])
            new_entry = {"Date": pd.to_datetime("today").strftime("%Y-%m-%d"), "Entry": entry}
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv("gratitude_journal.csv", index=False)
            st.success("Your gratitude entry has been saved!")

    if os.path.exists("gratitude_journal.csv"):
        df = pd.read_csv("gratitude_journal.csv")
        st.write("### Previous Entries")
        st.write(df)