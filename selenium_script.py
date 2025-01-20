from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# List of URLs to process
urls_to_check = [

 ]

# List of suspicious URLs
suspicious_urls = [
    "https://web.sidexfee.com/",
    "https://box.tech-news.app/",
    "https://ww2.dizztips.com/",
    "https://blog.finzoox.com/"
]

def main():
    for input_url in urls_to_check:
        print(f"Processing URL: {input_url}")
        
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU usage
        chrome_options.add_argument("--no-sandbox")  # Necessary for Linux environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
        
        # Initialize WebDriver with headless mode
        driver = webdriver.Chrome(options=chrome_options)  # Adjust path to your WebDriver if necessary
        
        try:
            driver.get(input_url)
            
            # Wait for redirection and capture the final URL
            time.sleep(5)  # Adjust delay based on redirection time
            redirected_url = driver.current_url
            print(f"Redirected URL: {redirected_url}")
            
            # Check if the redirected URL matches any suspicious URLs
            if any(suspicious in redirected_url for suspicious in suspicious_urls):
                print(f"Detected suspicious URL: {redirected_url}")
                automate_verification(driver)
            else:
                print("No matching suspicious URL detected.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            # Close the browser and clean up
            driver.quit()
            print("Browser closed.")
        
        # Wait for 5 seconds before starting the next URL
        print("Waiting for 5 seconds before processing the next URL...")
        time.sleep(5)

def automate_verification(driver):
    try:
        wait = WebDriverWait(driver, 10)  # Adjust timeout if necessary
        time.sleep(12)  # Wait for the countdown to complete
        
        # Locate and click the verification button
        verification_button = wait.until(EC.element_to_be_clickable((By.ID, "lite-human-verif-button")))
        driver.execute_script("arguments[0].scrollIntoView();", verification_button)
        verification_button.click()
        print("Verification button clicked!")
        
        # Wait for 10 seconds and click the "Start" button
        time.sleep(12)
        start_button = wait.until(EC.presence_of_element_located((By.ID, "lite-start-sora-button")))
        driver.execute_script("arguments[0].scrollIntoView();", start_button)
        driver.execute_script("arguments[0].click();", start_button)
        print("Start button clicked!")
        
        # Wait for another 10 seconds and click the "End" button
        time.sleep(12)
        end_button = wait.until(EC.presence_of_element_located((By.ID, "lite-end-sora-button")))
        driver.execute_script("arguments[0].scrollIntoView();", end_button)
        driver.execute_script("arguments[0].click();", end_button)
        print("End button clicked!")
        
        # Wait for the new tab to open
        time.sleep(5)
        new_tab_url = get_new_tab_url(driver)
        
        if new_tab_url:
            print(f"New tab URL: {new_tab_url}")
            save_url_to_file(new_tab_url)
        else:
            print("No new tab detected.")
    
    except Exception as e:
        print(f"An error occurred during verification: {e}")

def get_new_tab_url(driver):
    """Switch to the new tab and get its URL."""
    original_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            return driver.current_url
    return None

def save_url_to_file(url):
    """Save the URL to a text file."""
    with open("urls.txt", "a") as file:
        file.write(url + "\n")
    print(f"URL saved to urls.txt")

if __name__ == "__main__":
    main()
