import requests
import time
from django.http import JsonResponse, HttpResponse

times = str(round((time.time())*1000))
#
# def investment_portfolio():
#     my_nvestment_portfolio_url="https://simqry2.eastmoney.com/qry_tzzh_v2?type=spo_zuhe_preview&plat=2&ver=web20&userid=1687456732613796&utToken=FobyicMgeV6Hb_DbDix6-CJmlGkS6DvK8-qSRX5IgnM27yq0V8aX0DqGze4Ez4vfW7NwOEGFNKLmmDUS-xLn95FCBDDORcDkM-50dMrN43sPfi5JAgSwKma5-ozfYZbjoxmQkWbCP8XyVEB4aXanbvE8Z6IXKmM46qbac-4W9evWrrD84nV2ypqGarBxMcpPfsNQkr3rECT70tlQ7oiu6GckMVkcdJAN3HdlvWwEiwJz2gmnGZGrM6WfuRD1pFK_KGeJX3rQgkMjgrAzYvx1vhwSjdgkkKJM&ctToken=LdDTKT_xrvyDgS7o9LhOYwHtjU3mePaMiZFyJHIuvNHVaBLkWDrHlM_gsterqMR3StTrqAdlHeWTIAjZS5Ofa2osRSUWHvjCtw8YV0p2tHPEsDylEm11Tm5l7JkFHJRT8-dzyr96QPWGyhTpx9go5VOJYqch8-IGSTxSUE5sVZQ&_="+times
#     my_nvestment_portfolio_data=requests.get(my_nvestment_portfolio_url).json()
#     # print(my_nvestment_portfolio_data["data"])
#     if len(my_nvestment_portfolio_data["data"])>0:
#         zjzh=my_nvestment_portfolio_data["data"][0]["zjzh"]
#         # print(zjzh)
#         return zjzh
#     else:
#         zuheName = "韭菜518"
#         comment = "韭菜518"
#         investment_portfolio_url = "https://simoper.eastmoney.com/oper_tzzh_v2?type=spo_create_zuhe&plat=2&ver=web20&utToken=FobyicMgeV6Hb_DbDix6-CJmlGkS6DvK8-qSRX5IgnM27yq0V8aX0DqGze4Ez4vfW7NwOEGFNKLmmDUS-xLn95FCBDDORcDkM-50dMrN43sPfi5JAgSwKma5-ozfYZbjoxmQkWbCP8XyVEB4aXanbvE8Z6IXKmM46qbac-4W9evWrrD84nV2ypqGarBxMcpPfsNQkr3rECT70tlQ7oiu6GckMVkcdJAN3HdlvWwEiwJz2gmnGZGrM6WfuRD1pFK_KGeJX3rQgkMjgrAzYvx1vhwSjdgkkKJM&ctToken=LdDTKT_xrvyDgS7o9LhOYwHtjU3mePaMiZFyJHIuvNHVaBLkWDrHlM_gsterqMR3StTrqAdlHeWTIAjZS5Ofa2osRSUWHvjCtw8YV0p2tHPEsDylEm11Tm5l7JkFHJRT8-dzyr96QPWGyhTpx9go5VOJYqch8-IGSTxSUE5sVZQ&zuheName=" + zuheName + "&comment=" + comment + "&authority=0&_=" + times
#         investment_portfolio_list = requests.get(investment_portfolio_url).json()
#         # print(investment_portfolio)
#         # 获取组合ID
#         try:
#             if investment_portfolio_list["result"] == 0:
#                 print("创建成功", investment_portfolio_list["zjzh"])
#                 zjzh = investment_portfolio_list["zjzh"]
#                 return zjzh
#             elif investment_portfolio_list["result"] == 10001:
#                 print(investment_portfolio_list['message'])
#         except IndexError:
#             print(investment_portfolio_list['message'])
#调试用
# buy_signal={"data": [{"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}, {"code": "601528", "price": 8.04}]}

def buy_order(buy_signal):

    #线上用
    buy_signal=buy_signal["data"]
    # print(buy_signal)
    zjzh='231140300000054491'#组合ID
    print(zjzh)
    userid="1687456732613796"#用户ID
    # stkCode=buy_signal["data"][0]["code"]#"300814"#股票ID
    # price=buy_signal["data"][0]["price"]#"21.87"#股价
    wtsl="100"#买入数量
    #查询持仓信息
    position_order_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_hold&reqUserid=&recIdx=0&recCnt=100&_=" + times
    position_order = requests.get(position_order_url).json()
    # print(len(position_order["data"]))
    position_list = []
    for b in range(len(position_order["data"])):
        position_list.append(position_order["data"][b]["stkCode"])
    # print(position_list)
    #查看挂单信息
    registration_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_orders_cancel&reqUserid=&recIdx=0&recCnt=100&_=1681635713685"
    registration = requests.get(registration_url).json()
    registration_list = []
    for a in range(len(registration["data"])):
        registration_list.append(registration["data"][a]["stkCode"])
    # print(registration_list)
    new_position_code =list (position_code for position_code in position_list if position_code == stkCode)
    new_registration_code = list(registration_code for registration_code in registration_list if registration_code == stkCode)
    # print((new_position_code),len((new_position_code)))
    for num in range(len(buy_signal)):
        stkCode=buy_signal[num]["code"]#"300814"#股票ID
        price=buy_signal[num]["price"]#"21.87"#股价
        if len((new_position_code)) ==0:#判断持仓信息
            # print((new_position_code))
            if len((new_registration_code)) ==0:#判断挂单信息
                #下单
                order_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_order&mmfx=1&mktCode=0&stkCode=" + stkCode + "&price=" + str(price) + "&wtsl=" + wtsl + "&r=53106012&_=" + times
                order = requests.get(order_url).json()
                # print(order)
                if order["result"] == 0:
                    print(order["message"], "订单号：" + order["wth"])
                    # 查看挂单信息
                    registration_url = "https://simoper.eastmoney.com/oper_tzzh_v2?userid=" + userid + "&zjzh=" + zjzh + "&plat=2&ver=web20&type=spo_orders_cancel&reqUserid=&recIdx=0&recCnt=100&_=" + times
                    registration = requests.get(registration_url).json()
                    # print(registration["data"][0]["wth"])
                    if order["wth"] == registration["data"][0]["wth"]:
                        data=("挂单信息：" + "股票id" + registration["data"][0]["stkCode"],
                              "股票名称" + registration["data"][0]["stkName"], "挂单订单号" + registration["data"][0]["wth"])
                        data= ({"data":data})
                else:
                    data= (({"data":order["message"]}))
                    print(data)
            else:
                print("挂单信息：" + "股票id"+new_registration_code[0])

        else:
            print("持仓股票：" + "股票code：" + new_position_code[0])
    return data

# buy_order(buy_signal)

