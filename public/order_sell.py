import requests
import time
import efinance as ef
import datetime


# 获取今天的日期
today = datetime.date.today()
today_date = today.strftime("%Y%m%d")
# print(today_date)
times = str(round((time.time()) * 1000))
zjzh = '231140300000054491'  # 组合ID
# print(zjzh)
# print(zjzh)
userid = "1687456732613796"  # 用户ID


def position_order():  # 需要拿到秒级数据判断给出卖的信号
    # buy_signal=[{'time': '14:53:07', 'code': '001255', 'name': '博菲电气', 'Price': '43.99', 'buy_je': 116, 'zdf': '4.66', 'zj_msg': '主力净流入额市场排名892/5150，占流通市值比例0.53%；今日净流入较近5日净流入的均值增加112.31万元。'}]
    # stkCode=buy_signal[0]["code"]#"300814"#股票ID
    # price=buy_signal[0]["Price"]#"21.87"#股价
    # wtsl = "100"  # 买入数量
    # 查询持仓信息
    position_code = []
    position_order_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_hold&reqUserid=&recIdx=0&recCnt=100&_=" + times
    position_order = requests.get(position_order_url).json()
    # print(position_order["data"])
    # print(position_order["data"][0])
    sell_list = []
    sell_code_list = []
    for a in range(len(position_order["data"])):
        if int(position_order["data"][a]["kysl"]) > 0:  # 在持仓中查询可用持仓
            sell_list.append(position_order["data"][a])
            sell_code_list.append(position_order["data"][a]["stkCode"])
        else:
            pass
            # print("进入买入"+"股票code："+position_order["data"][a]["stkCode"],"股票名称："+position_order["data"][a]["stkName"],"持仓数量："+position_order["data"][a]["kysl"],"浮动盈亏比："+position_order["data"][a]["rateMax"],)
    # print(sell_list)
    # print(sell_code_list)
    return sell_code_list, sell_list

def registration_oeder():
    #查看挂单信息
    registration_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_orders_cancel&reqUserid=&recIdx=0&recCnt=100&_=1681635713685"
    registration = requests.get(registration_url).json()
    # print(registration)
    cancel_oeder_lis=[]
    cancel_list=[]
    for a in range(len(registration["data"])):
        cancel_list.append(registration["data"][a])
        cancel_oeder_lis.append(registration["data"][a]["stkCode"])
    return cancel_oeder_lis,cancel_list


def sell_order():
    sell_code_list = position_order()[0]  # 获取卖出的code
    # sell_code_list=['000404','000521']
    # print(sell_code_list)
    sell_list = position_order()[1]  # 获取卖出去的所有信息
    # sell_list=[{'cbj': '6.360', 'drsl': '0', 'fdyk': '-10.01', 'fullcode': '65792', 'kysl': '100', 'ljcbyk': '-10.01', 'mktVal': '626.00', 'newPrc': '6.26', 'prePrc': '0.00', 'qljcbyk': '0.00', 'rateMax': '-1.57', 'stkCode': '000404', 'stkName': '长虹华意', 'zqlb': '6', 'zqsl': '100'}, {'cbj': '6.500', 'drsl': '0', 'fdyk': '-0.01', 'fullcode': '84032', 'kysl': '100', 'ljcbyk': '-0.01', 'mktVal': '650.00', 'newPrc': '6.50', 'prePrc': '0.00', 'qljcbyk': '0.00', 'rateMax': '-0.00', 'stkCode': '000521', 'stkName': '长虹美菱', 'zqlb': '6', 'zqsl': '100'}]
    # print(sell_list)
    real_data = ef.stock.get_quote_history(sell_code_list, beg=today_date, end=today_date, klt=1)
    # print(real_data,type(real_data))
    for i, a_mun in zip(sell_code_list, range(len(sell_code_list))):
        df = real_data[i]
        if len(df.index) != 0:
            df.rename(columns={'股票代码': 'code', '日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low',
                               '成交量': 'volume', '成交额': 'pay', '振幅': 'zf', '涨跌幅': 'zdf', '涨跌额': 'zde', '换手率': 'hsl',
                               }, inplace=True)  ##修改列名
        # print(df.tail(1))
        # print(a_mun)
        # print(df.tail(1).iloc[0].iat[4])
        # print(sell_list[a_mun]["cbj"])
        new_close = df.tail(1).iloc[0].iat[4]  # 获取现价
        cost_price = sell_list[a_mun]["cbj"]  # 获取成本价
        new_high = df.tail(1).iloc[0].iat[5]  # 获取最高价
        holding_quantity = sell_list[a_mun]["kysl"]  # 获取持仓数量
        #卖出
        if float(new_close) < float(cost_price) - 0.1:
            print("小于成本价一个点", i)
            # 卖出下单
            sell_order_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_order&mmfx=2&mktCode=0&stkCode=" + i + "&price=" + str(
                new_close) + "&wtsl=" + holding_quantity + "&r=3429902&_=" + times
            sell_order_data = requests.get(sell_order_url).json()
            if sell_order_data["result"] == 0:
                # print(sell_order_data)
                print("委托卖出：" + "股票名称：" + sell_list[a_mun]["stkName"], "委托价：" + str(new_close),
                      "成本价：" + str(cost_price), "委托数量：" + holding_quantity, "订单ID：" + sell_order_data["wth"])
            else:
                pass

                # print(sell_order_data["message"])
        elif float(new_close) > float(cost_price):
            if float(new_close) > float(cost_price) + 0.3:
                print("大于成本价3个点", i)
                if float(new_high) > float(new_close) - 2:
                    print("回调2个点", i)
                    # 卖出下单
                    sell_order_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_order&mmfx=2&mktCode=0&stkCode=" + i + "&price=" + str(
                        new_close) + "&wtsl=" + holding_quantity + "&r=3429902&_=" + times
                    sell_order_data = requests.get(sell_order_url).json()
                    if sell_order_data["result"] == 0:
                        # print(sell_order_data)
                        print("委托卖出：" + "股票名称：" + sell_list[a_mun]["stkName"], "委托价：" + str(new_close),
                              "成本价：" + str(cost_price),
                              "委托数量：" + holding_quantity, "订单ID：" + sell_order_data["wth"])
                    else:
                        pass
                        # print(sell_order_data["message"])
            else:
                pass
            #   print("大于成本价，需要观察",i)
        else:
            pass
            # print("观察   股票code："+i," 现价："+str(new_close),"成本价："+str(cost_price))


