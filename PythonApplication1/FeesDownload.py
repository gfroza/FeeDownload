##TO DO
## Add counter so see when error
## Add exception handler whole way through. if exception then generate CSV files as is

import urllib.request as urlget
import xml.etree.ElementTree
import pandas as pd
import csv
import time

mstar_id = "./Fund"
fund_code = "./TradingInformation/ExchangeListing/TradingExchange/TradingExchangeList/TradingSymbol"
ter = "./Operation/AnnualReport/FeeAndExpense/NetExpenseRatio"
tc = "./Operation/AnnualReport/FeeAndExpense/TransactionCosts"
tic = "./Operation/AnnualReport/FeeAndExpense/Investmentmangementcharges"

#Need to add morningstar id later
#for mstar_code in root.findall(mstar_id):
   # print(mstar_code.tag)

#codes_pop = ['F000002COA','F00000W8CC','F00000W8CB','F00000W8C9','F00000W8C8','F00000W8BZ','F00000W8BX','F00000W8BW','F00000W3IM','F00000W3IF','F00000W8CA','F00000W3IL','F00000W2CU','F00000W2CT']

with open('codes_for_fees.csv', 'r') as f:
  reader = csv.reader(f)
  the_list = list(reader)

codes_pop  = [val for sublist in the_list for val in sublist]

#print(codes_pop)
my_list = []
failed_codes_list = []

counter = 0

for code in codes_pop:
    try:
        counter += 1
        print(counter)
        time.sleep(0.5)
        url = "http://edw.morningstar.com/DataOutput.aspx?Package=EDW&ClientId=Grindrod&Id=" + code + "&IDTYpe=FundShareClassId&Content=1&Currencies=BAS"
        s = urlget.urlopen(url)
        #print(url)
        root = xml.etree.ElementTree.parse(s).getroot()
        #print(root)
        my_dict = {}
        for trading_code in root.findall(fund_code):
            jse_code = trading_code.text
            #print("Running..." + jse_code)
            my_dict.update({"code" : jse_code})
        
        for ter_value in root.findall(ter):
            name = 'ter'
            value = ter_value.text
            my_dict.update({name: value})
        for tc_value in root.findall(tc):
            name = 'tc'
            value = tc_value.text
            my_dict.update({name: value})
        for tic_value in root.findall(tic):
            name = 'tic'
            value = tic_value.text
            my_dict.update({name: value})
    
        my_list.append(my_dict)
    
    except Exception as str_error:
        #failed_codes_list.append(code)
        print("failed...")
        time.sleep(30)
        pass

print("Looped through all funds")
#print(my_list)

df = pd.DataFrame(my_list,columns=['code','ter','tc','tic'])
 
#print(df)
df.to_csv('fees.csv',',')

#myfile = open('failed.csv', 'wb')
#wr = csv.writer(myfile)
#wr.writerow(failed_codes_list)

