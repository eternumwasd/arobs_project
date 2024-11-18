from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from recorder import record_screen
from logger import logger
import time



def reject_cookies(driver): # Clicks the "Reject all" button when entering YouTube in a Selenium session
    driver.get("https://www.youtube.com")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Reject all']]"))
    )
    button.click()
    logger.info("Rejected all cookies.")

def play_from_youtube(driver, keyword, rectime):  # Automatically searches for the given term and plays the first video
    logger.info("Trying to play video.")
    try:
        search_bar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "search_query")))
        logger.info("Clicked the search bar.")
        search_bar.click()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)
        logger.info("Sent keyword.")

        # Waits for the first video and click it
        xpath = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a"
        video_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        video_element.click()
        logger.info("Clicked on the first video available.")

        # Check for age restriction
        try:
            age_restriction_xpath = '//*[@id="reason"]'
            age_restriction_element = WebDriverWait(driver, 5).until(
                EC.text_to_be_present_in_element((By.XPATH, age_restriction_xpath), "Sign in to confirm your age")
            )
            if age_restriction_element:
                logger.warning("Age restriction detected. Cannot proceed with the video.")
                return
        except TimeoutException:
            logger.info("No age restriction detected. Continuing.")

        # If there is a skippable ad, it will press the skip button.
        try:
            xpath_ad = f'//*[@id="skip-button:2"]'
            ad_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_ad)))
            ad_element.click()
        except TimeoutException:
            logger.info("Skip ad button not found. Continuing with the video.")

        # Start recording the screen for a specified duration (e.g., 30 seconds)
        logger.info("Starting screen recording.")
        logger.info(f"Recording saved as {record_screen(rectime)}")

    except TimeoutException as e:
        logger.error(f"An error occurred while trying to play the video: {e}")
