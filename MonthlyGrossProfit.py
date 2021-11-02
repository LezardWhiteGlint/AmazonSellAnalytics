from tkinter import filedialog
from tkinter import *
import pandas as pd


class MonthlyGrossProfit(object):
    def __init__(self):
        self.filePath = filedialog.askopenfilename()
        self.sheet = pd.read_csv(self.filePath,skiprows=7,thousands=',')
        self.itemsCost = {}
        self.itemCount = {}
        self.totalRevenue = 0
        self.totalCost = 0
        self.conversionRate = 6.3962
        self.sku = self.sheet['sku'].unique()

    def getTotalRevenue(self):
        """total minus transferred amount"""
        total = self.sheet['total'].sum()
        transferred = self.sheet[self.sheet['type'] == 'Transfer']['total'].sum()
        result = total - transferred
        print("Total revenue is")
        print(result*self.conversionRate)
        print("--------------------------------")
        self.totalRevenue = result

    def getItemSoldCount(self):
        result = {}
        orders = self.sheet[self.sheet['type'] == 'Order']
        for sku in self.sku:
            result[sku] = orders[orders['sku'] == sku]['date/time'].count()
        self.itemCount = result
        return result

    def getItemSoldTotalCost(self):
        result = 0
        for sku in self.sku:
            try:
                result += self.itemCount[sku] * self.itemsCost[sku]
            except:
                pass
        self.totalCost = result
        print("The total cost of items sold is")
        print(result)
        print("------------------------------------------")

    def getGrossProfit(self):
        print("The total gross profit is")
        print(self.totalRevenue*self.conversionRate - self.totalCost)



test = MonthlyGrossProfit()
#set original cost
test.itemsCost = {
    '20mm-band':10,
    '2duragbutton':15,
    '38mmcase':8,
    '42mmcase':8,
    'frogphonecase':9.5,
    'rainbowband22mm':10,
    'rainbowcase-40mm':8,
    'rainbowcase-44mm':8,
    'stretchyband3840mm':10,
    'stretchyband4244mm':10,
    'watchband-rainbow':20,
    'watchband-rainbow44':20,
    'cat banner':18.5,
    '4Z-H83K-ZUX5':15,
    'rainbow banner':18.5,
    'rainbow-airpodcase':15,
}

test.getTotalRevenue()
for i in test.getItemSoldCount().items():
    print(i)
print("------------------------------------")
test.getItemSoldTotalCost()
test.getGrossProfit()




