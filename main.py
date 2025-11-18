# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Student Expenses Tracker", layout="wide")
st.title("💰 Student Expenses Tracker")

# --- User Input ---
st.header("Add Your Expense")

with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Books", "Others"])
    amount = st.number_input("Amount (RM)", min_value=0.0, step=0.01)
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Expense")

# --- Initialize session state ---
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# --- Add expense ---
if submitted:
    new_expense = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Amount": [amount],
        "Description": [description]
    })
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
    st.success("Expense added!")

# --- Display expenses ---
st.header("📊 Your Expenses")
if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses)

    # --- Total Expenses ---
    total = st.session_state.expenses["Amount"].sum()
    st.metric("Total Expenses (RM)", f"{total:.2f}")

    # --- Visualization ---
    st.subheader("Expenses by Category")
    plt.figure(figsize=(8,5))
    sns.barplot(
        data=st.session_state.expenses.groupby("Category")["Amount"].sum().reset_index(),
        x="Category",
        y="Amount",
        palette="viridis"
    )
    plt.ylabel("Total Amount (RM)")
    st.pyplot(plt)

    st.subheader("Expenses Over Time")
    plt.figure(figsize=(10,4))
    time_data = st.session_state.expenses.groupby("Date")["Amount"].sum().reset_index()
    sns.lineplot(data=time_data, x="Date", y="Amount", marker="o")
    plt.ylabel("Amount (RM)")
    st.pyplot(plt)

else:
    st.info("No expenses recorded yet. Add your first expense above!")