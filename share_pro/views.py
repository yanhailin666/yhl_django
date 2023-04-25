import requests,json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging.config
from django.conf import settings
from public.dingding import sed_dingding
from public.order_buy import buy_order
from public.order_sell import *





#
logger = logging.getLogger('share_pro')
logging.config.dictConfig(settings.LOGGING)


def aa(request):
    if request.method == 'GET':
        return JsonResponse({"data":"成功"})

def main_inflow(request):#根据现金流监测-主力净流入》行业板块——个股大于0.8亿
    if request.method == 'GET':
        #前5资金行业流向
        url = "https://push2.eastmoney.com/api/qt/clist/get?fid=f62&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m%3A90+t%3A2&stat=1&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124&ut=b2884a393a59ad64002292a3e90d46a5"
        industry_funds = requests.get(url).json()
        # print(industry_funds["data"]["diff"])
        industry_funds_data_list = []
        industry_funds_code_list=[]
        for i in range(len(industry_funds["data"]["diff"])):
            industry_funds_data =  "\n行业名称：" + str(
                industry_funds["data"]["diff"][i]["f14"]) + " 主力净流入：" + str(
                int(industry_funds["data"]["diff"][i]["f62"]) / 100000000) + "亿  " + " 涨跌幅：" + str(
                industry_funds["data"]["diff"][i]["f3"]) + " 主力净占比：" + str(industry_funds["data"]["diff"][i]["f184"])
            industry_funds_code_list.append(industry_funds["data"]["diff"][i]["f12"])
            industry_funds_data_list.append(industry_funds_data)
        sed_dingding("".join(industry_funds_data_list))#发送钉钉数据
        #行业板块
        share_fund_code = {}
        share_fund_list = []
        for a in industry_funds_code_list:
            url = "https://push2.eastmoney.com/api/qt/clist/get?fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=b:" + a + "&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13"
            # print(url)
            share_fund_data = requests.get(url).json()
            for i in range(len(share_fund_data["data"]["diff"])):
                # print(share_fund_data["data"]["diff"][i]["f3"],(share_fund_data["data"]["diff"][i]["f14"]))
                try:
                    if "ST" not in share_fund_data["data"]["diff"][i]["f14"]:#去掉st
                        # print(share_fund_data["data"]["diff"][i]["f3"], (share_fund_data["data"]["diff"][i]))
                        if int(share_fund_data["data"]["diff"][i]["f3"]) > 0:#判断涨幅大于0
                            if int(share_fund_data["data"]["diff"][i]["f62"]) / 100000000 > 0.3:#判断主力净流入大于0.8亿
                                share_fund_code["code"]=(share_fund_data["data"]["diff"][i]["f12"])
                                share_fund_code["price"] = (share_fund_data["data"]["diff"][i]["f2"])
                                share_fund_list.append(share_fund_code)
                except ValueError:
                    continue
        # print(share_fund_code)
        return JsonResponse({"data":share_fund_list})



def share_inflow(request):#根据个股现金流大于0.3亿并且股价在5到50之间
    if request.method == 'GET':
        share_inflow_code={}
        share_inflow_list=[]
        share_inflow_url="https://push2.eastmoney.com/api/qt/clist/get?fid=f66&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13"
        share_inflow_data=requests.get(share_inflow_url).json()
        # print(share_inflow_data)
        for ia in range(50):
            if int(share_inflow_data["data"]["diff"][ia]["f62"])/100000000 >0.3:
                if 5<int(share_inflow_data["data"]["diff"][ia]["f2"])<50:
                    share_inflow_code["code"]=(share_inflow_data["data"]["diff"][ia]["f12"])
                    share_inflow_code["price"]=(share_inflow_data["data"]["diff"][ia]["f2"])
                    share_inflow_list.append(share_inflow_code)
        return JsonResponse({"data":share_inflow_list})
def order(request):
    if request.method == 'GET':
        print("交易程序执行中......")
        buy_data=requests.get("http://127.0.0.1:8000/share/share_inflow").json()
        data=buy_order(buy_data)
        sell_order()
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})






