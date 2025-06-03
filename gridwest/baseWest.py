import pandas as pd
import os

def abSource():
    """
    Base Function - URL Source
    ---
    Output: str, URL of AESO
    """
    
    return 'http://ets.aeso.ca/ets_web/ip/Market/Reports'

def abHistoricalMapping(input=None):
    """
    Base Function - Name Mapping
    ---
    + input: str, AESO Website Report Name (Format: 'Pool Price')
    ---
    Output: str, Backend Mapping ID For Data Download
    """

    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'map', 'abHistoricalMap.csv')
    df = pd.read_csv(csv_path)
    df = df[df['Operational'] == 1]

    if input:
        df = df[df['Report'] == input]

    if df.empty:
        print("❌ This report does not exist or is not currently operational. Please check your spelling or visit AESO.ca to view available reports.")
        return None

    return df
