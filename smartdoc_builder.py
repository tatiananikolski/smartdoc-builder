import streamlit as st
import os

# Only import openai if not in demo mode (to avoid errors when openai isn't installed)
try:
    import openai
except ImportError:
    openai = None

st.set_page_config(page_title="SmartDoc Builder", layout="centered")

st.title("🧠 SmartDoc Builder")
st.subheader("Generate medical forms with AI")

# Form type selector
form_type = st.selectbox("Select a form type", [
    "Cardiology Intake Form",
    "Nuclear Test Consent Form",
    "Endocrinology Intake Form",
    "Custom"
])

# Tone selector
tone = st.radio("Select tone", ["Plain English", "Formal Medical"])

# Custom input box
custom_input = ""
if form_type == "Custom":
    custom_input = st.text_area("Describe the form you want")

# Demo mode toggle
demo_mode = st.checkbox("Demo Mode (Use sample outputs, no API calls)")

# Sample canned outputs
SAMPLE_FORMS = {
    "Cardiology Intake Form": """
    <h2>Cardiology Intake Form</h2>
    <p><strong>Patient Demographics:</strong> Name, DOB, Contact Info</p>
    <p><strong>Reason for Visit:</strong> Symptoms, Referral Reason</p>
    <p><strong>Past Medical History:</strong> Cardiovascular conditions, Surgeries</p>
    <p><strong>Current Medications:</strong> List with dosages</p>
    <p><strong>Allergies:</strong> Known allergies</p>
    <p><strong>Family History:</strong> Heart disease, Hypertension</p>
    <p><strong>Lifestyle:</strong> Smoking, Alcohol, Exercise habits</p>
    <p><strong>Previous Cardiac Tests:</strong> EKG, Echo, Stress test results</p>
    """,

    "Nuclear Test Consent Form": """
    <h2>Nuclear Stress Test Consent Form</h2>
    <p><strong>Purpose:</strong> To evaluate heart function using nuclear imaging.</p>
    <p><strong>Procedure:</strong> Explanation of the nuclear stress test.</p>
    <p><strong>Risks and Benefits:</strong> Minimal radiation exposure, possible side effects.</p>
    <p><strong>Alternatives:</strong> Other cardiac stress tests or imaging.</p>
    <p><strong>Acknowledgment:</strong> Patient understands the procedure and consents.</p>
    <p><strong>Signatures:</strong> Patient and Physician signature fields.</p>
    """,

    "Endocrinology Intake Form": """
    <h2>Endocrinology Intake Form</h2>
    <p><strong>Patient Demographics:</strong> Name, DOB, Contact Info</p>
    <p><strong>Reason for Visit:</strong> Diabetes, Thyroid issues, Hormone imbalance</p>
    <p><strong>Past Medical History:</strong> Endocrine disorders, Surgeries</p>
    <p><strong>Medications:</strong> Insulin, Hormone therapy</p>
    <p><strong>Allergies:</strong> Known allergies</p>
    <p><strong>Symptoms Checklist:</strong> Fatigue, Weight changes, Mood changes</p>
    <p><strong>Lifestyle & Diet:</strong> Exercise, Nutrition habits</p>
    <p><strong>Previous Lab Results:</strong> Recent blood tests, Imaging</p>
    """,
}

# Helper functions
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
    if openai is None:
        raise RuntimeError("OpenAI library is not installed.")
    openai.api_key = os.getenv("OPENAI_API_KEY")
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

# Main form generation
if st.button("Generate Form"):
    with st.spinner("Generating form..."):
        prompt = generate_prompt(form_type, custom_input, tone)

        if demo_mode:
            form_output = SAMPLE_FORMS.get(form_type, "<p><em>Custom demo form output here.</em></p>")
            st.markdown(form_output, unsafe_allow_html=True)
        else:
            try:
                form_output = call_openai_api(prompt)
                st.markdown(form_output, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during API call: {e}")

st.markdown("---")
st.caption("No PHI is used or stored. This is a prototype for demo purposes.")
