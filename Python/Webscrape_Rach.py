import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
import time

# Define Global Variables
thresh = [int(os.environ['upperthresh']), int(
    os.environ['lowerthresh'])]  # threshold high, low
#thresh=[150,-50]    # range outside which an email alert will be triggered
sender = 'price.alerts12@gmail.com' #email that is sending the alert
receivers = ["rmoglen@whiskerlabs.com", "r7m3w9d8e9v8q5m2@whiskerlabs.slack.com"]     #list of recievers of the alert
#receivers = ["rmoglen@whiskerlabs.com"]     #list of recievers of the alert, uncomment for debugging
email_pass = os.environ['password']

def scrape_website():
    """
    This method goes to the specified url and extracts the contents of the 
    table and the corresponding headers
    :param:
    :return: lists of all information scraped from the website
    :rtype: dict
    """
    site_data = {}   #define dictionary
    url = "http://www.ercot.com/content/cdr/html/real_time_spp" #url to be scraped
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all(class_="labelClassCenter")
    headers = soup.find_all(class_="headerValueClass")
    site_data['prices'] = [pt.get_text() for pt in prices]
    site_data['headers'] = [pt.get_text() for pt in headers]
    site_data['list_len'] = len(prices)
    return site_data


def trigger_alert(site_data):
    """
    This method checks the data that have been scraped from the website
    and descides if they are extreme enough to trigger an alert
    If they should trigger an alert, this function also builds a table
    of all the extreme prices, and their location, time, and date
    :param dict site_data: all information scraped from the website
    :return: lists of prices, dates, times, and locations with high prices
    :rtype: dict
    """
    alert_table = {}    #define dictionary
    alert_table['alert_price'] = []
    alert_table['alert_date'] = []
    alert_table['alert_timecode'] = []
    alert_table['alert_location'] = []
    alert_table['p_warning'] = False
    LZ_of_concern = [10, 12]  # LZ_Houston and LZ_North
    for i in LZ_of_concern:
        try:
            if ((float(site_data['prices'][site_data['list_len'] - 16 + i]) > 
                thresh[0] and float(site_data['prices'][site_data['list_len']- 
                32 + i]) < thresh[0]) or (float(site_data['prices']
                [site_data['list_len']- 16 + i]) < thresh[1] and 
                float(site_data['prices'][site_data['list_len']- 32 + i]) > 
                thresh[1])):
                #build table of extreme prices and their information
                alert_table['alert_price'].append(site_data['prices']
                    [site_data['list_len']- 16 + i])
                alert_table['alert_date'].append(site_data['prices']
                    [site_data['list_len']- 16])
                alert_table['alert_timecode'] .append(site_data['prices']
                    [site_data['list_len']- 15])
                alert_table['alert_location'].append(site_data['headers']
                    [i])
                #require an email alert to be sent
                alert_table['p_warning'] = True
        except:
            pass
    return alert_table


def format_email(alert_table):
    """
    This methods builds and formats the email that will be sent, and all the
    text that it will hold.
    :param dict alert_table: lists of prices, dates, times, and locations 
    with high prices
    :return: text that describes the email to be sent
    :rtype: str
    """
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = "," .join(receivers)
    msg['Subject'] = "Extreme Price Warning"
    html = """        <html>
      <body>
        One or more load zones has shown an extreme price outside the
        window of [%s, %s] 
        </br></br>
        <table border="1">
        <tr>
            <th> Oper Day </th>
            <th> Interval Ending </th>
            <th> SPP </th>
            <th> Location </th>
        </tr>""" % (str(thresh[1]), str(thresh[0]))
    for row in range(0, len(alert_table['alert_price'])):
        html += """<tr>
            <td> %s </td>
            <td> %s </td>
            <td> %s </td>
            <td> %s </td>
        </tr>""" % (str(alert_table['alert_date'][row]), str(alert_table
                    ['alert_timecode'][row]), str(alert_table['alert_price']
                    [row]), str(alert_table['alert_location'][row]))
    html += """</table> </br> The full table of prices is available 
        <a href="http://ercot.com/content/cdr/html/real_time_spp">here</a>.
        </p>
      </body>
    </html>"""
    msg.attach(MIMEText(html, 'html'))
    text = msg.as_string()
    return text


def send_email(text):
    """
    This method initializes the SMTP connection and sends the email alert
    :param str text: text that describes the email to be sent
    :return:
    :rtype:
    """
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.set_debuglevel(True)
    smtpObj.ehlo()
    time.sleep(1)
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login(sender, email_pass)
    time.sleep(1)
    smtpObj.sendmail(sender, receivers, text)
    print("Successfully sent price alert")
    time.sleep(1)
    smtpObj.quit()


def main(json_input, context):

    try:
        site_data = scrape_website()
    except:
        print("Failed to access website")

    alert_table = trigger_alert(site_data)

    #alert_table['p_warning'] = True   #uncomment to trigger alert for debugging

    if alert_table["p_warning"]:
        text = format_email(alert_table)
        send_email(text)

    print("FINISHED")

if __name__ == '__main__':
    main(json_input, context)