from Order import Order
from plotly.offline import plot
import chart_studio.plotly as py
import plotly.graph_objs as go
from tkinter import filedialog
from tkinter import *
import pymongo
from pymongo import MongoClient

import chart_studio
chart_studio.tools.set_credentials_file(username='lezardvaleth66', api_key='Fwgzi9cSidhFfJSfsRHg')
chart_studio.tools.set_config_file(world_readable=True,sharing='public')

"""文件是从 库存和销售报告---->所有订单 中导出"""
class AmazonSellAnalytics(object):
    def __init__(self):

        self.orders = []
        # check if input file is correct
        #initiate data base
        self.client = MongoClient()
        self.DB = self.client.Amazon
        self.Collection = self.DB.AmazonAnalysisSuperMoneyBall


    def updateDataBase(self,file):
        unprocessedContent = []
        if file != None:
            titles = file.readline().split("\t")
            unprocessedContent = file.readlines()
            assert len(titles) == 32, ("错误的文件，请确保文件是从 库存和销售报告---->所有订单 中导出")
            # read the content, put them in the storage class
        for content in unprocessedContent:
            temp = content.split("\t")
            self.orders.append(Order())
            self.orders[-1].amazonOrderID = temp[0]
            self.orders[-1].merchantOrderID = temp[1]
            self.orders[-1].purchaseDate = temp[2].split("T")[0]
            self.orders[-1].purchaseTime = temp[2].split("T")[1]
            self.orders[-1].lastUpdatedDate = temp[3].split("T")[0]
            self.orders[-1].orderStatus = temp[4]
            self.orders[-1].fulfillmentChannel = temp[5]
            self.orders[-1].salesChannel = temp[6]
            self.orders[-1].orderChannel = temp[7]
            self.orders[-1].url = temp[8]
            self.orders[-1].shipServiceLevel = temp[9]
            self.orders[-1].productName = temp[10]
            self.orders[-1].sku = temp[11]
            self.orders[-1].asin = temp[12]
            self.orders[-1].itemStatus = temp[13]
            self.orders[-1].quantity = temp[14]
            self.orders[-1].currency = temp[15]
            self.orders[-1].itemPrice = temp[16]
            self.orders[-1].itemTax = temp[17]
            self.orders[-1].shippingPrice = temp[18]
            self.orders[-1].shippingTax = temp[19]
            self.orders[-1].giftWrapPrice = temp[20]
            self.orders[-1].giftWrapTax = temp[21]
            self.orders[-1].itemPromotionDiscount = temp[22]
            self.orders[-1].shipPromotionDiscount = temp[23]
            self.orders[-1].shipCity = temp[24]
            self.orders[-1].shipState = temp[25]
            self.orders[-1].shipPostalCode = temp[26]
            self.orders[-1].shipCountry = temp[27]
            self.orders[-1].promotionIDs = temp[28]
            self.orders[-1].isBusnessOrder = temp[29]
            self.orders[-1].purchaseOrderNumber = temp[30]
            self.orders[-1].priceDesignation = temp[31]

        for order in self.orders:
            post = {
                "amazonOrderID":order.amazonOrderID,
                "purchaseDate":order.purchaseDate,
                "purchaseTime":order.purchaseTime,
                "sku":order.sku,
                "orderStatus":order.orderStatus,
                "asin":order.asin,
                "quantity":order.quantity,
                "currency":order.currency,
                "itemPrice":order.itemPrice,
                "itemTax":order.itemTax,
                "itemShippingPrice":order.shippingPrice,
                "itemShippingTax":order.shippingTax,
                "itemGiftWrapPrice":order.giftWrapPrice,
                "itemGiftWrapTax":order.giftWrapTax,
                "itemPromotionDiscount": order.itemPromotionDiscount,
                "shipPromotionDiscount":order.shipPromotionDiscount,
                "shipState":order.shipState,
                "shipCountry":order.shipCountry
            }
            self.Collection.replace_one({"amazonOrderID":order.amazonOrderID}, post, upsert= True)
        print("Data base updated")



    def plotBar(self,x,y,name):
        trace = go.Bar(x = x,y = y,name = name)
        plot([trace],filename = name + ".html")


    def shippingStatus(self):
        unShipped = self.Collection.find({"orderStatus":"Pending"})
        count = 0
        for i in unShipped:
            count += 1
        print("有 "+str(count)+" 个待发货")

    def bestSellProductSkuAndHowManyKindsTotal(self):
        sells = {}
        for order in self.Collection.find({"orderStatus":{"$in":["Shipped","Pending"]}}):
            # print(order["orderStatus"])
            if order["sku"] not in sells.keys():
                sells[order["sku"]] = 1
            else:
                sells[order["sku"]] += 1

        #plot
        x = []
        y = []
        for sku in sells.keys():
            x.append(sku)
            y.append(sells[sku])
        self.plotBar(x,y,"bestSellProductSkuAndHowManyKindsTotal "+str(len(sells.keys()))+" kinds sold")

    # def whenOrdersComeEveryday(self):
    #     def utcConvertToBeijing(utc):
    #         result = int(utc)+8
    #         if result >= 24:
    #             result -= 24
    #         return str(result)
    #
    #     orderTime = {}
    #     for order in self.orders:
    #         if order.orderStatus != "Cancelled":
    #             if utcConvertToBeijing(order.purchaseTime.split(":")[0]) not in orderTime.keys():
    #                 orderTime[utcConvertToBeijing(order.purchaseTime.split(":")[0])] = 1
    #             else:
    #                 orderTime[utcConvertToBeijing(order.purchaseTime.split(":")[0])] += 1
    #     # print(orderTime)
    #     #plot
    #     x = []
    #     y = []
    #     for time in orderTime.keys():
    #         x.append(time)
    #         y.append(orderTime[time])
    #     self.plotBar(x,y,"whenOrdersComeEveryday(Beijing Time)")

    def dailyRevenu(self):
        revenue = {}
        for order in self.Collection.find({"orderStatus":{"$in":["Shipped","Pending"]}}):
            # print(order)
            if order["purchaseDate"] not in revenue.keys():
                try:
                    revenue[order["purchaseDate"]] = float(order["itemPrice"])
                except ValueError:
                    print(order["itemPrice"])
            else:
                try:
                    revenue[order["purchaseDate"]] += float(order["itemPrice"])
                except ValueError:
                    print(order["itemPrice"])
        x = []
        y = []
        for rev in revenue.keys():
            x.append(rev)
            y.append(revenue[rev])
        # self.plotBar(x,y,"dailyRevenu")
        trace = go.Bar(x = x,y = y)
        py.plot([trace],filename = "revenue", auto_open= True)

    # def orderDateForEachSku(self):
    #     orderDates = {}
    #     skuList = []
    #     for order in self.orders:
    #         if order.orderStatus != "Cancelled":
    #             if order.sku not in skuList:
    #                 skuList.append(order.sku)
    #                 orderDates[order.sku] = [order.purchaseDate]
    #             else:
    #                 orderDates[order.sku].append(order.purchaseDate)
    #     plotData = []
    #     print(orderDates)
    #     for sku in orderDates.keys():
    #         x = []
    #         y = []
    #         for date in orderDates[sku]:
    #             x.append(date)
    #             y.append(1)
    #         trace = go.Bar(x = x,y = y,name = sku)
    #         plotData.append(trace)
    #     plot(plotData,filename= "test.html")
    #
    # def productCount(self,sku):
    #     count = 0
    #     for order in self.orders:
    #         if order.sku == sku:
    #             count += 1
    #     print(sku +" count is "+ str(count))

    def skuRevenu(self):
        sku = []
        #get sku list
        for order in self.Collection.find({"orderStatus":{"$in":["Shipped","Pending"]}}):
            if order["sku"] not in sku:
                sku.append(order["sku"])
        #for each sku get it curve and add to trace
        plotData = []
        for targetSku in sku:
            orderDates = {}
            for order in self.Collection.find({"orderStatus":{"$in":["Shipped","Pending"]},"sku":targetSku}).sort("purchaseDate",pymongo.ASCENDING):
                if order["purchaseDate"] not in orderDates.keys():
                    try:
                        orderDates[order["purchaseDate"]] = float(order["itemPrice"])
                    except ValueError:
                        print(order["itemPrice"])
                else:
                    orderDates[order["purchaseDate"]] += float(order["itemPrice"])
            x = []
            y = []
            for date in orderDates.keys():
                x.append(date)
                y.append(orderDates[date])
            trace = go.Scatter(
                x = x,
                y = y,
                name = targetSku
            )
            plotData.append(trace)
        plot(plotData,filename="skuRevenu.html")

    def bestSellsMonitor(self,monitorSkuList):
        sku = monitorSkuList
        plotData = []
        for targetSku in sku:
            orderDates = {}
            for order in self.Collection.find({"orderStatus": {"$in": ["Shipped", "Pending"]}, "sku": targetSku}).sort(
                    "purchaseDate", pymongo.ASCENDING):
                # print(order["purchaseDate"])
                if order["purchaseDate"] not in orderDates.keys():
                    try:
                        orderDates[order["purchaseDate"]] = float(order["itemPrice"])
                    except ValueError:
                        print(order["itemPrice"])
                else:
                    orderDates[order["purchaseDate"]] += float(order["itemPrice"])
            x = []
            y = []
            for date in orderDates.keys():
                x.append(date)
                y.append(orderDates[date])
            trace = go.Bar(
                x=x,
                y=y,
                name=targetSku
            )
            plotData.append(trace)
        plot(plotData, filename="bestSellsMonitor.html")




class interface(object):
    def __init__(self):
        self.analysis = AmazonSellAnalytics()
        self.root = Tk()
        loadDataButton = Button(self.root, text="Load Data", command=self.loadData)
        loadDataButton.pack()
        reportButton = Button(self.root, text="Report Generator", command=self.reportOutput)
        reportButton.pack()
        self.root.mainloop()


    def loadData(self):
        print("load")
        self.root.file = filedialog.askopenfile()
        self.analysis.updateDataBase(self.root.file)

    def reportOutput(self):
        self.analysis.bestSellsMonitor(["2duragbutton","watchband-rainbow","watchband-rainbow44","fitbit-pink","fitbit-black","IK-0E1K-DW3N"])
        self.analysis.skuRevenu()
        self.analysis.dailyRevenu()



test = interface()


