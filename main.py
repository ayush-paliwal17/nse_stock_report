from utils import bhav_copy_equities
from json2html import *
import datetime
import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(email_message):
    """Send email."""
    message = MIMEMultipart()
    message['Subject'] = 'Daily Portfolio Report'
    message['From'] = 'paliwal.ayush721@gmail.com'
    message['To'] = 'paliwal.ayush721@gmail.com'

    part = MIMEText(email_message, 'html')
    message.attach(part)

    email_client = boto3.client('ses', region_name='us-east-1')
    try:
        email_client.send_raw_email(
            Source='paliwal.ayush721@gmail.com',
            Destinations=['paliwal.ayush721@gmail.com'],
            RawMessage={
                'Data': message.as_string()
            }
        )
        print("Email Sent Successfully")
    except Exception:
        print(Exception)


def nse_data():
    """Get data From NSE for the specified Date"""
    date = (datetime.datetime.today()-datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    data = bhav_copy_equities(date)
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


def main(event,context):
    """Main Function"""
    final_data = []
    dict = [{'Name' :'ADANIENT','Quantity': 100,'Buying Price' : 2000},
            {'Name' :'IDEAFORGE','Quantity': 100,'Buying Price' : 650},
            {'Name' :'IRFC','Quantity': 2000,'Buying Price' : 65},
            {'Name' :'KPIGREEN','Quantity': 100,'Buying Price' : 800}]

    try:
        data = nse_data()
    except Exception:
        raise ValueError("NO DATA FOUND")
    else:
        for item in dict:
            dict_data = filter_data(data,item)
            final_data.append(dict_data)
        table = html_table(final_data)  

        send_email(email_message=table)
    


if __name__ == "__main__":
    main(None,None)