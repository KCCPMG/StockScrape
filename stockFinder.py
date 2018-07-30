# Take a stock ticker symbol as input, return downloaded csv files as output

from selenium import webdriver
import time


print('Working...')


# Open automated browser
browser = webdriver.Chrome('C:\\Users\\Connor\\Python\\Python36-32\\chromedriver.exe')

# Search term for now. This will be modified to later be a true input
tick_sym = "SPY"

# Go to Yahoo Finance
browser.get('http://www.finance.yahoo.com')

# Identify search field and search button
s_field = browser.find_element('tag name', 'input')
s_button = browser.find_element_by_id('search-button')

# Enter the text into the Search field and click to search
s_field.send_keys(tick_sym)
s_button.click()
# Assuming the search went well, we are now on the stock's page

time.sleep(10)
# Get rid of "Click here to start trading: ad that blocks our information
for svg in browser.find_elements_by_tag_name('svg'):
    if svg.get_attribute('data-icon') == 'close':
        svg.click()


# Pause for all DOM to load, get to tab for historical data
time.sleep(10)

# Find and click on "Historical Data" section
for link in browser.find_elements_by_tag_name('a'):
    try:
        if link.get_attribute('href'):
            if 'history' in link.get_attribute('href'):
                link.click()
                break
    except:
        pass

time.sleep(10)

# Find and click on option to change date range
for link in browser.find_elements_by_tag_name('input'):
    try:
        if link.get_attribute('data-test') == 'date-picker-full-range':
            link.click()
            break
        else:
            continue
    except:
        print('Error when attempting to find data-test')
time.sleep(10)
for tag in browser.find_elements_by_tag_name('span'):
    try:
        if tag.get_attribute('innerHTML') == '<span>Max</span>':
            tag.click()
            break
        else:
            continue
    except:
        pass


for button in browser.find_elements_by_tag_name('button'):
    if button.get_attribute('innerHTML') == '<span>Done</span>':
        button.click()
        break

# Selecting the Frequency selector
for tag in browser.find_elements_by_tag_name('span'):
    if tag.get_attribute('innerHTML') == 'Daily':
        tag.click()
        break

# Selecting "Monthly" on the Frequency selector
for tag in browser.find_elements_by_tag_name('span'):
    if tag.get_attribute('innerHTML') == 'Monthly':
        tag.click()
        break

# Clicking the Apply button to put the search parameters in place
for button in browser.find_elements('tag name', 'button'):
    if button.get_attribute('innerHTML') == '<span>Apply</span>':
        button.click()
        break

# Downloading the CSV by clicking the link to 'Download Data'
browser.find_element_by_link_text('Download Data').click()

# Resetting the search criteria to show Dividends instead of prices

# Opening the "Show" menu
for span in browser.find_elements('tag name', 'span'):
    if span.get_attribute('innerHTML') == 'Historical Prices':
        span.click()
        break

# Clicking "Dividends Only" in the "Show" menu
for span in browser.find_elements('tag name', 'span'):
    if span.get_attribute('innerHTML') == 'Dividends Only':
        span.click()
        break


# Clicking the Apply button to put the search parameters in place
for button in browser.find_elements('tag name', 'button'):
    if button.get_attribute('innerHTML') == '<span>Apply</span>':
        button.click()
        break


# Let changes take effect
time.sleep(2)

# Downloading the CSV by clicking the link to 'Download Data'
browser.find_element_by_link_text('Download Data').click()


print('Finished.')




