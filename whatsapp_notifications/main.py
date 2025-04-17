from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send_whatsapp_messages(message, numbers, media_path=None):
    """
    Sends WhatsApp messages to the provided numbers using Selenium.

    :param message: The message to send.
    :param numbers: List of phone numbers to send the message to.
    :param media_path: Path to the media file to send (optional).
    """
    print(f"send_whatsapp_messages called with message: {message}, numbers: {numbers}, media_path: {media_path}")  # Debug log

    try:
        # Use a persistent user profile so login persists
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=/tmp/chrome-profile")  # Use a separate temp profile
        options.add_argument("--profile-directory=Default")
        options.add_argument("--start-maximized")

        print("Initializing WebDriver...")  # Debug log
        try:
            driver = webdriver.Chrome(options=options)
            print("WebDriver initialized successfully.")  # Debug log
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")
            return

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com")
        print("WhatsApp Web opened.")  # Debug log

        # Wait for WhatsApp to fully load
        print("Waiting for WhatsApp Web to be ready...")
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
            )
            print("WhatsApp Web is ready.")  # Debug log
        except:
            input("Scan the QR code in the browser, then press Enter to continue...")

        for number in numbers:
            try:
                # Open chat with the specific number
                url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
                print(f"Opening chat for number: {number}")  # Debug log
                driver.get(url)

                # Wait for the chat to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
                )
                print(f"Chat loaded for number: {number}")  # Debug log

                # Press Enter to send the message
                send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                send_button.click()
                print(f"Message sent to {number}")  # Debug log
                time.sleep(5)

                # Optionally, send media
                if media_path:
                    attach_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]'))
                    )
                    attach_button.click()

                    media_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
                    )
                    media_input.send_keys(media_path)

                    send_media_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
                    )
                    send_media_button.click()
                    print(f"Media sent to {number}")  # Debug log
                    time.sleep(5)

            except Exception as e:
                print(f"Failed to send message to {number}: {e}")

        # Close the browser
        driver.quit()
        print("WebDriver closed.")  # Debug log

    except Exception as e:
        print(f"Error initializing WebDriver or loading WhatsApp Web: {e}")
