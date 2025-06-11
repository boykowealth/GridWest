# GridWest

The GridWest Data Package is a comprehensive Python library designed to streamline access and processing of historical and real-time electricity market data across Western North America. This package currently supports data retrieval and management for four key regions:

+ Alberta (AESO)
+ Saskatchewan (SaskPower - Crown Corporation)
+ British Columbia (BC Hydro - Crown Corporation)
+ Montana (SPP)

It provides traders, analysts, and energy professionals with easy-to-use functions to pull, clean, and analyze power market time-series data crucial for trading, risk management, and operational decision-making.

## Purpose

Developed specifically for Western Power Traders, this package condenses disparate data sources into consistent, ready-to-use Pandas DataFrames. It handles the unique formatting quirks, timestamp conversions, and dataset variations found across different regional market operators.

Whether you're assessing historical price trends, load forecasts, or ancillary service reports, this package saves you significant time and effort by automating data retrieval and preprocessing.

## Package Modules

+ __Alberta (gridwest.ab):__ Accesses AESO (Alberta Electric System Operator) historical and operational reports. Handles multiple report types with varying date/time formats. Provides flexible querying by report name and date range.
+ __Saskatchewan (gridwest.sk):__ Interfaces with SaskPower's public data portals and report feeds. Standardizes load, generation, and price datasets. Supports time-series extraction and cleaning.
+ __British Columbia (gridwest.bc):__ Pulls data from BC Hydro and BC Utilities commission sources. Manages multiple data formats and interval types. Converts timestamps and adjusts for time zone differences.
+ __Montana (gridwest.mt):__ Connects to Southwest Power Pool (SPP) public datasets.Aggregates generation, demand, and pricing information. Normalizes data for use in cross-border market analysis.

## Installation

```
pip install gridwest
```

## Contact

Brayden Boyko

Email: braydenboyko@boykowealth.com

## License

The following project is made available under the GPL.

## Documentation

[⬇️ Download docs](https://github.com/boykowealth/GridWest/releases/download/Docs/docs.html)

