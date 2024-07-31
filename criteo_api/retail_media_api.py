"""
functions to connect to criteo retail media api; auth.get_token() must be called in your driver class
Author: Ryan Morlando
Created:1/3/2023
Updated:
V1.0.1
Patch Notes:
-Updated to newest stable version 2024-01
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
    url = f'https://api.criteo.com/2024-01/retail-media/accounts'

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
    url = f'https://api.criteo.com/2024-01/retail-media/accounts/{account_id}/brands?pageSize=50'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        # convert the response to a dataframe
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_all_brands(account_id=account_id)
    else:
        exit(f'{response.text}')


def get_all_retailers(account_id: str) -> json:
    """
    Gets all the retialers for a specific account
    :param account_id: account ids can be found by calling get_all_accounts() or in the retail media portal account
    :return: json object
    """
    url = f'https://api.criteo.com/2024-01/retail-media/accounts/{account_id}/retailers?pageSize=50'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        # return response
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_all_retailers(account_id=account_id)
    else:
        exit(f'{response.text}')


def get_all_line_items(account_id: str) -> json:
    """
    Gets all the line items for a specific account
    :param account_id: account ids can be found by calling get_all_accounts() or in the retail media portal account
    :return: json object
    """
    url = f'https://api.criteo.com/2024-01/retail-media/accounts/{account_id}/line-items?pageSize=50'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        # return reponse
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_all_line_items(account_id=account_id)
    else:
        exit(f'{response.text}')


def get_line_item_products(line_item_id: str) -> json:
    """
    gets all the products for a specific line item group
    :param line_item_id: id for a line item group
    :return: json object
    """
    url = f'https://api.criteo.com/2024-01/retail-media/line-items/{line_item_id}/products?pageSize=50'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        # convert the response to a dataframe
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return get_line_item_products(line_item_id=line_item_id)
    else:
        exit(f'{response.text}')


def get_all_campaign_ids(account_id: str) -> list:
    """
    Gets all the campaign ids associated with the account
    :param account_id: account ids can be found by calling get_all_accounts() or in the retail media portal account
    :return: list
    """
    url = f"https://api.criteo.com/2024-01/retail-media/accounts/{account_id}/campaigns?pageSize=50"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
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
    url = f"https://api.criteo.com/2024-01/retail-media/accounts/{account_id}/campaigns?pageSize=50"

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
        return get_all_campaigns(account_id=account_id)

    else:
        exit(f'{response.text}')


def request_report(endpoint: str, ids: list | str, report_type: str, start_date: str, end_date: str,
                   click_attr_window: str = None, view_attr_window: str = None,
                   metrics: list = None, dimensions: list = None, sales_chanel: str = None,) -> json:
    """
    Requests a line item report based on all the parameters and returns the response
    :param endpoint: str: 'line-items' or 'campaigns'
    :param ids: list of ids or a single id str. Either campaign or line item ids depending on endpoint
    :param report_type: one of (summary, pageType, keyword, productCategory, product, attributedTransactions)
    :param start_date: report start date
    :param end_date: report end date
    :param metrics: List of metrics to have in the requested report
    :param dimensions: List of dimensions to have in the requested report
    :param sales_chanel: One of (offline, online)
    :param click_attr_window: click attribution window. One of (1D, 14D, 30D). Defaults to campaign value if None;
    Must be specified if click_attr_window is used
    :param view_attr_window: view attribution window. One of (none, 1D, 14D, 30D). Defaults to campaign value if None;
    Must be <= click_attr_window; Must be specified if click_attr_window is used
    :return: json object
    """
    if endpoint != 'line-items' and endpoint != 'campaigns':
        exit('invalid endpoint. Must be one of line-items or campaigns')

    url = f"https://api.criteo.com/2024-01/retail-media/reports/{endpoint}"

    if type(ids) is list:
        attributes = {"ids": ids}

    else:
        attributes = {"id": f"{ids}"}

    attributes['reportType'] = report_type
    attributes['startDate'] = start_date
    attributes['endDate'] = end_date
    attributes['timeZone'] = "America/New_York"
    attributes['campaignType'] = 'sponsoredProducts'
    if metrics:
        attributes['metrics'] = metrics
    if dimensions:
        attributes['dimensions'] = dimensions
    if sales_chanel:
        attributes['salesChannel'] = sales_chanel

    if click_attr_window is not None:
        attributes['clickAttributionWindow'] = click_attr_window

        if view_attr_window is None:
            exit('Can not use click attribution window without specifying view attribution window')
        else:
            attributes['viewAttributionWindow'] = view_attr_window

    else:
        if view_attr_window is not None:
            exit('Can not use view attribution window without specifying click attribution window')

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
        print(f'{endpoint}/{report_type} report request successful')
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return request_report(endpoint=endpoint, ids=ids, report_type=report_type, start_date=start_date,
                              end_date=end_date, click_attr_window=click_attr_window, view_attr_window=view_attr_window)

    else:
        exit(f'{response.text}')


def is_generated(report_id: str):
    """
    loops until file is no longer pending
    :param report_id: report id
    :return:
    """
    url = f"https://api.criteo.com/2024-01/retail-media/reports/{report_id}/status"
    headers = {
        'Accept': 'application/json',
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
    url = f"https://api.criteo.com/2024-01/retail-media/reports/{report_id}/output"
    headers = {
        'Accept': 'application/octet-stream',
        'Authorization': f'Bearer {env.get("criteo_access_token")}'
    }
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print("File download successful")
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
        print("Moved to next page")
        return json.loads(response.text)

    elif response.status_code == 401:
        print('Refreshing Token')
        auth.refresh_token()
        return paginate(url=url)

    else:
        exit(f'{response.text}')
