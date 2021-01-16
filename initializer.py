from datetime import datetime, time
import pandas as pd
import robin_stocks as rs
import pyotp


class Initialize():
    def login(username, password):
        rs.login(username, password)
        totp  = pyotp.TOTP("My2factorAppHere").now()
        print("Current OTP:", totp)
    def stock_name(stock_name):
        stock_data = rs.stocks.get_stock_historicals(stock_name, interval="day", span="week")
        stock_historical = pd.DataFrame(stock_data)
        return stock_historical, stock_name

    def is_time_between(begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.utcnow().time()
        if datetime.utcnow().time() <= end_time and datetime.utcnow().time() >= begin_time:
            return True
        else: # crosses midnight
            return False





