from datetime import datetime, time
from time import sleep
import robin_stocks as rs
from initializer import Initialize


stocks = ['F','KO', 'T']

if __name__ == '__main__':
    l = Initialize
    l.login('username', 'password')
    while True:
        for i in stocks:
            stock_info = l.stock_name(i)
            endtime = str(datetime.utcnow().time()).split(":")
            endtime = int(endtime[0]) 
            print(endtime)
            if endtime > 21 or endtime < 14:
                today_price = float(rs.stocks.get_latest_price(stock_info[1], includeExtendedHours=True)[0])
                print(stock_info[1], today_price)
            else:
                price_yesterday = float(stock_info[0].iloc[-1]['close_price'])
                print(stock_info[1] + ' yesterday: ', price_yesterday)
            if l.is_time_between(time(14, 31), time(20, 59)) is True:
                try:
                    today_price = float(rs.stocks.get_latest_price(stock_info[1], includeExtendedHours=True)[0])
                    print(stock_info[1], today_price)
                    if today_price * 1.005 <= price_yesterday:
                        try:
                            rs.orders.order_buy_market(stock_info[1], 1, timeInForce='gfd', priceType='ask_price',
                                                       extendedHours=False)
                            print(
                                "1 SHARE BOUGHT BECAUSE PRICE DROPPED MORE THAN .5%, LAST PRICE'S DIFFERENCE: {} TODAY'S DIFFERENCE: {} PERCENTAGE CHANGE: {}%\n".format(
                                    price_yesterday, today_price, ((today_price / price_yesterday - 1)) * 100))
                            # sleep(43200)
                            today_price = float(rs.stocks.get_latest_price(stock_info[1], includeExtendedHours=True)[0])
                            price_yesterday = today_price
                        except Exception as e:
                            print("Error placing orders:", e)
                            sleep(15/len(stocks))
                    else:
                        print("STILL WAITING, Last Price: {} TODAY'S Price: {} PERCENTAGE CHANGE: {}%\n".format(
                            price_yesterday, today_price, ((today_price / price_yesterday - 1)) * 100))
                        sleep(15/len(stocks))
                except Exception as e:
                    print("Error fetching latest prices:", e)
                    sleep(15/len(stocks))
            else:
                print("Market is closed!")
                sleep(15/len(stocks))
