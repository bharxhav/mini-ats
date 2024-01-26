"""
mini-ats
"""

import os
from typing import Any

import PyPDF2 as pdf
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

class ResumeEvaluator:
    """
    A class to evaluate resumes based on job descriptions using the Gemini API.
    """

    def __init__(self):
        """
        Initializes the ResumeEvaluator class and configures the Gemini API key.
        """
        # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    def get_gemini_response(self, input_text: str) -> str:
        """
        Generates a response using the Gemini API for a given input text.

        Parameters:
            input_text (str): The input text for which the response is generated.

        Returns:
            str: The generated response.
        """
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_text)
        return response.text

    def input_pdf_text(self, uploaded_file: Any) -> str:
        """
        Extracts text from a PDF file.

        Parameters:
            uploaded_file (Any): The uploaded PDF file.

        Returns:
            str: The extracted text from the PDF file.
        """
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for _, page in enumerate(reader.pages):
            text += str(page.extract_text())
        return text


def main():
    """
    Main function for the Streamlit application.
    """
    st.title("Smart ATS")
    st.text("Improve Your Resume ATS")
    
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")
    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            resume_evaluator = ResumeEvaluator()
            resume_text = resume_evaluator.input_pdf_text(uploaded_file)
            input_prompt = f"""
            Act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of tech field, software engineering, data science, data analyst and big data engineer. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide best assistance for improving the resumes. Assign the percentage Matching based on Jd and the missing keywords with high accuracy.
            resume: {resume_text}
            description: {jd}
        
            I want the response in one single string having the structure \
            {{"JD Match":"%", 
            "Missing Keywords" : [],
            "Profile Summary" : ""}}
            """

            response = resume_evaluator.get_gemini_response(input_prompt)
            st.subheader(response)


if __name__ == "__main__":
    load_dotenv()
    main()