def cancel_oeder():#撤单代码
    cancel_code_list = registration_oeder()[0]  # 获取持仓的code
    # print(sell_code_list)
    cancel_list = registration_oeder()[1]  # 获取持仓的所有信息
    # sell_list=[{'cbj': '6.360', 'drsl': '0', 'fdyk': '-10.01', 'fullcode': '65792', 'kysl': '100', 'ljcbyk': '-10.01', 'mktVal': '626.00', 'newPrc': '6.26', 'prePrc': '0.00', 'qljcbyk': '0.00', 'rateMax': '-1.57', 'stkCode': '000404', 'stkName': '长虹华意', 'zqlb': '6', 'zqsl': '100'}, {'cbj': '6.500', 'drsl': '0', 'fdyk': '-0.01', 'fullcode': '84032', 'kysl': '100', 'ljcbyk': '-0.01', 'mktVal': '650.00', 'newPrc': '6.50', 'prePrc': '0.00', 'qljcbyk': '0.00', 'rateMax': '-0.00', 'stkCode': '000521', 'stkName': '长虹美菱', 'zqlb': '6', 'zqsl': '100'}]
    # print(sell_list)
    real_data = ef.stock.get_quote_history(cancel_code_list, beg=today_date, end=today_date, klt=1)
    # print(real_data,type(real_data))
    for ia, b_mun in zip(cancel_code_list, range(len(cancel_code_list))):
        df = real_data[ia]
        if len(df.index) != 0:
            df.rename(columns={'股票代码': 'code', '日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low',
                               '成交量': 'volume', '成交额': 'pay', '振幅': 'zf', '涨跌幅': 'zdf', '涨跌额': 'zde', '换手率': 'hsl',
                               }, inplace=True)  ##修改列名
        # print(df.tail(1))
        # print(a_mun)
        # print(df.tail(1).iloc[0].iat[4])
        # print(sell_list[a_mun]["cbj"])
        new_close = df.tail(1).iloc[0].iat[4]  # 获取现价
        entrust_price = cancel_list[b_mun]["wtjg"]  # 获取成本委托价
        # print(new_close,entrust_price)
        #撤单
        if int(cancel_list[b_mun]["mmflag"])==1:
            if float(entrust_price) > (float(new_close)):
                cancel_url="https://simoper.eastmoney.com/oper_tzzh_v2?userid="+userid+"&zjzh="+zjzh+"&plat=2&ver=web20&type=spo_cancel&stkCode="+cancel_list[b_mun]["stkCode"] +"&mktCode=0&wth="+cancel_list[b_mun]["wth"]+"&mmfx=2&_="+times
                cancel_data=requests.get(cancel_url).json()
                if cancel_data["result"] == 0:
                    print("撤单："+cancel_data["message"],"撤单订单号："+cancel_data["wth"])
        else:
            if float(entrust_price) > float(new_close):
                cancel_url="https://simoper.eastmoney.com/oper_tzzh_v2?userid="+userid+"&zjzh="+zjzh+"&plat=2&ver=web20&type=spo_cancel&stkCode="+cancel_list[b_mun]["stkCode"] +"&mktCode=0&wth="+cancel_list[b_mun]["wth"]+"&mmfx=2&_="+times
                cancel_data=requests.get(cancel_url).json()
                if cancel_data["result"] == 0:
                    print("撤单："+cancel_data["message"],"撤单订单号："+cancel_data["wth"])
# cancel_oeder()