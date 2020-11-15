#!/usr/bin/env python

# WS client example

# import asyncio
# import websockets
#
#
# async def hello():
#     uri = "ws://localhost:8765"
#     async with websockets.connect(uri) as websocket:
#         name = input("What's your name? ")
#
#         await websocket.send(name)
#         print(f"> {name}")
#
#         greeting = await websocket.recv()
#         print(f"< {greeting}")
#
# asyncio.get_event_loop().run_until_complete(hello())

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
from tabulate import tabulate
import json
import threading

driver_path = "C:/Git_project/selenumeTest/drivers/chromedriver.exe"


class ClientThread(threading.Thread):
    '''
        This class scrape the data from the tsetmc.ir website and return the
        data in the json format.
    '''

    def __init__(self, host, port, namad):
        threading.Thread.__init__(self)
        self.namad = namad
        self.num = len(self.namad)
        self.host = host
        self.port = port

    def scrape(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.drive = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

        self.drive.get("http://tsetmc.ir/")

        search = ''
        while search == '':
            self.drive.find_element_by_id("search").click()

            for i in self.namad:
                self.drive.find_element_by_id("SearchKey").send_keys(i)
                time.sleep(2)
                search = ''
                while search == '':
                    try:
                        search = self.drive.find_element_by_xpath(
                            '//*[@id="SearchResult"]/div/div[2]/table/tbody/tr[1]/td[1]/a')
                    except:
                        search = ''
                index = 2
                while 'نماد قدیمی' in search.text:
                    search = self.drive.find_element_by_xpath(
                        '//*[@id="SearchResult"]/div/div[2]/table/tbody/tr[' + str(index) + ']/td[1]/a')
                    index += 1
                link = search.get_attribute('href')
                self.drive.execute_script('''window.open("{}","_blank");'''.format(link))

                self.drive.find_element_by_id("SearchKey").clear()

        data = self.read()

        print(data)
        return data

    def read(self):
        windows = self.drive.window_handles
        while True:
            time.sleep(1)
            data_list = []
            for i in range(1, self.num + 1):
                self.drive.switch_to.window(windows[self.num + 1 - i])
                situation = self.drive.find_element_by_xpath('//*[@id="d01"]')

                while situation.text == '':
                    pass

                situation = situation.text

                if situation != 'ممنوع-متوقف' and situation != 'ممنوع':

                    buy_number = []
                    vol_buy = []
                    price_buy = []

                    buy_number.append([self.drive.find_element_by_xpath('//*[@id="bl"]/tr[' + str(i) + ']/td[1]') \
                                       for i in range(2, 5)])
                    vol_buy.append([self.drive.find_element_by_xpath('//*[@id="bl"]/tr[' + str(i) + ']/td[2]') \
                                    for i in range(2, 5)])
                    price_buy.append([self.drive.find_element_by_xpath('//*[@id="bl"]/tr[' + str(i) + ']/td[3]') \
                                      for i in range(2, 5)])
                    sell_number = []
                    vol_sell = []
                    price_sell = []

                    price_sell.append([self.drive.find_element_by_xpath('//*[@id="bl"]/tr[' + str(i) + ']/td[4]') \
                                       for i in range(2, 5)])
                    vol_sell.append([self.drive.find_element_by_xpath('//*[@id="bl"]/tr[' + str(i) + ']/td[5]') \
                                     for i in range(2, 5)])
                    sell_number.append([self.drive.find_element_by_xpath('//*[@id="bl"]/tr[' + str(i) + ']/td[6]') \
                                        for i in range(2, 5)])

                    lprice = self.drive.find_element_by_xpath('//*[@id="d02"]')
                    fprice = self.drive.find_element_by_xpath('//*[@id="d03"]')
                    turnover = self.drive.find_element_by_xpath('//*[@id="d09"]')

                    private_turn_buy = self.drive.find_element_by_xpath('//*[@id="e0"]')
                    legal_turn_buy = self.drive.find_element_by_xpath('//*[@id="e1"]')
                    private_turn_sell = self.drive.find_element_by_xpath('//*[@id="e3"]')
                    legal_turn_sell = self.drive.find_element_by_xpath('//*[@id="e4"]')

                    private_num_buy = self.drive.find_element_by_xpath('//*[@id="e5"]')
                    legal_num_buy = self.drive.find_element_by_xpath('//*[@id="e6"]')
                    private_num_sell = self.drive.find_element_by_xpath('//*[@id="e8"]')
                    legal_num_sell = self.drive.find_element_by_xpath('//*[@id="e9"]')

                    min_price = self.drive.find_element_by_xpath('//*[@id="d07"]')
                    max_price = self.drive.find_element_by_xpath('//*[@id="d06"]')

                    buy_number = [buy_number[0][i].text for i in range(3)]
                    buy_number = [int(re.sub(r',', '', i).strip()) if i != ' ' else 0 for i in buy_number]
                    bn = buy_number
                    vol_buy = [vol_buy[0][i].text for i in range(3)]
                    vol_buy = [int(re.sub(r',', '', i).strip()) if i != ' ' else 0 for i in vol_buy]
                    vb = vol_buy
                    price_buy = [price_buy[0][i].text for i in range(3)]
                    price_buy = [int(re.sub(r',', '', i).strip()) if i != ' ' else 0 for i in price_buy]
                    pb = price_buy
                    sell_number = [sell_number[0][i].text for i in range(3)]
                    sell_number = [int(re.sub(r',', '', i).strip()) if i != ' ' else 0 for i in sell_number]
                    sn = sell_number
                    vol_sell = [vol_sell[0][i].text for i in range(3)]
                    vol_sell = [int(re.sub(r',', '', i).strip()) if i != ' ' else 0 for i in vol_sell]
                    vs = vol_sell
                    price_sell = [price_sell[0][i].text for i in range(3)]
                    price_sell = [int(re.sub(r',', '', i).strip()) if i != ' ' else 0 for i in price_sell]
                    ps = price_sell

                    lp = lprice.text.split()
                    last_price = int(re.sub(r',', '', lp[0]).strip())
                    fp = fprice.text.split()
                    final_price = int(re.sub(r',', '', fp[0]).strip())
                    try:
                        state = self.drive.find_element_by_xpath('//*[@id="d02"]/span[2]')
                        state_lp = state.get_attribute('style')

                        lp = lprice.text.split()
                        lp_shakhes = int(re.sub(r',', '', lp[1]).strip())
                        try:
                            lp_percent = float(re.findall(r'\d+\W\d+', lp[2])[0])
                        except:
                            lp_percent = float(re.findall(r'\d', lp[2])[0])

                        if 'red' in state_lp:
                            lp_percent = -1 * lp_percent
                            lp_shakhes = -1 * lp_shakhes

                        state = self.drive.find_element_by_xpath('//*[@id="d03"]/span')
                        state_fp = state.get_attribute('style')

                        fp_shakhes = int(re.sub(r',', '', fp[1]).strip())
                        try:
                            fp_percent = float(re.findall(r'\d+\W\d+', fp[2])[0])
                        except:
                            fp_percent = float(re.findall(r'\d', fp[2])[0])

                        if 'red' in state_fp:
                            fp_percent = -1 * fp_percent
                            fp_shakhes = -1 * fp_shakhes
                    except:
                        lp_shakhes = 0
                        lp_percent = 0
                        fp_shakhes = 0
                        fp_percent = 0

                    turnover = turnover.text

                    min_price = min_price.text.split()
                    min_price = [int(re.sub(r',', '', i).strip()) for i in min_price]
                    min_price = int(min_price[0])
                    max_price = max_price.text.split()
                    max_price = [int(re.sub(r',', '', i).strip()) for i in max_price]
                    max_price = int(max_price[0])

                    try:
                        private_turn_buy = private_turn_buy.text.split()
                        ptb = private_turn_buy
                        ptb[0] = re.sub(',', '', ptb[0])
                        if len(ptb) == 3:
                            try:
                                private_turn_buy_percent = float(re.findall(r'\d+\W\d+', ptb[2])[0])
                            except:
                                private_turn_buy_percent = float(re.findall(r'\d+', ptb[2])[0])
                            pvb_hajm = str(ptb[0]) + str(ptb[1])
                        else:
                            try:
                                private_turn_buy_percent = float(re.findall(r'\d+\W\d+', ptb[1])[0])
                            except:
                                private_turn_buy_percent = float(re.findall(r'\d+', ptb[1])[0])
                            pvb_hajm = str(ptb[0])
                        ptbp = private_turn_buy_percent

                        legal_turn_buy = legal_turn_buy.text.split()
                        ltb = legal_turn_buy
                        ltb[0] = re.sub(',', '', ltb[0])
                        if len(ltb) == 3:
                            try:
                                legal_turn_buy_percent = float(re.findall(r'\d+\W\d+', ltb[2])[0])
                            except:
                                legal_turn_buy_percent = float(re.findall(r'\d+', ltb[2])[0])
                            lvb_hajm = str(ltb[0]) + str(ltb[1])
                        else:
                            try:
                                legal_turn_buy_percent = float(re.findall(r'\d+\W\d+', ltb[1])[0])
                            except:
                                legal_turn_buy_percent = float(re.findall(r'\d+', ltb[1])[0])
                            lvb_hajm = str(ltb[0])
                        ltbp = legal_turn_buy_percent

                        private_turn_sell = private_turn_sell.text.split()
                        pts = private_turn_sell
                        pts[0] = re.sub(',', '', pts[0])
                        if len(pts) == 3:
                            try:
                                private_turn_sell_percent = float(re.findall(r'\d+\W\d+', pts[2])[0])
                            except:
                                private_turn_sell_percent = float(re.findall(r'\d+', pts[2])[0])
                            pvs_hajm = str(pts[0]) + str(pts[1])
                        else:
                            try:
                                private_turn_sell_percent = float(re.findall(r'\d+\W\d+', pts[1])[0])
                            except:
                                private_turn_sell_percent = float(re.findall(r'\d+', pts[1])[0])
                            pvs_hajm = str(pts[0])
                        ptsp = private_turn_sell_percent

                        legal_turn_sell = legal_turn_sell.text.split()
                        lts = legal_turn_sell
                        lts[0] = re.sub(',', '', lts[0])
                        if len(lts) == 3:
                            try:
                                legal_turn_sell_percent = float(re.findall(r'\d+\W\d+', lts[2])[0])
                            except:
                                legal_turn_sell_percent = float(re.findall(r'\d+', lts[2])[0])
                            lvs_hajm = str(lts[0]) + str(lts[1])
                        else:
                            try:
                                legal_turn_sell_percent = float(re.findall(r'\d+\W\d+', lts[1])[0])
                            except:
                                legal_turn_sell_percent = float(re.findall(r'\d+', lts[1])[0])
                            lvs_hajm = str(lts[0])
                        ltsp = legal_turn_sell_percent

                        private_num_buy = private_num_buy.text.split()
                        private_num_buy = [int(re.sub(r',', '', i).strip()) for i in private_num_buy]
                        pnb = int(private_num_buy[0])
                        legal_num_buy = legal_num_buy.text.split()
                        legal_num_buy = [int(re.sub(r',', '', i).strip()) for i in legal_num_buy]
                        lnb = int(legal_num_buy[0])
                        private_num_sell = private_num_sell.text.split()
                        private_num_sell = [int(re.sub(r',', '', i).strip()) for i in private_num_sell]
                        pns = int(private_num_sell[0])
                        legal_num_sell = legal_num_sell.text.split()
                        legal_num_sell = [int(re.sub(r',', '', i).strip()) for i in legal_num_sell]
                        lns = int(legal_num_sell[0])
                    except:
                        pnb = 0
                        ptbp = 0
                        pvb_hajm = 0
                        lnb = 0
                        ltbp = 0
                        lvb_hajm = 0
                        pns = 0
                        ptsp = 0
                        pvs_hajm = 0
                        lns = 0
                        ltsp = 0
                        lvs_hajm = 0

                    #                    print('\nنماد %s %s می باشد.' % (self.namad[i - 1], situation))
                    #                    print('\n')
                    #                    print('آخرین قیمت: %i  تاثیر شاخص: %i  درصد: %s' % (last_price, lp_shakhes, str(lp_percent)))
                    #                    print('قیمت پایانی: %i  تاثیر شاخص: %i  درصد: %s' % (final_price, fp_shakhes, str(fp_percent)))
                    #
                    #                    print('حجم معاملات: %s' % turnover)
                    #                    print('\n')
                    #                    print('بازه قیمت: کمترین: %i   بیشترین: %i' % (min_price, max_price))
                    #                    print('\n')
                    #                    print(tabulate([['Private', pnb, ptbp, pvb_hajm], ['Legal', lnb, ltbp, lvb_hajm]], \
                    #                                   headers=['Buy', 'Number', 'Precent', 'Turn'], tablefmt='orgtbl'))
                    #                    print('\n')
                    #                    print(tabulate([['Private', pns, ptsp, pvs_hajm], ['Legal', lns, ltsp, lvs_hajm]], \
                    #                                   headers=['Sell', 'Number', 'Precent', 'Turn'], tablefmt='orgtbl'))
                    #                    print('\n')
                    #                    print(tabulate(
                    #                        [[ps[0], vs[0], sn[0], pb[0], vb[0], bn[0]], [ps[1], vs[1], sn[1], pb[1], vb[1], bn[1]],
                    #                         [ps[2], vs[2], sn[2], pb[2], vb[2], bn[2]]], \
                    #                        headers=['Number', 'Turn', 'Price', 'Price', 'Turn', 'Number'], tablefmt='orgtbl'))
                    #                    print('#' * 80)

                    data = {"Name": self.namad[i - 1], "State": situation, "Last price": last_price,
                            "Last shakhes": lp_shakhes,
                            "Last_percent": lp_percent,
                            "Final price": last_price, "Final shakhes": lp_shakhes, "Final percent": lp_percent,
                            "Turnover": turnover, "Min price": min_price, "Max price": max_price, "pnb": pnb,
                            "ptbp": ptbp, "pvb_hajm": pvb_hajm, "lnb": lnb, "ltbp": ltbp, "lvb_hajm": lvb_hajm,
                            "pns": pns, "ptsp": ptsp, "pvs_hajm": pvs_hajm, "lns": lns, "ltsp": ltsp,
                            "lvs_hajm": lvs_hajm}
                    for i in range(3):
                        data["price_sell" + str(i)] = str(ps[i])
                        data["volume_sell" + str(i)] = str(vs[i])
                        data["number_sell" + str(i)] = str(sn[i])
                        data["price_buy" + str(i)] = str(pb[i])
                        data["volume_buy" + str(i)] = str(vb[i])
                        data["number_buy" + str(i)] = str(bn[i])

                    data_list.append(data)

                else:
                    #                    print('\nنماد %s ممنوع (متوقف) می باشد.' % self.namad[i - 1])
                    data = {"Name": self.namad[i - 1], "State": "ممنوع"}
                    data_list.append(data)

                time.sleep(0.1)

            data_list = json.dumps(data_list)
            return data_list
