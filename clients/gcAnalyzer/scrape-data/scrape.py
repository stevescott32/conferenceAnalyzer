from selenium import webdriver

print('Starting scrape script')

# TODO use a relative instead of this absolute path
DRIVER_PATH = "/Users/steven/Documents/personal/projects/text-analyzer/lib/webdrivers/geckodriver"
driver = webdriver.Firefox(executable_path=DRIVER_PATH)

driver.get('https://www.churchofjesuschrist.org/study/general-conference/2019/10/11holland?lang=eng')

titleEle = driver.find_elements_by_xpath("//h1[@id='title1']")
title = titleEle[0].text

authorEle = driver.find_elements_by_class_name("author-name")
author = authorEle[0].text

paragraphsEles = driver.find_elements_by_xpath("//div[@class='body-block']//p")
allText = ''
paragraphs = []
for e in paragraphsEles:
    paragraphs.append(e.text)

for p in paragraphs:
    print(p)

driver.quit()

print('Successfully completed scrape script')
