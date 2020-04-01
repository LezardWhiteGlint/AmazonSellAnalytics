from Order import Order


class AmazonSellAnalytics(object):
    def __init__(self,fileName):
        file = open(fileName, "r")
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

    def howManyKindProductIsOrdered(self):
        productsAsin = []
        for order in self.orders:
            if order.asin not in productsAsin:
                productsAsin.append(order.asin)
        print("The number of kinds is "+str(len(productsAsin)))
        # for productAsin in productsAsin:
        #     print(productAsin)

    def shippingStatus(self):
        shipped = 0
        notShipped = 0
        for order in self.orders:
            if order.itemStatus == "Shipped":
                shipped += 1
        print("For total "+str(len(self.orders))+", "+str(shipped)+" are shipped")

    def bestSellProductAsin(self):
        sell = {}
        for order in self.orders:
            if order.orderStatus != "Cancelled":
                if order.asin not in sell.keys():
                    sell[order.asin] = 1
                else:
                    sell[order.asin] += 1
        print(sell)


test = AmazonSellAnalytics("txt.txt")
test.bestSellProductAsin()
        
