
from google import genai


def generate_explanation(results, api_key):

    try:
        client = genai.Client(api_key=api_key)

        report_data = results.to_string(index=False)

        prompt = f"""
        You are a medical report explanation assistant.

        Explain the following synthetic blood test results
        in simple English that an ordinary person can understand.

        Report Results:
        {report_data}

        Please provide:

        1. Overall report summary.
        2. Explanation of each blood test.
        3. Explain which values are Normal, High or Low.
        4. Mention possible general reasons for abnormal values.
        5. Suggest discussing abnormal results with a doctor.

        Important:
        - Do not diagnose any disease.
        - Do not prescribe medicines.
        - Do not suggest treatment.
        - Use simple language.
        - Mention that reference ranges vary between laboratories.
        """

        response = client.models.generate_content(
          model="gemini-3.5-flash-lite",
          contents=prompt
        )

        return response.text

    except Exception as error:
        return f"AI Explanation Error: {error}"
