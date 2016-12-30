import urllib.request as urlget
import xml.etree.ElementTree
import csv
import pandas as pd

mstar_id = "./Fund"
fund_code = "./TradingInformation/ExchangeListing/TradingExchange/TradingExchangeList/TradingSymbol"
ter = "./Operation/AnnualReport/FeeAndExpense/NetExpenseRatio"
tc = "./Operation/AnnualReport/FeeAndExpense/TransactionCosts"
tic = "./Operation/AnnualReport/FeeAndExpense/Investmentmangementcharges"

#Need to add morningstar id later
#for mstar_code in root.findall(mstar_id):
   # print(mstar_code.tag)

codes_pop = ['F000002COA','F00000W8CC','F00000W8CB','F00000W8C9','F00000W8C8','F00000W8BZ','F00000W8BX','F00000W8BW','F00000W3IM','F00000W3IF','F00000W8CA','F00000W3IL','F00000W2CU','F00000W2CT']

my_list = []

df = pd.DataFrame(columns=['code','ter','tc','tic'])

for code in codes_pop:
    url = "http://edw.morningstar.com/DataOutput.aspx?Package=EDW&ClientId=Grindrod&Id=" + code + "&IDTYpe=FundShareClassId&Content=1&Currencies=BAS"
    #print(url)
    s = urlget.urlopen(url)
    root = xml.etree.ElementTree.parse(s).getroot()
    #print(root)
    my_dict = {}
    for trading_code in root.findall(fund_code):
        jse_code = trading_code.text
        print("Running..." + jse_code)
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
    print(my_dict)
    mini_df = pd.DataFrame.from_dict(my_dict,orient='columns')
    #mini_df = mini_df.transpose()
    #print(mini_df)
    df.append(mini_df)


    #my_list.append(my_dict)

print("Looped through all funds")
#print(my_list)
print(df)

#toCSV = my_list
#keys = toCSV[0].keys()
#with open('people.csv', 'w') as output_file:
    #dict_writer = csv.DictWriter(output_file, keys)
    #dict_writer.writeheader()
    #dict_writer.writerows(toCSV)

