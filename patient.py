import streamlit as st
import datetime

# Define Patient and HospitalLedger classes
class Patient:
    def __init__(self, patient_id, name, dob, gender):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.balance = 0
        self.transactions = []

    def add_transaction(self, date, description, amount):
        self.transactions.append({
            'date': date,
            'description': description,
            'amount': amount
        })
        self.balance += amount

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transactions

class HospitalLedger:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient

    def get_patient(self, patient_id):
        return self.patients.get(patient_id)

    def record_transaction(self, patient_id, date, description, amount):
        patient = self.get_patient(patient_id)
        if patient:
            patient.add_transaction(date, description, amount)
        else:
            st.error("Patient not found.")

    def generate_report(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            st.subheader(f"Patient: {patient.name} (ID: {patient.patient_id})")
            st.write(f"Balance: {patient.balance}")
            st.write("Transaction History:")
            for transaction in patient.transactions:
                st.write(f"{transaction['date']}: {transaction['description']} - {transaction['amount']}")
        else:
            st.error("Patient not found.")

# Initialize HospitalLedger
if 'ledger' not in st.session_state:
    st.session_state.ledger = HospitalLedger()

st.title("🏥 Hospital Ledger System")

# Sidebar for navigation
option = st.sidebar.selectbox("Choose Action", ["Add Patient", "Record Transaction", "Generate Report"])

if option == "Add Patient":
    st.header("Add New Patient")
    patient_id = st.text_input("Patient ID")
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    if st.button("Add Patient"):
        if patient_id and name:
            new_patient = Patient(patient_id, name, dob, gender)
            st.session_state.ledger.add_patient(new_patient)
            st.success(f"Patient {name} added successfully!")
        else:
            st.error("Please enter both Patient ID and Name.")

elif option == "Record Transaction":
    st.header("Record Transaction")
    patient_id = st.text_input("Patient ID for Transaction")
    date = st.date_input("Transaction Date", datetime.date.today())
    description = st.text_input("Description")
    amount = st.number_input("Amount", value=0)

    if st.button("Record Transaction"):
        if patient_id and description:
            st.session_state.ledger.record_transaction(patient_id, date, description, amount)
            st.success("Transaction recorded successfully!")
        else:
            st.error("Please enter Patient ID and Description.")

elif option == "Generate Report":
    st.header("Generate Patient Report")
    patient_id = st.text_input("Patient ID to View Report")

    if st.button("Generate Report"):
        st.session_state.ledger.generate_report(patient_id)
