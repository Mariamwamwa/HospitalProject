from google import genai
from django.conf import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


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