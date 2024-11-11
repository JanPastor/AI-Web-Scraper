from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
# Scraping Browser
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")
if not SBR_WEBDRIVER:
    raise ValueError("SBR_WEBDRIVER environment variable is not set. Please check your .env file.")

# Scrape the website
def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html

# Extract the body content from the HTML content
def extract_body_content(html_content): 
    soup = BeautifulSoup(html_content, "html.parser") # Parse the HTML content 
    body_content = soup.body # Get the body content 
    if body_content: # If the body content is not empty     
        return str(body_content) # Return the body content as a string
    return "" # Return an empty string if the body content is empty

# Clean the body content using BeautifulSoup parser
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser") # Parse the body content 
    # Remove script and style tags
    for script_or_style in soup(["script", "style"]): # Remove script and style tags
        script_or_style.extract() # Remove the script or style tag

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n") # This is the cleaned content and adds new lines between paragraphs
    cleaned_content = "\n".join( 
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    ) # Join the cleaned content with new lines
    # Return the cleaned content
    return cleaned_content

# Split the DOM content into chunks of a given maximum length
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
