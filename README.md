# Handwrite to Excel Converter

An AI-powered web application that converts images of handwritten bookkeeping notes into structured Excel spreadsheets. This project leverages the Google Gemini 3.5 Flash vision model to automatically extract, infer, and format unstructured handwritten data.

## Features

* Automated Data Extraction: Intelligently converts messy handwritten records into a structured format (Date, Amount, Notes).
* High-Accuracy Vision AI: Utilizes the Gemini 3.5 Flash model to handle complex layouts, strike-throughs, and cursive handwriting.
* Secure API Key Management: Users input their own Google Gemini API key via the web interface. Keys are never hardcoded or stored on the server, ensuring user privacy.
* Instant Excel Export: Processed data can be previewed directly on the web and downloaded as a formatted `.xlsx` file.
* Modern Web UI: Built with Streamlit for a clean, responsive, and user-friendly experience across desktop and mobile browsers.

## Tech Stack

* Language: Python
* Frontend Framework: Streamlit
* AI Model: Google Gemini 3.5 Flash (via google-genai SDK)
* Data Processing: Pandas, Openpyxl, Pillow
* Environment Management: uv

## Prerequisites

* Python installed on your local machine.
* `uv` package manager installed.
* A valid Google Gemini API Key (available for free from Google AI Studio).

## Installation and Setup

1. Clone this repository:
   ```bash
   git clone [https://github.com/Mintszebra/handwrite-to-excel.git](https://github.com/Mintszebra/handwrite-to-excel.git)
   cd handwrite-to-excel
Install dependencies using uv:

Bash
uv pip install streamlit google-genai pandas openpyxl pillow
Run the application:

Bash
uv run streamlit run app.py
Usage
Open the provided Local URL (usually http://localhost:8501) in your web browser.

Enter your Google Gemini API Key in the sidebar configuration panel.

Upload an image (JPG, JPEG, or PNG) of your handwritten notes.

Click the "Start Conversion" button and wait for the AI to process the image.

Preview the parsed data table and click "Download Excel" to save the file to your device.

Project Structure
app.py: The main Streamlit web application containing the UI logic and API integration.

experiments/: Contains early prototype scripts (e.g., local offline processing using Ollama). These are preserved to document the technical decision-making process and architecture evolution.

.gitignore: Configuration to prevent sensitive data, local environments, and temporary files from being committed to version control.

Privacy Disclaimer
If you are using the free tier of the Google Gemini API, the images and prompts you submit may be collected by Google to improve their AI models. Please refrain from uploading documents containing highly sensitive personal, medical, or confidential corporate financial information.
