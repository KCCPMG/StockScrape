import time
from selenium.common import exceptions


# Setting up methods to re-use to continually scrape for stocks

# Take a stock symbol and convert it into a url address the browser can use
def get_stock_url(symbol):
    return 'https://finance.yahoo.com/quote/%s?p=%s' % (symbol, symbol)


# Directs an already open webdriver to a specific url
def open_page(browser, url):
    browser.get(url)


# Close out the pop-up ad that blocks the historical data selector
def clear_trading_ad(browser):
    try:
        for svg in browser.find_elements_by_tag_name('svg'):
            if svg.get_attribute('data-icon') == 'close':
                svg.click()
                move_on = True
                break
    except exceptions.StaleElementReferenceException:
        pass
    time.sleep(2)


def select_historical_data(browser):
    try:
        for link in browser.find_elements_by_tag_name('a'):
            if link.get_attribute('href'):
                if 'history' in link.get_attribute('href'):
                    link.click()
                    break
    except exceptions.StaleElementReferenceException:
        select_historical_data(browser)
    time.sleep(2)


def maximize_data_range(browser):
    # Open date range
    move_on = False
    while move_on is False:
        try:
            for link in browser.find_elements_by_tag_name('input'):
                if link.get_attribute('data-test') == 'date-picker-full-range':
                    link.click()
                    move_on = True
                    break
                else:
                    continue
        except exceptions.StaleElementReferenceException:
            pass

    # Select "Max" time
    move_on = False
    while move_on is False:
        try:
            for tag in browser.find_elements_by_tag_name('span'):
                if tag.get_attribute('innerHTML') == '<span>Max</span>':
                    tag.click()
                    move_on = True
                    break
                else:
                    continue
        except exceptions.StaleElementReferenceException:
            pass

    # Click 'Done'
    move_on = False
    while move_on is False:
        try:
            for button in browser.find_elements_by_tag_name('button'):
                if button.get_attribute('innerHTML') == '<span>Done</span>':
                    button.click()
                    move_on = True
                    break
                else:
                    continue
        except exceptions.StaleElementReferenceException:
            pass
    time.sleep(2)


def set_monthly_frequency(browser):
    # Select frequency dropdown
    try:
        for tag in browser.find_elements_by_tag_name('span'):
            if tag.get_attribute('innerHTML') == 'Daily':
                tag.click()
                break
    except exceptions.StaleElementReferenceException:
        set_monthly_frequency(browser)

    # Select 'Monthly'
    for tag in browser.find_elements_by_tag_name('span'):
        if tag.get_attribute('innerHTML') == 'Monthly':
            tag.click()
            break
    time.sleep(2)


def apply_parameters(browser):
    # Click 'Apply' button to update data in accordance with selected items
    for button in browser.find_elements('tag name', 'button'):
        if button.get_attribute('innerHTML') == '<span>Apply</span>':
            button.click()
            break
    time.sleep(2)


def download_data(browser):
    # Click 'Download Data' link
    browser.find_element_by_link_text('Download Data').click()
    time.sleep(2)


def set_to_dividends(browser):
    # Opening the "Show" menu
    for span in browser.find_elements('tag name', 'span'):
        if span.get_attribute('innerHTML') == 'Historical Prices':
            span.click()
            break
    time.sleep(2)

    # Clicking "Dividends Only" in the "Show" menu
    for span in browser.find_elements('tag name', 'span'):
        if span.get_attribute('innerHTML') == 'Dividends Only':
            span.click()
            break
    time.sleep(2)


# main method to get everything
def scrape_stock(browser, sym):
    open_page(browser, get_stock_url(sym))
    clear_trading_ad(browser)
    select_historical_data(browser)
    maximize_data_range(browser)
    set_monthly_frequency(browser)
    apply_parameters(browser)
    download_data(browser)
    set_to_dividends(browser)
    apply_parameters(browser)
    download_data(browser)
    time.sleep(2)


