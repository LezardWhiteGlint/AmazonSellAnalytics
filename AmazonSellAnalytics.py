from Order import Order
from plotly.offline import plot
import plotly.graph_objs as go
from tkinter import filedialog
from tkinter import *


class AmazonSellAnalytics(object):
    def __init__(self,file):
        titles = file.readline().split("\t")
        unprocessedContent = file.readlines()
        self.orders = []
        # check if input file is correct
        assert len(titles) == 32, ("错误的文件，请确保文件是从 库存和销售报告---->所有订单 中导出")
        #read the content, put them in the storage class
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

    def plotBar(self,x,y,name):
        trace = go.Bar(x = x,y = y,name = name)
        plot([trace],filename = name + ".html")


    def shippingStatus(self):
        unShipped = 0
        for order in self.orders:
            if order.itemStatus == "Unshipped":
                unShipped += 1
        print("有 "+str(unShipped)+" 个待发货")

    def bestSellProductSkuAndHowManyKindsTotal(self):
        sells = {}
        for order in self.orders:
            if order.orderStatus != "Cancelled":
                if order.sku not in sells.keys():
                    sells[order.sku] = 1
                else:
                    sells[order.sku] += 1
        #plot
        x = []
        y = []
        for sku in sells.keys():
            x.append(sku)
            y.append(sells[sku])
        self.plotBar(x,y,"bestSellProductSkuAndHowManyKindsTotal "+str(len(sells.keys()))+" kinds sold")

    def whenOrdersComeEveryday(self):
        def utcConvertToBeijing(utc):
            result = int(utc)+8
            if result >= 24:
                result -= 24
            return str(result)

        orderTime = {}
        for order in self.orders:
            if order.orderStatus != "Cancelled":
                if utcConvertToBeijing(order.purchaseTime.split(":")[0]) not in orderTime.keys():
                    orderTime[utcConvertToBeijing(order.purchaseTime.split(":")[0])] = 1
                else:
                    orderTime[utcConvertToBeijing(order.purchaseTime.split(":")[0])] += 1
        # print(orderTime)
        #plot
        x = []
        y = []
        for time in orderTime.keys():
            x.append(time)
            y.append(orderTime[time])
        self.plotBar(x,y,"whenOrdersComeEveryday(Beijing Time)")

    def dailyRevenu(self):
        revenue = {}
        for order in self.orders:
            if order.orderStatus != "Cancelled":
                if order.purchaseDate not in revenue.keys():
                    revenue[order.purchaseDate] = float(order.itemPrice)
                else:
                    revenue[order.purchaseDate] += float(order.itemPrice)
        x = []
        y = []
        for rev in revenue.keys():
            x.append(rev)
            y.append(revenue[rev])
        self.plotBar(x,y,"dailyRevenu")


root = Tk()
root.file = filedialog.askopenfile()
analysis = AmazonSellAnalytics(root.file)
analysis.shippingStatus()
analysis.bestSellProductSkuAndHowManyKindsTotal()
analysis.whenOrdersComeEveryday()
analysis.dailyRevenu()
        
