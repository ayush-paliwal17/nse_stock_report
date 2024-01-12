from nselib import capital_market
from json2html import *
import json
import csv

def nse_data(date):
    """Get data From NSE for the specified Date"""

    data = capital_market.bhav_copy_equities("04-01-2024")
    return data


def filter_data(data,share):
    """Filter Through The data to get the data for the required Shares"""

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
        "Change (%)" : round((close-prevClose)/prevClose*100,2),
        "Day's Gain" : round((close - prevClose)*quantity,2),
        "Quantity" :quantity,
        "Buying Price" : buying_price,
        'Net Profit' : round((close-buying_price)*quantity,2),
        "Return(%)" : round(buying_price/close*100,2)
    }
    return final_dict


def html_table(json_data):
    """Convert The generated JSON into HTML Table"""

    table = json2html.convert(json_data, table_attributes = 'border="0.5" style="background-color:black;"')
    table = table.replace('<thead>','<thead align="Centre" style="background-color:limegreen;">')
    table = table.replace('<tbody>','<tbody align="Right" style="background-color:chartreuse;">')
    table = table.replace('<th>','<th width="100">')
    return table


def main():
    """Main Function"""

    final_data = []
    dict = [{'Name' :'ADANIENT','Quantity': 100,'Buying Price' : 2000},
            {'Name' :'IDEAFORGE','Quantity': 100,'Buying Price' : 650},
            {'Name' :'IRFC','Quantity': 2000,'Buying Price' : 65},
            {'Name' :'KPIGREEN','Quantity': 100,'Buying Price' : 800}]

    try:
        data = nse_data(None)
    except:
        raise ValueError("NO DATA FOUND")
    else:
        for item in dict:
            dict_data = filter_data(data,item)
            final_data.append(dict_data)
        
        table = html_table(final_data)

        ##Write to a JSON file
        with open('Report.json','w') as f:
            json.dump(final_data,fp=f)


if __name__ == "__main__":
    main()
##Write To a CSV File
# with open('Report.csv','w') as f:
#     writer = csv.DictWriter(f,fieldnames=final_data[0].keys())
#     writer.writeheader()
#     for item in final_data:
#         writer.writerow(item)
