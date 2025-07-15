import streamlit as st
import os

try:
    import openai
except ImportError:
    openai = None

st.set_page_config(page_title="SmartDoc Builder", layout="centered")

st.title("🧠 SmartDoc Builder")
st.subheader("Generate medical forms with AI")

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

demo_mode = st.checkbox("Demo Mode (Use sample outputs, no API calls)")

SAMPLE_FORMS = {
    "Cardiology Intake Form": """
    <h2>Cardiology Intake Form</h2>
    <form>
      <label>Full Name:</label><br>
      <input type="text" name="fullname"><br><br>

      <label>Date of Birth:</label><br>
      <input type="date" name="dob"><br><br>

      <label>Reason for Visit:</label><br>
      <textarea name="reason" rows="3" cols="40"></textarea><br><br>

      <label>Past Medical History (Cardiac):</label><br>
      <textarea name="history" rows="3" cols="40"></textarea><br><br>

      <label>Current Medications:</label><br>
      <textarea name="medications" rows="3" cols="40"></textarea><br><br>

      <label>Allergies:</label><br>
      <textarea name="allergies" rows="2" cols="40"></textarea><br><br>

      <label>Family History of Heart Disease:</label><br>
      <textarea name="family" rows="2" cols="40"></textarea><br><br>

      <label>Lifestyle (Smoking, Alcohol, Exercise):</label><br>
      <textarea name="lifestyle" rows="2" cols="40"></textarea><br><br>

      <label>Previous Cardiac Tests:</label><br>
      <textarea name="tests" rows="3" cols="40"></textarea><br><br>
    </form>
    """,

    "Nuclear Test Consent Form": """
    <h2>Nuclear Stress Test - Consent Form</h2>
    <form>
      <p><strong>Purpose of the Procedure:</strong><br>
      A nuclear stress test is used to evaluate blood flow to your heart muscle, both at rest and during stress.</p>

      <p><strong>Procedure Description:</strong><br>
      You will receive a small amount of radioactive material and undergo imaging after exercise or medication-induced stress.</p>

      <p><strong>Risks:</strong><br>
      Minor side effects may include nausea, dizziness, or allergic reaction to the tracer.</p>

      <p><strong>Alternatives:</strong><br>
      Echocardiogram, treadmill test, or no testing.</p>

      <p><strong>Benefits:</strong><br>
      Accurate assessment of cardiac function and identification of blocked arteries.</p>

      <label>Patient Initials:</label><br>
      <input type="text" name="initials"><br><br>

      <label>Patient Signature:</label><br>
      <input type="text" name="signature"><br><br>

      <label>Date:</label><br>
      <input type="date" name="date"><br><br>

      <label>Physician Signature:</label><br>
      <input type="text" name="physician"><br><br>
    </form>
    """,

    "Endocrinology Intake Form": """
    <h2>Endocrinology Intake Form</h2>
    <form>
      <label>Full Name:</label><br>
      <input type="text" name="fullname"><br><br>

      <label>Date of Birth:</label><br>
      <input type="date" name="dob"><br><br>

      <label>Reason for Visit:</label><br>
      <textarea name="reason" rows="3" cols="40" placeholder="e.g., Thyroid disorder, Diabetes, Hormonal issues"></textarea><br><br>

      <label>Past Medical History (Endocrine):</label><br>
      <textarea name="history" rows="3" cols="40"></textarea><br><br>

      <label>Current Medications:</label><br>
      <textarea name="medications" rows="3" cols="40"></textarea><br><br>

      <label>Allergies:</label><br>
      <textarea name="allergies" rows="2" cols="40"></textarea><br><br>

      <label>Symptoms Checklist:</label><br>
      <input type="checkbox"> Fatigue<br>
      <input type="checkbox"> Weight Gain/Loss<br>
      <input type="checkbox"> Mood Changes<br>
      <input type="checkbox"> Excessive Thirst<br>
      <input type="checkbox"> Hair Loss<br><br>

      <label>Lifestyle & Diet Overview:</label><br>
      <textarea name="lifestyle" rows="3" cols="40"></textarea><br><br>

      <label>Prior Lab Results (if known):</label><br>
      <textarea name="labs" rows="3" cols="40"></textarea><br><br>
    </form>
    """
}
# PDF Download Links
PDF_LINKS = {
    "Cardiology Intake Form": "https://drive.google.com/uc?export=download&id=1yGDs2--MvUlVJPnOkikAn8FTJMSWy68v",
    "Nuclear Test Consent Form": "https://drive.google.com/uc?export=download&id=1a3YQuTujX5EDGiX-z1IMcsEC7Sv62JWD",
    "Endocrinology Intake Form": "https://drive.google.com/uc?export=download&id=1-vAj3pHfb4B7aCoWvbfXxvBT8U86szwh"
}

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

if st.button("Generate Form"):
    with st.spinner("Generating form..."):
        prompt = generate_prompt(form_type, custom_input, tone)

        if demo_mode:
            form_output = SAMPLE_FORMS.get(form_type, "<p><em>Custom demo form output here.</em></p>")
            st.markdown(form_output, unsafe_allow_html=True)
                # ✅ Add download button (based on form type)
    if form_type in PDF_LINKS:
        pdf_link = PDF_LINKS[form_type]
        st.markdown(
            f"""
            <a href="{pdf_link}" download target="_blank">
                <button style="margin-top: 20px; padding: 10px 20px; font-size: 16px;">
                    ⬇️ Download This Form as PDF
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

            st.markdown(
    """
    <button onclick="window.print()" style="margin-top: 20px; padding: 10px 20px; font-size: 16px;">
        🖨️ Print or Save as PDF
    </a>
    """,
    unsafe_allow_html=True
)
        else:
            try:
                form_output = call_openai_api(prompt)
                st.markdown(form_output, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during API call: {e}")

st.markdown("---")
st.caption("No PHI is used or stored. This is a prototype for demo purposes.")
