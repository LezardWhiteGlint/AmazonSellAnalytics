from OrderWithAddress import OrderWithAddress
from tkinter import filedialog
from tkinter import *
import openpyxl
import os,sys


if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


class OrderRecordXlsx(object):
    def __init__(self):
        self.orderWithAddress = []
        self.skuAsin = {}
        self.storageFileLoaded = False


    def loadData(self):
        if self.storageFileLoaded == False:
            print("请先载入库存文件")
        else:
            print("请选择订单文件，订单文件下载路径为 订单---订单报告")
            file = filedialog.askopenfile()
            unprocessedContent = []
            if file != None:
                titles = file.readline().split("\t")
                unprocessedContent = file.readlines()
                # assert titles == ['order-id', 'order-item-id', 'purchase-date', 'payments-date', 'buyer-email',
                #                   'buyer-name', 'buyer-phone-number', 'sku', 'product-name', 'quantity-purchased',
                #                   'currency', 'item-price', 'item-tax', 'shipping-price', 'shipping-tax',
                #                   'ship-service-level', 'recipient-name', 'ship-address-1', 'ship-address-2',
                #                   'ship-address-3', 'ship-city', 'ship-state', 'ship-postal-code', 'ship-country',
                #                   'ship-phone-number', 'delivery-start-date', 'delivery-end-date', 'delivery-time-zone',
                #                   'delivery-Instructions', 'is-business-order', 'purchase-order-number',
                #                   'price-designation\n'], ("输入文件错误，需要订单报告，在订单---订单报告中下载")
            for content in unprocessedContent:
                temp = content.split("\t")
                self.orderWithAddress.append(OrderWithAddress())
                self.orderWithAddress[-1].amazonOrderID = temp[0]
                self.orderWithAddress[-1].purchaseTime = temp[2]
                self.orderWithAddress[-1].sku = temp[7]
                self.orderWithAddress[-1].asin = 'asin'
                self.orderWithAddress[-1].quantity = temp[9]
                self.orderWithAddress[-1].currency = temp[10]
                self.orderWithAddress[-1].itemPrice = temp[11]
                self.orderWithAddress[-1].itemTax = temp[12]
                self.orderWithAddress[-1].shippingPrice = temp[13]
                self.orderWithAddress[-1].shippingTax = temp[14]
                self.orderWithAddress[-1].recipientName = temp[16]
                self.orderWithAddress[-1].shipAddress = temp[17] + " " + temp[18] + " " + temp[19]
                self.orderWithAddress[-1].shipCity = temp[20]
                self.orderWithAddress[-1].shipState = temp[21]
                self.orderWithAddress[-1].shipPostalCode = temp[22]
                self.orderWithAddress[-1].shipCountry = temp[23]
                self.orderWithAddress[-1].buyerPhoneNumber = temp[24]
                self.orderWithAddress[-1].isBusnessOrder = temp[29]

    def asinFinder(self):
        unprocessedContent = []
        print("请选择库存文件，库存文件下载路径为 库存---库存报告")
        file = filedialog.askopenfile()
        if file != None:
            titles = file.readline().split("\t")
            unprocessedContent = file.readlines()
            # assert len(titles) == 16,("需要选择库存报告")
        for product in unprocessedContent:
            temp = product.split("\t")
            self.skuAsin[temp[0]] = temp[1]
        if file!=None:
            self.storageFileLoaded = True



    def outputXlsx(self):
        #add asin
        for order in self.orderWithAddress:
            try:
                order.asin = self.skuAsin[order.sku]
            except:
                print("注意：库存文件中有对应不到的asin，请确认库存文件为最新")
                pass

        xlsx = openpyxl.Workbook()
        sheet = xlsx.active
        sheet["A1"] = "订单号"
        sheet["B1"] = "下单时间"
        sheet["E1"] = "SKU"
        sheet["F1"] = "ASIN"
        sheet["N1"] = "利润"
        sheet["O1"] = "订单价格详情"
        sheet["P1"] = "联系买家"
        sheet["Q1"] = "地址"
        sheet["R1"] = "电话"
        sheet["S1"] = "物流"
        row = 1
        for order in self.orderWithAddress:
            row += 1
            sheet["A"+str(row)] = order.amazonOrderID
            sheet["B"+str(row)] = order.purchaseTime
            sheet["E"+str(row)] = order.sku
            sheet["F"+str(row)] = order.asin
            sheet["N"+str(row)] = ""
            sheet["O"+str(row)] = "商品小计: "+order.currency+order.itemPrice+"\n"+\
                                  "运费总额: "+order.currency+order.shippingPrice+"\n"+\
                "税务: "+order.currency+str(round(float(order.shippingTax)+float(order.itemTax),2))+"\n"+\
                "商品总计: "+order.currency+str(round(float(order.itemPrice)+float(order.shippingPrice)+float(order.itemTax)+float(order.shippingTax),2))
            sheet["P"+str(row)] = order.recipientName
            sheet["Q"+str(row)] = order.shipAddress+"\n"+order.shipCity+"\n"+order.shipState+"\n"+order.shipPostalCode+"\n"+order.shipCountry
            sheet["R"+str(row)] = order.buyerPhoneNumber
            sheet["S"+str(row)] = ""
        xlsx.save(application_path+"/orderWithAddress.xlsx")



test = OrderRecordXlsx()
test.asinFinder()
test.loadData()
test.outputXlsx()
