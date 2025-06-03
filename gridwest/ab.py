## FILE: ab.py 
## USE: Alberta Region Data

from baseWest import abHistoricalMapping, abSource

import pandas as pd
from datetime import datetime as dt

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
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y")
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Effective Begin (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H")

            datePart = df["Effective End (HE)"].str.slice(0, 10)
            hourPart = df["Effective End (HE)"].str.slice(11, 13)
            mask24 = hourPart == "24"
            date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y")
            date_fixed[mask24] += pd.Timedelta(days=1)
            hour_fixed = hourPart.where(~mask24, "00")
            df["Effective End (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H")

            df_other = df.drop(columns=["Effective Begin (HE)", "Effective End (HE)"]).convert_dtypes()
            df = pd.concat([df[["Effective Begin (HE)", "Effective End (HE)"]], df_other], axis=1)
    elif reportDate == 5:
        x = 1
    else:
        raise ValueError("❌ This report doesn't exist between these dates, please note some reports require no more than 31 days be requested at any time. Aditionally, please check your spelling or visit AESO.ca to view available reports.")
    
    return df

print(history(reportName='Secondary Offer Price Limit',startDate='11012023', endDate='12012023'))
