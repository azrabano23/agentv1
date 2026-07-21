import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Config.USER_AGENT
        })
        self.driver = None
        
    def setup_selenium(self):
        """Setup Selenium WebDriver for dynamic content scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={Config.USER_AGENT}")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def close_selenium(self):
        """Close Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            
    def extract_linkedin_url(self, website_content):
        """Extract LinkedIn URL from website content"""
        linkedin_patterns = [
            r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_]+',
            r'linkedin\.com/in/[a-zA-Z0-9\-_]+',
            r'@[a-zA-Z0-9\-_]+.*linkedin'
        ]
        
        for pattern in linkedin_patterns:
            matches = re.findall(pattern, website_content, re.IGNORECASE)
            if matches:
                url = matches[0]
                if not url.startswith('http'):
                    url = 'https://' + url
                return url
        return None
    
    def scrape_personal_website(self):
        """Scrape content from personal website"""
        try:
            logger.info(f"Scraping personal website: {Config.PERSONAL_WEBSITE}")
            response = self.session.get(Config.PERSONAL_WEBSITE, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text_content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract LinkedIn URL
            linkedin_url = self.extract_linkedin_url(text_content)
            if linkedin_url:
                Config.LINKEDIN_URL = linkedin_url
                logger.info(f"Found LinkedIn URL: {linkedin_url}")
            
            # Extract structured data
            structured_data = {
                'title': soup.title.string if soup.title else '',
                'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
                'links': [a.get('href') for a in soup.find_all('a', href=True)],
                'text_content': text_content,
                'meta_description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else ''
            }
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Error scraping personal website: {e}")
            return None
    
    def scrape_linkedin_profile(self, linkedin_url):
        """Scrape LinkedIn profile content"""
        if not linkedin_url:
            logger.warning("No LinkedIn URL provided")
            return None
            
        try:
            logger.info(f"Scraping LinkedIn profile: {linkedin_url}")
            
            if not self.driver:
                self.setup_selenium()
            
            self.driver.get(linkedin_url)
            time.sleep(3)  # Wait for page to load
            
            # Wait for content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract profile information
            profile_data = {}
            
            try:
                # Name - try multiple selectors for different LinkedIn layouts
                name_selectors = [
                    "h1.text-heading-xlarge",
                    "h1.break-words",
                    ".text-heading-xlarge",
                    "h1[data-section='name']",
                    ".pv-text-details__left-panel h1"
                ]
                profile_data['name'] = "Not found"
                for selector in name_selectors:
                    try:
                        name_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if name_element.text.strip():
                            profile_data['name'] = name_element.text.strip()
                            break
                    except:
                        continue
            except:
                profile_data['name'] = "Not found"
            
            try:
                # Headline - try multiple selectors
                headline_selectors = [
                    ".text-body-medium.break-words",
                    ".text-body-medium",
                    ".pv-text-details__left-panel .text-body-medium",
                    "[data-section='headline']",
                    ".break-words.text-body-medium"
                ]
                profile_data['headline'] = "Not found"
                for selector in headline_selectors:
                    try:
                        headline_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if headline_element.text.strip():
                            profile_data['headline'] = headline_element.text.strip()
                            break
                    except:
                        continue
            except:
                profile_data['headline'] = "Not found"
            
            try:
                # About section - try multiple selectors
                about_selectors = [
                    ".pv-shared-text-with-see-more",
                    ".pv-about__summary-text",
                    ".pv-about__summary",
                    "[data-section='summary'] .pv-shared-text-with-see-more",
                    ".pv-about__summary-text .pv-shared-text-with-see-more"
                ]
                profile_data['about'] = "Not found"
                for selector in about_selectors:
                    try:
                        about_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if about_element.text.strip():
                            profile_data['about'] = about_element.text.strip()
                            break
                    except:
                        continue
            except:
                profile_data['about'] = "Not found"
            
            try:
                # Experience - try multiple selectors and sections
                experience_selectors = [
                    ".pvs-list__item--line-separated",
                    ".pvs-entity--padded",
                    ".pvs-list__item--with-top-padding",
                    "[data-section='experience'] .pvs-list__item",
                    ".experience__item"
                ]
                experience_data = []
                
                for selector in experience_selectors:
                    try:
                        experience_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if experience_elements:
                            for exp in experience_elements[:5]:  # Limit to first 5 experiences
                                try:
                                    # Try different text selectors
                                    title_selectors = [".t-bold", ".pvs-entity__path-node", ".pvs-entity__title-text"]
                                    company_selectors = [".t-normal", ".pvs-entity__path-node", ".pvs-entity__company-name"]
                                    
                                    title = ""
                                    company = ""
                                    
                                    for title_sel in title_selectors:
                                        try:
                                            title_elem = exp.find_element(By.CSS_SELECTOR, title_sel)
                                            if title_elem.text.strip():
                                                title = title_elem.text.strip()
                                                break
                                        except:
                                            continue
                                    
                                    for company_sel in company_selectors:
                                        try:
                                            company_elem = exp.find_element(By.CSS_SELECTOR, company_sel)
                                            if company_elem.text.strip():
                                                company = company_elem.text.strip()
                                                break
                                        except:
                                            continue
                                    
                                    if title and company:
                                        experience_data.append(f"{title} at {company}")
                                    elif title:
                                        experience_data.append(title)
                                except:
                                    continue
                            break  # If we found elements with this selector, stop trying others
                    except:
                        continue
                
                profile_data['experience'] = experience_data
            except:
                profile_data['experience'] = []
            
            try:
                # Education - try multiple selectors
                education_selectors = [
                    ".pvs-list__item--line-separated",
                    ".pvs-entity--padded",
                    "[data-section='education'] .pvs-list__item",
                    ".education__item"
                ]
                education_data = []
                
                for selector in education_selectors:
                    try:
                        education_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if education_elements:
                            for edu in education_elements[:3]:  # Limit to first 3 education entries
                                try:
                                    # Try different text selectors
                                    school_selectors = [".t-bold", ".pvs-entity__path-node", ".pvs-entity__school-name"]
                                    degree_selectors = [".t-normal", ".pvs-entity__path-node", ".pvs-entity__degree-name"]
                                    
                                    school = ""
                                    degree = ""
                                    
                                    for school_sel in school_selectors:
                                        try:
                                            school_elem = edu.find_element(By.CSS_SELECTOR, school_sel)
                                            if school_elem.text.strip():
                                                school = school_elem.text.strip()
                                                break
                                        except:
                                            continue
                                    
                                    for degree_sel in degree_selectors:
                                        try:
                                            degree_elem = edu.find_element(By.CSS_SELECTOR, degree_sel)
                                            if degree_elem.text.strip():
                                                degree = degree_elem.text.strip()
                                                break
                                        except:
                                            continue
                                    
                                    if school and degree:
                                        education_data.append(f"{degree} from {school}")
                                    elif school:
                                        education_data.append(f"Education from {school}")
                                except:
                                    continue
                            break  # If we found elements with this selector, stop trying others
                    except:
                        continue
                
                profile_data['education'] = education_data
            except:
                profile_data['education'] = []
            
            # Get full page text for additional context
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            profile_data['full_text'] = page_text
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn profile: {e}")
            return None
    
    def scrape_all_sources(self):
        """Scrape all available sources and return combined data"""
        all_data = {}
        
        # Scrape personal website
        website_data = self.scrape_personal_website()
        if website_data:
            all_data['website'] = website_data
        
        # Scrape LinkedIn - prioritize direct URL, fallback to extracted URL
        linkedin_url = Config.LINKEDIN_URL
        if not linkedin_url and 'website' in all_data:
            # Try to extract LinkedIn URL from website if not directly configured
            linkedin_url = self.extract_linkedin_url(all_data['website'].get('text_content', ''))
        
        if linkedin_url:
            logger.info(f"Scraping LinkedIn profile: {linkedin_url}")
            linkedin_data = self.scrape_linkedin_profile(linkedin_url)
            if linkedin_data:
                all_data['linkedin'] = linkedin_data
        else:
            logger.warning("No LinkedIn URL found for scraping")
        
        self.close_selenium()
        return all_data
