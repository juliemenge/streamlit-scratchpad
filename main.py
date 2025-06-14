import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="Spreadsheet Scratchpad", layout="wide")
st.title("🧮 Spreadsheet Scratchpad")

st.markdown("Use this lightweight, disposable spreadsheet for quick calculations. Nothing is saved.")

st.subheader("1. Input Data")
input_text = st.text_area("Paste data (tab or comma-separated):", height=200, placeholder="e.g.\nItem, Cost\nA, 10\nB, 15")

def parse_input(text):
    try:
        if "," in text:
            df = pd.read_csv(io.StringIO(text))
        else:
            df = pd.read_csv(io.StringIO(text), delimiter="\t")
        return df
    except Exception as e:
        st.warning("Could not parse input. Check format.")
        return pd.DataFrame()

if input_text:
    df = parse_input(input_text)
    if not df.empty:
        st.dataframe(df, use_container_width=True)

        st.subheader("2. Quick Stats")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col = st.selectbox("Choose a column to summarize:", numeric_cols)
            if col:
                st.write(f"**Sum:** {df[col].sum():,.2f}")
                st.write(f"**Mean:** {df[col].mean():,.2f}")
                st.write(f"**Max:** {df[col].max():,.2f}")
                st.write(f"**Min:** {df[col].min():,.2f}")

        st.subheader("3. Custom Formula")
        formula = st.text_input("Enter a formula using column names (e.g., df['Cost'] * 1.1)")
        if formula:
            try:
                result = eval(formula)
                st.write("Result:", result)
            except Exception as e:
                st.error(f"Error evaluating formula: {e}")
    else:
        st.info("Waiting for valid data input.")
else:
    st.info("Paste some data above to get started.")