from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time  

InputLanguage = 'en'

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <script>
        let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en';  
        recognition.continuous = true;

        recognition.onresult = function(event) {
            const transcript = event.results[event.results.length - 1][0].transcript;
            console.log("TEXT: " + transcript);  // Send text to terminal
        };

        recognition.start();
    </script>
</body>
</html>'''

# Write HTML file
os.makedirs("Data", exist_ok=True)
with open("Data/Voice.html", "w") as f:
    f.write(HtmlCode)

# Get file path
current_dir = os.getcwd()
Link = f"file:///{current_dir}/Data/Voice.html"

# Chrome options for complete background execution
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Fully Headless Mode
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-popup-blocking")  
chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging for headless mode
chrome_options.add_argument("--use-fake-ui-for-media-stream")  
chrome_options.add_argument("--allow-file-access-from-files")  
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  

# Initialize WebDriver in headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function for Speech Recognition
def SpeechRecognition():
    driver.get(Link)
    time.sleep(1)  # Wait for page load

    while True:
        try:
            Text = driver.find_element(By.TAG_NAME, "body").text
            if Text:
                print(f"Recognized Speech: {Text}")  # Show output in terminal
                return Text  
        except Exception as e:
            pass
        time.sleep(0.5)  # Avoid CPU overload

# Run
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(f"Final Output: {Text}")
