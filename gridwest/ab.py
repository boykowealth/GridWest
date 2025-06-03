## FILE: ab.py 
## USE: Alberta Region Data

from baseWest import abHistoricalMapping, abSource

import pandas as pd
from datetime import datetime as dt

def history(report=None, startDate=None, endDate=None):
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
    reportId = 1

    url = f'{base}/{report}?beginDate={startDate}&endDate={endDate}&contentType=csv'
    df = pd.read_csv(url, skiprows=4)

    ## FIX DATE HOUR FORMAT
    datePart = df["Date (HE)"].str.slice(0, 10)
    hourPart = df["Date (HE)"].str.slice(11, 13)
    mask24 = hourPart == "24"
    date_fixed = pd.to_datetime(datePart, format="%m/%d/%Y")
    date_fixed[mask24] += pd.Timedelta(days=1)
    hour_fixed = hourPart.where(~mask24, "00")
    df["Date (HE)"] = pd.to_datetime(date_fixed.dt.strftime("%m/%d/%Y") + " " + hour_fixed, format="%m/%d/%Y %H")
    
    df.loc[:, df.columns != 'Date (HE)'] = df.loc[:, df.columns != 'Date (HE)'].apply(pd.to_numeric, errors='coerce')

    return df

history(report='DdsPaymentSummaryReportServlet',startDate='11012023', endDate='12012023')

## PublicSummaryAllReportServlet
## HistoricalPoolPriceReportServlet
## DdsPaymentSummaryReportServlet