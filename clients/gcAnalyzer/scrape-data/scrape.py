from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

print("Starting scrape script")

# TODO use a relative instead of this absolute path
DRIVER_PATH = "/Users/steven/Documents/personal/projects/text-analyzer/lib/webdrivers/geckodriver"

# run settings
debug = True
quit_early = True
ready_to_quit = False
talks_before_early_quit = 1

# setup the driver
options = Options()
options.headless = True

driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
wait = WebDriverWait(driver, 10)

# define reusable element selectors
card_selector = 'a[href*="study/general-conference/"]'
talk_selector = 'a[href*="study/general-conference/"].item-3cCP7:not(.sectionTitle-27yfi)'
title_selector = "//h1[@id='title1']"

driver.get("https://www.churchofjesuschrist.org/study/general-conference?lang=eng")


def visit_all_cards():
    global ready_to_quit
    if ready_to_quit:
        return
    conference_content = driver.find_elements_by_class_name("manifest")
    cards = driver.find_elements_by_css_selector(card_selector)

    if len(conference_content) > 0:
        visit_all_talks()
    else:
        refs = []
        for card in cards:
            ref = card.get_attribute("href")
            refs.append(ref)
        for ref in refs:
            if ready_to_quit:
                return
            print(ref)
            driver.get(ref)
            visit_all_cards()


def visit_all_talks():
    global talks_before_early_quit
    global ready_to_quit
    talks = driver.find_elements_by_css_selector(talk_selector)
    for talk in talks:
        talks_before_early_quit = talks_before_early_quit - 1
        if quit_early and talks_before_early_quit < 0:
            ready_to_quit = True
            return
        talk.click()
        scrape_one_talk()


def scrape_one_talk():
    global debug
    title = ""
    author = ""

    wait.until(EC.presence_of_all_elements_located((By.XPATH, title_selector)))
    title_ele = driver.find_elements_by_xpath(title_selector)
    if len(title_ele) > 0:
        title = title_ele[0].text

    author_ele = driver.find_elements_by_class_name("author-name")
    if len(author_ele) > 0:
        author = author_ele[0].text

    paragraph_elements = driver.find_elements_by_xpath("//div[@class='body-block']//p")
    paragraphs = []
    for e in paragraph_elements:
        paragraphs.append(e.text)

    for p in paragraphs:
        print(p)
    if debug:
        print(f"Scraped {len(paragraphs)} paragraphs from {title} by {author}")


visit_all_cards()
driver.quit()

print("Successfully completed scrape script")
