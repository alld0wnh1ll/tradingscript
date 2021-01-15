from datetime import datetime, time
from time import sleep
import pandas as pd
import robin_stocks as rs
import pyotp


rs.login("username", "password")
totp  = pyotp.TOTP("My2factorAppHere").now()
print("Current OTP:", totp)
Ford_data = rs.stocks.get_stock_historicals("F", interval="day", span="week")
Ford_historical = pd.DataFrame(Ford_data)


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if datetime.utcnow().time() <= end_time and datetime.utcnow().time() >= begin_time:
        return True
    else: # crosses midnight
        return False
print(datetime.utcnow().time())

stock_name = "Ford:"
stock_yesterday = stock_name + " yesterday"


while True:
    endtime = str(datetime.utcnow().time()).split(":")
    endtime = int(endtime[0])

    if endtime > 21 or endtime < 14:
        today_price = float(rs.stocks.get_latest_price('F', includeExtendedHours=True)[0])
        print(stock_name, today_price)
    else:
        price_yesterday = float(Ford_historical.iloc[-1]['close_price'])
        print(stock_yesterday, price_yesterday)
    while is_time_between(time(14, 31), time(20, 59)) is True:
        try:
            today_price = float(rs.stocks.get_latest_price('F', includeExtendedHours=True)[0])
            print(stock_name, today_price)


            if today_price*1.005 <= price_yesterday:
                try:

                    rs.orders.order_buy_market('F', 1, timeInForce='gfd', priceType='ask_price', extendedHours=False)


                    print("1 SHARE BOUGHT BECAUSE PRICE DROPPED MORE THAN .5%, YESTERDAY'S DIFFERENCE: {} TODAY'S DIFFERENCE: {} PERCENTAGE CHANGE: {}%\n".format(price_yesterday, today_price, ((today_price/price_yesterday - 1))*100))
                    #sleep(43200)
                    today_price = float(rs.stocks.get_latest_price('F', includeExtendedHours=True)[0])
                    price_yesterday = today_price
                except Exception as e:
                    print("Error placing orders:", e)
                    sleep(15)



            else:
                print("STILL WAITING, Last Price: {} TODAY'S Price: {} PERCENTAGE CHANGE: {}%\n".format(price_yesterday, today_price, ((today_price/price_yesterday - 1))*100))
                sleep(15)
        except Exception as e:
            print("Error fetching latest prices:", e)
            sleep(15)
    else:
        print("not time yet")
        sleep(15)

