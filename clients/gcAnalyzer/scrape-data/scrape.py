from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

print('Starting scrape script')

# TODO use a relative instead of this absolute path
DRIVER_PATH = "/Users/steven/Documents/personal/projects/text-analyzer/lib/webdrivers/geckodriver"

# setup the driver
options = Options()
options.headless = False

driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
wait = WebDriverWait(driver, 10)

# define reusable element selectors
card_selector = 'a[href*="study/general-conference/"]'
talk_selector = 'a[href*="study/general-conference/"].item-3cCP7:not(.sectionTitle-27yfi)'

driver.get('https://www.churchofjesuschrist.org/study/general-conference?lang=eng')


def visit_all_cards():
    print('visiting all cards')
    conference_content = driver.find_elements_by_class_name('manifest')
    cards = driver.find_elements_by_css_selector(card_selector)

    if len(conference_content) > 0:
        visit_all_talks()
    else:
        for card in cards:
            ref = card.get_attribute("href")
            print(ref)
            driver.get(ref)
            visit_all_cards()


def visit_all_talks():
    print('visiting all talks')
    talks = driver.find_elements_by_css_selector(talk_selector)
    for talk in talks:
        talk.click()
        scrape_one_talk()


def scrape_one_talk():
    print('scraping one talk')
    #title_ele = driver.find_elements_by_xpath("//h1[@id='title1']")
    #title = title_ele[0].text

    #author_ele = driver.find_elements_by_class_name("author-name")
    #author = author_ele[0].text

    paragraph_elements = driver.find_elements_by_xpath("//div[@class='body-block']//p")
    paragraphs = []
    for e in paragraph_elements:
        paragraphs.append(e.text)

    for p in paragraphs:
        print(p)


visit_all_cards()
driver.quit()

print('Successfully completed scrape script')
