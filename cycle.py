from selenium import webdriver
import stockScraper
import symbolSearcher
import sqlManager
import os


def move_csv(symbol, start_folder='C:\\Users\\Connor\\Downloads',
             destination_folder='C:\\Users\\Connor\\PycharmProjects\\StockScrape\\Downloads\\'):
    # find all files in this folder that start with the symbol
    os.chdir(start_folder)
    files_to_move = []
    for file in os.listdir():
        if file.startswith(symbol):
            files_to_move.append(file)
    # move all files to destination folder
    for file in files_to_move:
        os.rename(file, destination_folder + file)


def process_csv(file):
    fhand = open(file, 'r')
    first_line = fhand.readline()
    content = fhand.readlines()
    if first_line == 'Date,Dividends\n':
        return dividend_content_dict(content)
    elif first_line == 'Date,Open,High,Low,Close,Adj Close,Volume\n':
        return history_content_dict(content)
    else:
        return


# Returns word 'dividend' to identify type, dictionary with date, dividend amount
def dividend_content_dict(content):
    dict_out = {}
    for line in content:
        line = line.split(',')
        date = line[0].replace('-', '')
        dict_out[date] = line[1].strip()
    return 'dividends', dict_out


# Returns word 'assets' to identify type, dictionary with date, adj. close
def history_content_dict(content):
    dict_out = {}
    for line in content:
        line = line.split(',')
        date = line[0].replace('-', '')
        dict_out[date] = line[-2].strip()
    return 'history', dict_out


def move_and_process(symbol, sql_manager, start_folder='C:\\Users\\Connor\\Downloads',
                     destination_folder='C:\\Users\\Connor\\PycharmProjects\\StockScrape\\Downloads\\'):
    move_csv(symbol, start_folder, destination_folder)
    os.chdir(destination_folder)
    for file in os.listdir():
        if file.startswith(symbol):
            asset_data = process_csv(file)
            if asset_data[0] == 'history':
                sql_manager.populate_asset_history(asset_data[1], symbol)
            elif asset_data[0] == 'dividends':
                sql_manager.populate_dividend_history(asset_data[1], symbol)
            os.remove(file)








# prompt for text file
f_loc = input('Please enter a file location: ')
input_list = []
print('Working...')
for line in open(f_loc, 'r'):
    input_list.append(line.strip())

# create list from text file, print out both results
valid_list, invalid_list = symbolSearcher.get_valid_symbols(input_list, output_incorrect=True)
print("Valid ticker symbol list: ", valid_list)
print("Invalid ticker symbol list (consider revising): ", invalid_list)
if input("Proceed? (y/n) ") == 'n':
    quit()

browser = webdriver.Chrome('C:\\Users\\Connor\\Python\\Python36-32\\chromedriver.exe')
sqlm = sqlManager.SQLManager()



for ticker in valid_list:
    stockScraper.scrape_stock(browser, ticker)
    move_and_process(ticker, sqlm)
browser.close()

print('Finished')
