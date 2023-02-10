"""
classes to connect to criteo retail media api; auth.get_token() must be called in your driver class
Author: Ryan Morlando
Created:1/3/2023
Updated:
V1.0.0
Patch Notes:

To Do:
Add line items in
Handle more api responses
"""
import pandas as pd
import json
import requests
from time import sleep
from os import environ as env
from criteo_api import auth


def get_all_accounts() -> json:
    """
    Gets all the accounts associated with the credentials used to grab the api token
    :return: json with data
    """
    url = f'https://api.criteo.com/2022-10/retail-media/accounts'

    payload = {}

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        get_all_accounts()

    else:
        exit(response.text)


def get_all_brands(account_id: str) -> json:
    """
    gets all the brands associated with a specific account
    :param account_id: account ids can be found by calling get_all_accounts() or in the retail media portal account
    :return:
    """
    url = f'https://api.criteo.com/2022-10/retail-media/accounts/{account_id}/brands'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f'Get all brands request successful')
        # convert the response to a dataframe
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_all_brands(account_id=account_id)
    else:
        exit(f'{response.text}')


def get_all_line_items(account_id: str) -> json:
    """
    Gets all the line items for a specific account
    :param account_id: account ids can be found by calling get_all_accounts() or in the retail media portal account
    :return: json object
    """
    url = f'https://api.criteo.com/2022-10/retail-media/accounts/{account_id}/line-items'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f'Get all brands request successful')
        # convert the response to a dataframe
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_all_line_items(account_id=account_id)
    else:
        exit(f'{response.text}')


def get_all_campaign_ids(account_id: str) -> list:
    """
    Gets all the campaign ids associated with the account
    :param account_id: account ids can be found by calling get_all_accounts() or in the retail media portal account
    :return: list
    """
    url = f"https://api.criteo.com/2022-10/retail-media/accounts/{account_id}/campaigns"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f'Get all campaign ids request successful')
        # convert the response to a dataframe
        campaigns = pd.DataFrame(json.loads(response.text)['data'])

        return list(campaigns['id'].unique())

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_all_campaign_ids(account_id=account_id)
    else:
        exit(f'{response.text}')


def get_all_campaigns(account_id: str) -> json:
    """
    Gets all the campaign information associated with the account
    :param account_id: account ids can be found by calling get_all_accounts() or in the retail media portal account
    :return: json response
    """
    url = f"https://api.criteo.com/2022-10/retail-media/accounts/{account_id}/campaigns"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f'Get all campaigns request successful')
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_all_campaigns(account_id=account_id)

    else:
        exit(f'{response.text}')


def request_campaign_report(campaigns: list | str, report_type: str, start_date: str, end_date: str,
                            click_attr_window: str = None, view_attr_window: str = None) -> json:
    """
    Requests a campaign report based on all the parameters and returns the response
    :param campaigns: list of campaign ids or a str for single campaign
    :param report_type: one of (summary, pageType, keyword, productCategory, product, attributedTransactions)
    :param start_date: report start date
    :param end_date: report end date
    :param click_attr_window: click attribution window. One of (1D, 14D, 30D). Defaults to campaign value if None
    :param view_attr_window: view attribution window. One of (1D, 14D, 30D). Defaults to campaign value if None; Must be
    <= click_attr_window; Must be specified if click_attr_window is used
    :return: json object
    """
    url = "https://api.criteo.com/2022-10/retail-media/reports/campaigns"

    if type(campaigns) is list:
        attributes = {"ids": campaigns}

    else:
        attributes = {"id": f"{campaigns}"}

    attributes['reportType'] = report_type
    attributes['startDate'] = start_date
    attributes['endDate'] = end_date
    attributes['timeZone'] = "America/New_York"

    if click_attr_window is not None:
        attributes['clickAttributionWindow'] = click_attr_window

        if view_attr_window is None:
            exit('Can not use click attribution window without specifying view attribution window')
        else:
            attributes['viewAttributionWindow'] = view_attr_window

    else:
        if view_attr_window is not None:
            attributes['viewAttributionWindow'] = view_attr_window

    attributes['format'] = "json"

    payload = json.dumps({
        "data": {
            "type": "RetailMediaReportRequest",
            "attributes": attributes
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f'{report_type} report request successful')
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return request_campaign_report(campaigns=campaigns, report_type=report_type, start_date=start_date,
                                       end_date=end_date, click_attr_window=click_attr_window,
                                       view_attr_window=view_attr_window)

    else:
        exit(f'{response.text}')


def is_generated(report_id: str):
    """
    loops until file is no longer pending
    :param report_id: report id
    :return:
    """
    url = f"https://api.criteo.com/2022-04/retail-media/reports/{report_id}/status"
    headers = {
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        report_status = json.loads(response.text)['data']['attributes']['status']
        if report_status == 'success':
            print('File generated')
            return True
        elif report_status == 'pending':
            print('File still pending, trying again in 10 seconds')
            sleep(10)
            return is_generated(report_id=report_id)
        else:
            print('File generation failed')
            return False
    elif response.status_code == 401:
        print('refreshing token')
        auth.refresh_token()
        return is_generated(report_id=report_id)

    else:
        return False


def download_report(report_id: str) -> pd.DataFrame():
    """
    using a report id, downloads as json and converts to pandas dataframe
    :param report_id: report id
    :return: dataframe of report
    """
    url = f"https://api.criteo.com/2022-04/retail-media/reports/{report_id}/output"
    headers = {
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print("FIle download successful")
        return pd.DataFrame(json.loads(response.text))

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return download_report(report_id=report_id)

    else:
        exit(f'{response.text}')


def paginate(url: str) -> json:
    """
    gets data from the next page
    :param url: url to next page found in metadata of response
    :return:
    """
    headers = {
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print("File download successful")
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return paginate(url=url)

    else:
        exit(f'{response.text}')
