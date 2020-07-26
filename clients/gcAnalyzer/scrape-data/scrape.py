from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

# TODO use a relative instead of this absolute path
DRIVER_PATH = "/Users/steven/Documents/personal/projects/text-analyzer/lib/webdrivers/geckodriver"
BASE_PATH = "https://www.churchofjesuschrist.org/study/general-conference?lang=eng"

# run settings
quit_early = True
ready_to_quit = False
talks_before_early_quit = 3


def scrape_gen_conf():
    """Scrape talks from general conference.

    Creates a Selenium Web Driver. Starting at BASE_PATH, visit all cards
    (eventually visiting every session of general conference).
    At each card, scrape the author, title, and content of each talk.

    Returns: an array of conference talks.
    """
    print("Starting to scrape general conference talks")

    # setup the driver
    options = Options()
    options.headless = False

    driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
    wait = WebDriverWait(driver, 10)

    # define reusable element selectors
    card_selector = 'a[href*="study/general-conference/"]'
    talk_selector = 'a[href*="study/general-conference/"].item-3cCP7:not(.sectionTitle-27yfi)'
    title_selector = "//h1[@id='title1']"

    driver.get("https://www.churchofjesuschrist.org/study/general-conference?lang=eng")

    def visit_all_cards():
        """Function to recursively visit all cards.

        Gather all hrefs from the visible cards on a page. Iterate through these
        links. At each page visited while iterating through the links, check
        whether conference content is visible. If so, call visit_all_talks().
        If not, recursively call self.

        Returns: an array of scraped conference talks.
        """
        global ready_to_quit
        talks = []
        if ready_to_quit:
            return talks
        conference_content = driver.find_elements_by_class_name("manifest")
        cards = driver.find_elements_by_css_selector(card_selector)

        if len(conference_content) > 0:
            talks = talks + visit_all_talks()
        else:
            refs = []
            for card in cards:
                ref = card.get_attribute("href")
                refs.append(ref)
            for ref in refs:
                if ready_to_quit:
                    return talks
                print(ref)
                driver.get(ref)
                talks = talks + visit_all_cards()
        return talks

    def visit_all_talks():
        """ Iterate through all talks in this session of conference.

        This method assumes that the web driver has already navigated to a
        page with a session of conference displayed. Iterate through all
        displayed talks in this session of conference, calling scrape_one_talk
        on each one.

        Returns: an array of all conference talks from one session of conference.
        """
        global talks_before_early_quit
        global ready_to_quit
        talks = []
        talks_elements = driver.find_elements_by_css_selector(talk_selector)
        for talk in talks_elements:
            talks_before_early_quit = talks_before_early_quit - 1
            if quit_early and talks_before_early_quit < 0:
                ready_to_quit = True
                return talks
            talk.click()
            talks.append(scrape_one_talk())
        return talks

    def scrape_one_talk():
        """ Scrape the content, title, and author of one conference talk.

        This method assumes that the web driver has already navigated to
        the page where the target talk is.

        Returns: a dictionary containing the author, title, and content
            from the conference talk.
        """
        talk = {}
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

        talk["title"] = title
        talk["author"] = author
        talk["paragraphs"] = paragraphs

        return talk

    return visit_all_cards()
    driver.quit()

    print("Successfully completed scrape script")
