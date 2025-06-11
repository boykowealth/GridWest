## FILE: mt.py 
## USE: Montana Region Data (Via Southwest Power Pool)

import requests
import pandas as pd
from io import BytesIO

def weis(report=None):
    """
    WEIS - Western Energy Services Current Data Request
    ---
    + report: str, Data Report Required (Format: '')
        + 'Forecast Summary'
        + 'Interchange Trend'
        + 'Generation Mix'
    ---
    Output: DataFrame, Current Reported Data
    """
    if report == 'Forecast Summary':
        url = "https://portal.spp.org/chart-api/weis-load-forecast/asFile"

        headers = {
            "accept": "*/*",
            "referer": "https://portal.spp.org/pages/weis-forecast-summary",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-xsrf-token": "3c94ee33-874e-4714-bc2e-215b3c29dde7"
        }

        cookies = {
            "_gid": "GA1.2.849622134.1749674772",
            "_ga_HYGY6K9055": "GS2.2.s1749674772$o1$g1$t1749674904$j60$l0$h0",
            "JSESSIONID": "F11F42151837729262918D742C9FE405",
            "XSRF-TOKEN": "3c94ee33-874e-4714-bc2e-215b3c29dde7",
            "_ga": "GA1.1.1871728114.1749674772",
            "_ga_37CS7YY6EF": "GS2.1.s1749674910$o1$g1$t1749676242$j60$l0$h0"
        }

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise f"Failed to fetch data. Status code: {response.status_code}"
    elif report == 'Interchange Trend':
        url = "https://portal.spp.org/chart-api/weis-interchange-trend/asFile"

        headers = {
            "accept": "*/*",
            "referer": "https://portal.spp.org/pages/weis-interchange-trend",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-xsrf-token": "3c94ee33-874e-4714-bc2e-215b3c29dde7"
        }

        cookies = {
            "_gid": "GA1.2.849622134.1749674772",
            "_ga_HYGY6K9055": "GS2.2.s1749674772$o1$g1$t1749674904$j60$l0$h0",
            "JSESSIONID": "F11F42151837729262918D742C9FE405",
            "XSRF-TOKEN": "3c94ee33-874e-4714-bc2e-215b3c29dde7",
            "_ga": "GA1.1.1871728114.1749674772",
            "_ga_37CS7YY6EF": "GS2.1.s1749674910$o1$g1$t1749676242$j60$l0$h0"
        }

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise f"Failed to fetch data. Status code: {response.status_code}"
    elif report == 'Generation Mix':
        url = "https://portal.spp.org/chart-api/weis-gen-mix/asFile"

        headers = {
            "accept": "*/*",
            "referer": "https://portal.spp.org/pages/weis-generation-mix",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-xsrf-token": "3c94ee33-874e-4714-bc2e-215b3c29dde7"
        }

        cookies = {
            "_gid": "GA1.2.849622134.1749674772",
            "_ga_HYGY6K9055": "GS2.2.s1749674772$o1$g1$t1749674904$j60$l0$h0",
            "JSESSIONID": "F11F42151837729262918D742C9FE405",
            "XSRF-TOKEN": "3c94ee33-874e-4714-bc2e-215b3c29dde7",
            "_ga": "GA1.1.1871728114.1749674772",
            "_ga_37CS7YY6EF": "GS2.1.s1749674910$o1$g1$t1749676242$j60$l0$h0"
        }

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise f"Failed to fetch data. Status code: {response.status_code}"
    else:
        raise "Please enter a valid report; 'Forecast Summary', 'Interchange Trend', 'Generation Mix'"
    
    return df

