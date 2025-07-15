import streamlit as st
import openai
import os

# ------------------ CONFIG ------------------
st.set_page_config(page_title="SmartDoc Builder", layout="centered")

st.title("🧠 SmartDoc Builder")
st.subheader("Generate medical forms with AI")

# ------------------ FORM OPTIONS ------------------
form_type = st.selectbox("Select a form type", [
    "Cardiology Intake Form",
    "Nuclear Test Consent Form",
    "Endocrinology Intake Form",
    "Custom"
])

tone = st.radio("Select tone", ["Plain English", "Formal Medical"])

custom_input = ""
if form_type == "Custom":
    custom_input = st.text_area("Describe the form you want")

# ------------------ HELPER FUNCTIONS ------------------
def generate_prompt(form_type, custom_input, tone):
    if form_type == "Custom":
        return f"You are a medical administrator. Create a {tone.lower()} medical form based on the following request: {custom_input}"

    if form_type == "Cardiology Intake Form":
        return f"You are a medical administrator creating an intake form for a general cardiology clinic. Use a {tone.lower()} tone. Include demographics, reason for visit, past medical history (cardiac), medications, allergies, family history, lifestyle questions, and previous cardiac test results. Format as HTML."

    if form_type == "Nuclear Test Consent Form":
        return f"You are preparing a consent form for a nuclear stress test. Use a {tone.lower()} tone. Include purpose, explanation, risks, alternatives, acknowledgment, and signature areas. Format as HTML."

    if form_type == "Endocrinology Intake Form":
        return f"Create a new patient intake form for an endocrinology clinic. Use a {tone.lower()} tone. Include demographics, reason for visit, past medical history (endocrine), medications, allergies, symptoms checklist, lifestyle/diet, and prior test results. Format as HTML."

    return ""

def call_openai_api(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your API key as env variable
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates medical forms."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message['content']

# ------------------ GENERATE FORM ------------------
if st.button("Generate Form"):
    with st.spinner("Generating form..."):
        prompt = generate_prompt(form_type, custom_input, tone)
        try:
            form_output = call_openai_api(prompt)
            st.markdown(form_output, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("No PHI is used or stored. This is a prototype for demo purposes.")
