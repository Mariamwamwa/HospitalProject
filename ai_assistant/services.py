from google import genai
from django.conf import settings

print("GEMINI KEY:", settings.GEMINI_API_KEY)

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def test_gemini():

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Say hello"
    )

    print(response.text)

def generate_health_summary(patient_data):

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=f"""
Create a patient health summary.

Patient details:
{patient_data}

Include:
- Overall health overview
- Appointment history
- Medical record summary
- Wellness recommendations

Do not provide diagnosis.
"""
    )

    return response.text



def generate_health_recommendation(patient_data):

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=f"""
You are a healthcare recommendation assistant.

Analyze this patient's health information:

{patient_data}


Generate personalized recommendations based on the patient's
existing diagnosis, medical records, prescriptions, and history.


Include:

Recommended Actions:
- What the patient should do

Lifestyle Advice:
- Diet, exercise, and daily habits

Follow-up:
- When the patient should consult a doctor


Important:
- Do not create new diagnoses.
- Do not replace a doctor's advice.
- If there is no diagnosis, provide general wellness recommendations.

Format:

Recommended Actions:

✓ Action 1
✓ Action 2


Lifestyle Advice:

✓ Advice 1


Follow-up:

✓ Advice
"""
    )

    return response.text