def integratedMarket(report=None):
    """
    Integrated Marketplace Forecast Current Data Request
    ---
    + report: str, Data Report Required (Format: '')
        + 'Forecast vs Actual'
        + 'Prices'
        + 'Generation Mix'
        + 'ACE'
    ---
    Output: DataFrame, Current Reported Data
    """
    if report == 'Forecast vs Actual':

        url = "https://portal.spp.org/chart-api/load-forecast/asFile"

        headers = {
            "accept": "*/*",
            "referer": "https://portal.spp.org/pages/integrated-marketplace-forecast-vs.-actual",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-xsrf-token": "3c94ee33-874e-4714-bc2e-215b3c29dde7"
        }

        cookies = {
            "_gid": "GA1.2.849622134.1749674772",
            "_ga_HYGY6K9055": "GS2.2.s1749674772$o1$g1$t1749674904$j60$l0$h0",
            "JSESSIONID": "F11F42151837729262918D742C9FE405",
            "XSRF-TOKEN": "3c94ee33-874e-4714-bc2e-215b3c29dde7",
            "_ga": "GA1.1.1871728114.1749674772",
            "_ga_37CS7YY6EF": "GS2.1.s1749674910$o1$g1$t1749677003$j60$l0$h0"
        }

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise f"Failed to fetch data. Status code: {response.status_code}"
    elif report == 'Prices':
        url = "https://portal.spp.org/chart-api/lmp-trend/asFile"

        headers = {
            "accept": "*/*",
            "referer": "https://portal.spp.org/pages/integrated-marketplace-hub-and-interface-prices",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-xsrf-token": "3c94ee33-874e-4714-bc2e-215b3c29dde7"
        }

        cookies = {
            "_gid": "GA1.2.849622134.1749674772",
            "_ga_HYGY6K9055": "GS2.2.s1749674772$o1$g1$t1749674904$j60$l0$h0",
            "JSESSIONID": "F11F42151837729262918D742C9FE405",
            "XSRF-TOKEN": "3c94ee33-874e-4714-bc2e-215b3c29dde7",
            "_ga": "GA1.1.1871728114.1749674772",
            "_ga_37CS7YY6EF": "GS2.1.s1749674910$o1$g1$t1749677003$j60$l0$h0"
        }

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise f"Failed to fetch data. Status code: {response.status_code}"
        
    elif report == 'Generation Mix':
        url = "https://portal.spp.org/chart-api/gen-mix/asFile"

        headers = {
            "accept": "*/*",
            "referer": "https://portal.spp.org/pages/integrated-marketplace-generation-mix",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-xsrf-token": "3c94ee33-874e-4714-bc2e-215b3c29dde7"
        }

        cookies = {
            "_gid": "GA1.2.849622134.1749674772",
            "_ga_HYGY6K9055": "GS2.2.s1749674772$o1$g1$t1749674904$j60$l0$h0",
            "JSESSIONID": "F11F42151837729262918D742C9FE405",
            "XSRF-TOKEN": "3c94ee33-874e-4714-bc2e-215b3c29dde7",
            "_ga": "GA1.1.1871728114.1749674772",
            "_ga_37CS7YY6EF": "GS2.1.s1749674910$o1$g1$t1749677003$j60$l0$h0"
        }

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise f"Failed to fetch data. Status code: {response.status_code}"     
    elif report == 'ACE':
        url = "https://portal.spp.org/chart-api/ace/asFile"

        headers = {
            "accept": "*/*",
            "referer": "https://portal.spp.org/pages/integrated-marketplace-ace-chart",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-xsrf-token": "3c94ee33-874e-4714-bc2e-215b3c29dde7"
        }

        cookies = {
            "_gid": "GA1.2.849622134.1749674772",
            "_ga_HYGY6K9055": "GS2.2.s1749674772$o1$g1$t1749674904$j60$l0$h0",
            "JSESSIONID": "F11F42151837729262918D742C9FE405",
            "XSRF-TOKEN": "3c94ee33-874e-4714-bc2e-215b3c29dde7",
            "_ga": "GA1.1.1871728114.1749674772",
            "_ga_37CS7YY6EF": "GS2.1.s1749674910$o1$g1$t1749677003$j60$l0$h0"
        }

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise f"Failed to fetch data. Status code: {response.status_code}"
    else:
        raise "Please enter a valid report; 'Forecast vs Actual', 'Prices', 'Generation Mix', 'ACE"

    return df

