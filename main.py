from nselib import capital_market
import json
import csv

def nse_data(date):
    data = capital_market.bhav_copy_equities("04-01-2024")
    return data

def filter_data(data,share):
    filter = (data['SYMBOL']== share['Name'])
    data = data.loc[filter,['SYMBOL','CLOSE','PREVCLOSE']]
    data = (str(data).replace('\n',' ')).split()
    
    symbol = data[4]
    close = float(data[5])
    prevClose = float(data[6])
    quantity = share['Quantity']
    buying_price = share['Buying Price']

    final_dict = {
        "Symbol" : symbol,
        "Close" : close,
        "PrevClose" : prevClose,
        "Change" : round(close - prevClose,2),
        "Quantity" :quantity,
        "Buying Price" : buying_price,
        'Net Profit' : round((close-buying_price)*quantity,2),
        "Return(%)" : round(buying_price/close*100,2)
    }
    return final_dict

final_data = []
dict = [{'Name' :'ADANIENT','Quantity': 100,'Buying Price' : 2000},
        {'Name' :'IDEAFORGE','Quantity': 100,'Buying Price' : 650},
        {'Name' :'IRFC','Quantity': 2000,'Buying Price' : 65},
        {'Name' :'KPIGREEN','Quantity': 100,'Buying Price' : 800}]

data = nse_data(None)
for item in dict:
    dict_data = filter_data(data,item)
    final_data.append(dict_data)
print(final_data)

##Write To a CSV File
with open('Report.csv','w') as f:
    writer = csv.DictWriter(f,fieldnames=final_data[0].keys())
    writer.writeheader()
    for item in final_data:
        writer.writerow(item)

##Write to a JSON file
with open('Report.json','w') as f:
    json.dump(final_data,fp=f)