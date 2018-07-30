import sqlite3
import assetMath


class SQLManager(object):

    def __init__(self):
        self.conn = sqlite3.connect('C:\\Users\\Connor\\PycharmProjects\\StockScrape\\Assets.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS Histories '
                       '(Date int)')
        self.c.execute('CREATE TABLE IF NOT EXISTS Dividends '
                       '(Date int)')
        self.conn.commit()
        print('Connection established')

    def add_history_column(self, col_name, type_str):
        self.c.execute('PRAGMA table_info("Histories")')
        history = self.c.fetchall()
        for header in history:
            for attr in header:
                if attr == col_name:
                    return
        exec_str = 'ALTER TABLE Histories ADD ' + col_name + ' ' + type_str
        self.c.execute(exec_str)
        self.conn.commit()

    def add_dividend_column(self, col_name, type_str):
        self.c.execute('PRAGMA table_info("Dividends")')
        history = self.c.fetchall()
        for header in history:
            for attr in header:
                if attr == col_name:
                    return
        exec_str = 'ALTER TABLE Dividends ADD ' + col_name + \
                   ' ' + type_str
        self.c.execute(exec_str)
        self.conn.commit()

    def populate_asset_history(self, dict_in, asset_name):
        self.add_history_column(asset_name, 'float')
        self.c.execute('SELECT Date FROM Histories')
        all_dates = self.c.fetchall()
        for i in range(len(all_dates)):
            all_dates[i] = all_dates[i][0]
        for date in list(dict_in.keys()):
            formatted_date = date.replace('-', '')
            formatted_date = int(formatted_date)
            if formatted_date not in all_dates:
                self.c.execute('INSERT INTO Histories '
                               '(Date) VALUES (?)',
                               (formatted_date,))
        self.conn.commit()
        for entry in dict_in:
            date_int = entry.replace('-', '')
            date_int = int(date_int)
            exec_str = 'UPDATE Histories SET ' + asset_name + \
                       ' = ' + str(dict_in[entry]) \
                + ' WHERE Date = ' + str(date_int)
            self.c.execute(exec_str)
        self.conn.commit()

    def populate_dividend_history(self, dict_in, asset_name):
        self.add_dividend_column(asset_name, 'float')
        self.c.execute('SELECT Date FROM Dividends')
        all_dates = self.c.fetchall()
        for i in range(len(all_dates)):
            all_dates[i] = all_dates[i][0]
        for date in list(dict_in.keys()):
            formatted_date = date.replace('-', '')
            formatted_date = int(date)
            if formatted_date not in all_dates:
                self.c.execute('INSERT INTO Dividends '
                               '(Date) VALUES (?)',
                               (str(formatted_date),))
        self.conn.commit()
        for entry in dict_in:
            date_int = entry.replace('-', '')
            date_int = int(date_int)
            exec_str = 'UPDATE Dividends SET ' + asset_name + ' = ' + str(dict_in[entry]) \
                + ' WHERE Date = ' + str(date_int)
            self.c.execute(exec_str)
        self.conn.commit()

    def fetch_asset_names(self):
        self.c.execute('PRAGMA table_info(Histories)')
        headers_data = self.c.fetchall()
        headers_data = headers_data[1:]
        headers = []
        for hd in headers_data:
            headers.append(hd[1])
        return headers

    def fetch_asset_history(self, asset_name):
        exec_str = 'SELECT Date, ' + asset_name + \
                   ' FROM Histories'
        self.c.execute(exec_str)
        return self.c.fetchall()

    # fetch gains, return [asset_name, {date : gain, date : gain...}]
    def fetch_asset_gains(self, asset_name):
        exec_str = 'SELECT Date, ' + asset_name + \
                   ' FROM Gains'
        self.c.execute(exec_str)
        gains_dict = {}
        for tup in self.c.fetchall():
            if tup[1] is not None:
                gains_dict[tup[0]] = tup[1]
        return [asset_name, gains_dict]

    def populate_gains(self):
        # Create table
        self.c.execute('CREATE TABLE IF NOT EXISTS Gains ' +
                       '(Date int)')
        self.conn.commit()

        # Get names of assets from Histories
        assets = self.fetch_asset_names()

        self.c.execute('PRAGMA table_info(Gains)')
        existing_assets = [i[1] for i in self.c.fetchall()][1:]

        # Populate asset headers in gains
        for asset in assets:
            if asset not in existing_assets:
                self.c.execute('ALTER TABLE Gains ADD COLUMN '
                               + asset + ' float')

        for asset in assets:
            # Getting history as list of tuples (date, price)
            history = self.fetch_asset_history(asset)

            # Modifying history to only get 1st date of year
            history = [i for i in history if (i[0]-101) % 10000 == 0]
            # Now eliminating None points
            history = [i for i in history if i[1] is not None]

            # Creating the gains table
            gains = assetMath.percentages_table(history)
            # Getting all dates to populate as we go
            self.c.execute('SELECT Date FROM Gains')
            existing_dates = [i[0] for i in self.c.fetchall()]

            for point in gains:
                if point[0] not in existing_dates:
                    self.c.execute('INSERT INTO Gains (Date) ' +
                                   'VALUES (' + str(point[0]) +
                                   ')')
                self.c.execute('UPDATE Gains SET ' + asset +
                               ' = ' + str(point[1]) +
                               ' WHERE Date = ' + str(point[0]))
            self.conn.commit()

    # This is all wrong
    # def create_covariance_table(self, year):
    #     # Get usable date int out of year
    #     date = year * 10000 + 10101
    #
    #     self.c.execute('SELECT Date from GAINS')
    #     all_dates = [i[0] for i in self.c.fetchall()]
    #     if date not in all_dates:
    #         return
    #
    #     self.c.execute('SELECT * FROM GAINS WHERE DATE = ' + str(date))
    #     values = self.c.fetchall()[0]
    #
    #     self.c.execute('PRAGMA table_info(Gains)')
    #     headers = [i[1] for i in self.c.fetchall()]
    #
    #     # Getting headers that have values for the date only
    #     valid_headers = [headers[i] for i in range(len(values)) if values[i] is not None]
    #     # Assets are all valid headers except date, which comes first in valid_headers
    #     assets = valid_headers[1:]
    #
    #     # create table, first row, headers
    #     table_name = 'Covariance_' + str(year)
    #     self.c.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' (Asset varchar)')
    #     self.conn.commit()
    #     for asset in assets:
    #         self.c.execute('INSERT INTO ' + table_name + ' (Asset) VALUES ("' + asset + '")')
    #     self.conn.commit()
    #     for asset in assets:
    #         self.c.execute('ALTER TABLE ' + table_name + ' ADD COLUMN ' + asset + (' float'))
    #     self.conn.commit()
    #
    #     # Not completed

    def create_correlation_coefficient_table(self):
        # Get headers
        self.c.execute('PRAGMA table_info(Gains)')
        assets = [i[1] for i in self.c.fetchall()][1:]
        self.c.execute('CREATE TABLE IF NOT EXISTS Correlation_Coefficient (Asset varchar)')
        self.c.execute('PRAGMA table_info(Correlation_Coefficient)')
        existing_headers = [i[1] for i in self.c.fetchall()]
        self.conn.commit()
        # Populate the table
        for asset in assets:
            if asset not in existing_headers:
                self.c.execute('INSERT INTO Correlation_Coefficient (Asset) VALUES ("' + asset + '")')
                self.c.execute('ALTER TABLE Correlation_Coefficient ADD COLUMN ' + asset + ' float')
                self.conn.commit()
        for asset in assets:
            for other_asset in assets:
                dict_a = self.fetch_asset_gains(asset)[1]
                dict_b = self.fetch_asset_gains(other_asset)[1]
                a_dates = list(dict_a.keys())
                b_dates = list(dict_b.keys())
                for date in a_dates:
                    if date not in b_dates:
                        del dict_a[date]
                for date in b_dates:
                    if date not in a_dates:
                        del dict_b[date]
                cor = assetMath.sample_correlation_coefficient(dict_a, dict_b)
                self.c.execute("UPDATE Correlation_Coefficient SET " + asset + " = "
                               + str(cor) + " WHERE Asset = '" + other_asset + "'")
                self.conn.commit()

    def quit(self):
        self.conn.close()


sqlm = SQLManager()
sqlm.create_correlation_coefficient_table()

#### Next Step is to export all SQL tables to csvs to give to Dad to read and we can review the math




