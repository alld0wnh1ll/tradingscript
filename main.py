from datetime import datetime, time
from time import sleep
import pandas as pd
import robin_stocks as rs
import pyotp


rs.login("username", "password")
totp  = pyotp.TOTP("My2factorAppHere").now() #this keeps you from getting logged out
print("Current OTP:", totp)
Ford_data = rs.stocks.get_stock_historicals("F", interval="day", span="week") #retrieve historical data on desired stock
Ford_historical = pd.DataFrame(Ford_data)


def is_time_between(begin_time, end_time, check_time=None): #creates a function for the program to know when the market is open 
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if datetime.utcnow().time() <= end_time and datetime.utcnow().time() >= begin_time:
        return True
    else: # crosses midnight
        return False
print(datetime.utcnow().time())

#Below, I embedded two while loops (N^2). The top level while just keeps updating yesterday's closed price and today's current price; this allows you to stay up to date during
#the after-market; When market time hits as per second while loop (14 31 GMT); the second loop will commence and will continuously update the days price; when you purchase a share
#after the stock falls below .5%, the price_yesterday variable gets updated with the price you purchased the share at; so as it falls another .5%, you will purchase another share
#this also prevents the script in going into an endless buy frenzy.


while True:
    price_yesterday = float(Ford_historical.iloc[-1]['close_price'])
    print("Ford Yesterday:",price_yesterday)
    while is_time_between(time(14, 31), time(20, 59)) is True:
        try:
            Ford_today = float(rs.stocks.get_latest_price('F', includeExtendedHours=True)[0])
            print("Ford today:", Ford_today)


            if Ford_today*1.005 <= price_yesterday:
                try:

                    rs.orders.order_buy_market('F', 1, timeInForce='gfd', priceType='ask_price', extendedHours=False)


                    print("1 SHARE BOUGHT BECAUSE PRICE DROPPED MORE THAN .5%, YESTERDAY'S DIFFERENCE: {} TODAY'S DIFFERENCE: {} PERCENTAGE CHANGE: {}%\n".format(price_yesterday, Ford_today, ((Ford_today/price_yesterday - 1))*100))
                    #sleep(43200)
                    Ford_today = float(rs.stocks.get_latest_price('F', includeExtendedHours=True)[0])
                    price_yesterday = Ford_today
                except Exception as e:
                    print("Error placing orders:", e)
                    sleep(15)



            else:
                print("STILL WAITING, YESTERDAY'S Price: {} TODAY'S Price: {} PERCENTAGE CHANGE: {}%\n".format(price_yesterday, Ford_today, ((Ford_today/price_yesterday - 1))*100))
                sleep(15)
        except Exception as e:
            print("Error fetching latest prices:", e)
            sleep(15)
    else:
        print("not time yet")
        Ford_today = float(rs.stocks.get_latest_price('F', includeExtendedHours=True)[0])
        price_yesterday = float(Ford_historical.iloc[-1]['close_price'])
        print("Ford today:", Ford_today)
        sleep(15)

