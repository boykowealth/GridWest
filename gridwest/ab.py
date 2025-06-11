## FILE: ab.py 
## USE: Alberta Region Data (Via AESO)

from baseWest import abHistoricalMapping, abSource, abCurrentMapping, abSDtMapping

import pandas as pd
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup

def history(reportName=None, startDate=None, endDate=None):
    """
    Pulls Historical Data From AESO.
    ---
    + report: str, Data Report Required (Format: '')
    + startDate: str, Start Date (Format: 'mmddyyyy')
    + endDate: str, End Date (Format: 'mmddyyyy')
    ---
    Output: DataFrame, Historical Data Time-Series
    """
    base = abSource()
    report = abHistoricalMapping(input=reportName)

    if not report.empty:
        report = report.reset_index(drop=True)
        reportId = report.loc[0, 'ReportID']
        reportDate = report.loc[0, 'DateID']
        rowSkip = int(report.loc[0, 'Row'])
    else:
        raise ValueError("This report does not exist.")

    url = f'{base}/{reportId}?beginDate={startDate}&endDate={endDate}&contentType=csv'
    df = pd.read_csv(url, skiprows=rowSkip)

    if reportDate == 1:
        df["HE"] = pd.to_numeric(df["HE"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
        df = df.dropna(subset=["HE"])
        df["HE"] = df["HE"].astype(int)
        date_part = pd.to_datetime(df["Date"], format="%m/%d/%Y")
        hour_part = df["HE"]
        mask24 = hour_part == 24
        date_part[mask24] += pd.Timedelta(days=1)
        hour_part = hour_part.where(~mask24, 0)
        df["Datetime"] = pd.to_datetime(date_part.dt.strftime("%Y-%m-%d") + " " + hour_part.astype(str).str.zfill(2), format="%Y-%m-%d %H")
        df.drop(columns=["Date", "HE"], inplace=True)
        df = df[["Datetime"] + [col for col in df.columns if col != "Datetime"]]

        df_other = df.drop(columns=["Datetime"]).convert_dtypes()
        df = pd.concat([df[["Datetime"]], df_other], axis=1)

    elif reportDate == 2:
        dateCol = next((col for col in df.columns if "date" in col.lower()), None) ## CHECK DATE COLUMN NAME
        if dateCol == "Date (HE)":
            datePart = df["Date (HE)"].str.slice(0, 10)
            hourPart = df["Date (HE)"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y")
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Date (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H")

            df_other = df.drop(columns=["Date (HE)"]).convert_dtypes()
            df = pd.concat([df[["Date (HE)"]], df_other], axis=1)
        else:
            datePart = df["Date"].str.slice(0, 10)
            hourPart = df["Date"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y")
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Date"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H")

            df_other = df.drop(columns=["Date"]).convert_dtypes()
            df = pd.concat([df[["Date"]], df_other], axis=1)
    elif reportDate == 3:
        dateCol = next((col for col in df.columns if "date" in col.lower()), None) ## CHECK DATE COLUMN NAME
        if dateCol == "Date":
            df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")

            df_other = df.drop(columns=["Date"]).convert_dtypes()
            df = pd.concat([df[["Date"]], df_other], axis=1)
        else:
            df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")
            
            df_other = df.drop(columns=["Date/Time"]).convert_dtypes()
            df = pd.concat([df[["Date/Time"]], df_other], axis=1)
    elif reportDate == 4:
            df.columns = df.columns.str.strip()
            datePart = df["Effective Begin (HE)"].str.slice(0, 10)
            hourPart = df["Effective Begin (HE)"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y", errors='coerce')
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Effective Begin (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H", errors="coerce")

            datePart = df["Effective End (HE)"].str.slice(0, 10)
            hourPart = df["Effective End (HE)"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y", errors='coerce')
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Effective End (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H", errors="coerce")

            df_other = df.drop(columns=["Effective Begin (HE)", "Effective End (HE)"]).convert_dtypes()
            df = pd.concat([df[["Effective Begin (HE)", "Effective End (HE)"]], df_other], axis=1)
    elif reportDate == 5:
        df_other = df.convert_dtypes()
    else:
        raise ValueError("This report doesn't exist between these dates, please note some reports require no more than 31 days be requested at any time. Aditionally, please check your spelling or visit AESO.ca to view available reports.")
    
    return df

def current(reportName=None):
    base = abSource()
    report = abCurrentMapping(input=reportName)

    if not report.empty:
        report = report.reset_index(drop=True)
        reportId = report.loc[0, 'ReportID']
        reportDate = report.loc[0, 'DateID']
        rowSkip = int(report.loc[0, 'Row'])
    else:
        raise ValueError("This report does not exist.")

    url = f'{base}/{reportId}?beginDate=&endDate=&contentType=csv'
    df = pd.read_csv(url, skiprows=rowSkip)

    if reportDate == 1:
        df["HE"] = pd.to_numeric(df["HE"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
        df = df.dropna(subset=["HE"])
        df["HE"] = df["HE"].astype(int)
        date_part = pd.to_datetime(df["Date"], format="%m/%d/%Y")
        hour_part = df["HE"]
        mask24 = hour_part == 24
        date_part[mask24] += pd.Timedelta(days=1)
        hour_part = hour_part.where(~mask24, 0)
        df["Datetime"] = pd.to_datetime(date_part.dt.strftime("%Y-%m-%d") + " " + hour_part.astype(str).str.zfill(2), format="%Y-%m-%d %H")
        df.drop(columns=["Date", "HE"], inplace=True)
        df = df[["Datetime"] + [col for col in df.columns if col != "Datetime"]]

        df_other = df.drop(columns=["Datetime"]).convert_dtypes()
        df = pd.concat([df[["Datetime"]], df_other], axis=1)

    elif reportDate == 2:
        dateCol = next((col for col in df.columns if "date" in col.lower()), None) ## CHECK DATE COLUMN NAME
        if dateCol == "Date (HE)":
            datePart = df["Date (HE)"].str.slice(0, 10)
            hourPart = df["Date (HE)"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y")
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Date (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H")

            df_other = df.drop(columns=["Date (HE)"]).convert_dtypes()
            df = pd.concat([df[["Date (HE)"]], df_other], axis=1)
        else:
            datePart = df["Date"].str.slice(0, 10)
            hourPart = df["Date"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y")
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Date"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H")

            df_other = df.drop(columns=["Date"]).convert_dtypes()
            df = pd.concat([df[["Date"]], df_other], axis=1)
    elif reportDate == 3:
        dateCol = next((col for col in df.columns if "date" in col.lower()), None) ## CHECK DATE COLUMN NAME
        if dateCol == "Date":
            df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")

            df_other = df.drop(columns=["Date"]).convert_dtypes()
            df = pd.concat([df[["Date"]], df_other], axis=1)
        else:
            df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")
            
            df_other = df.drop(columns=["Date/Time"]).convert_dtypes()
            df = pd.concat([df[["Date/Time"]], df_other], axis=1)
    elif reportDate == 4:
            df.columns = df.columns.str.strip()
            datePart = df["Effective Begin (HE)"].str.slice(0, 10)
            hourPart = df["Effective Begin (HE)"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y", errors='coerce')
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Effective Begin (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H", errors="coerce")

            datePart = df["Effective End (HE)"].str.slice(0, 10)
            hourPart = df["Effective End (HE)"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y", errors='coerce')
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Effective End (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H", errors="coerce")

            df_other = df.drop(columns=["Effective Begin (HE)", "Effective End (HE)"]).convert_dtypes()
            df = pd.concat([df[["Effective Begin (HE)", "Effective End (HE)"]], df_other], axis=1)
    elif reportDate == 5:
        df_other = df.convert_dtypes()
    else:
        raise ValueError("This report doesn't exist between these dates, please note some reports require no more than 31 days be requested at any time. Aditionally, please check your spelling or visit AESO.ca to view available reports.")

    return df

def supplyForecasts(reportPeriod):
    """
    Pulls 24 Month Supply and Demand Forecasts From AESO.
    ---

    + reportPeriod: str, Forecast Period Required (Format: '1-6')
        + '1-6': Daily Peak Hour (one month-six months)
        + '2-6': Daily Peak Hour (two months-six months)
        + '3-6': Daily Peak Hour (three months-six months)
        + '4-6': Daily Peak Hour (four months-six months)

    ---
    Output: DataFrame, Forecasted Time Series
    """

    url = f'http://ets.aeso.ca/Market/Reports/Manual/supply_and_demand/csvData/{reportPeriod}month.csv'

    try:
        df = pd.read_csv(url, on_bad_lines='skip').dropna()
        df = df.convert_dtypes()
    except:
        raise ValueError('Please provide a correct forecasting period.')
    
    return df

def currentSD():
    """
    Pulls The Current Supply Demand Report (GROUP, MC, TNG, DCR) From AESO.
    ---
    Output: DataFrame, Supply and Deman Measures Per Group/Type
    """
    url = "http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise f"Error: Connection Status code {response.status_code}"
    
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    data = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [col.text.strip() for col in cols]
            if cols:
                data.append(cols)

    if not data:
        raise "No Current data found."
    
    data = data[20:]

    df = pd.DataFrame(data)
    df.columns = df.iloc[0] 
    df = df[1:].reset_index(drop=True)
    df = df[['GROUP', 'MC', 'TNG', 'DCR']]
    df = df[df['GROUP'] != 'ASSET']

    mapsd = abSDtMapping()

    df = pd.merge(df, mapsd, how='left', on='GROUP')

    df['GROUP'] = df['GROUP'].str.title()
    df['MC'] = pd.to_numeric(df['MC'], errors='coerce')
    df['TNG'] = pd.to_numeric(df['TNG'], errors='coerce')
    df['DCR'] = pd.to_numeric(df['DCR'], errors='coerce')

    return df