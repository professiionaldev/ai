from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import time
import mtranslate as mt

# Load environment variables
env_vars = dotenv_values(".env")

# Get the input language from the environment variables
InputLanguage = env_vars.get("InputLanguage", "en-US")  # Default to English if not set

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'LANG_CODE';
            recognition.continuous = true;
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript + " ";
            };

            recognition.onerror = function(event) {
                console.error("Speech recognition error:", event.error);
            };

            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
            }
        }
    </script>
</body>
</html>'''

# Replace language placeholder with actual language setting
HtmlCode = HtmlCode.replace("LANG_CODE", InputLanguage)

# Save the HTML file
data_folder = "Data"
os.makedirs(data_folder, exist_ok=True)  # Ensure the Data folder exists
html_file_path = os.path.join(data_folder, "Voice.html")

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Get the absolute file path for the HTML file
html_file_url = f"file:///{os.path.abspath(html_file_path)}"

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allows mic access
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")  # Optional: run browser in headless mode

# Initialize the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to modify query for proper formatting
def QueryModifier(query):
    query = query.strip().lower()
    if query and query[-1] not in [".", "?", "!"]:
        query += "."

    return query.capitalize()

# Function to translate text to English if needed
def UniversalTranslator(text):
    return mt.translate(text, "en", "auto").capitalize()

# Function to perform speech recognition using Selenium
def SpeechRecognition():
    driver.get(html_file_url)
    driver.find_element(By.ID, "start").click()

    print("🎤 Listening... Speak now!")

    while True:
        try:
            time.sleep(3)  # Wait for speech to be recognized
            text = driver.find_element(By.ID, "output").text.strip()

            if text:
                driver.find_element(By.ID, "end").click()  # Stop recognition
                print(f"✅ Recognized: {text}")

                # Translate if needed
                if "en" in InputLanguage.lower():
                    return QueryModifier(text)
                else:
                    print("🌍 Translating to English...")
                    return QueryModifier(UniversalTranslator(text))
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            break

# Main execution loop
if __name__ == "__main__":
    while True:
        recognized_text = SpeechRecognition()
        print(f"🔹 Final Output: {recognized_text}")
