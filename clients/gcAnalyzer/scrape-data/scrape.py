from selenium import webdriver

print('Starting scrape script')

# TODO use a relative instead of this absolute path
DRIVER_PATH = "/Users/steven/Documents/personal/projects/text-analyzer/lib/webdrivers/geckodriver"
driver = webdriver.Firefox(executable_path=DRIVER_PATH)
driver.get('https://lds.org')

driver.close()

print('Successfully completed scrape script')
