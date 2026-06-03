# Gaming Analytics
Data analysis of Steam games collected from https://steamcharts.com

# Gaming Analytics - SQL Server & Power BI & Data Scrapper

## Description
A data analytics project focused on analyzing player trends across various games from 2012 to 2026 using SQL Server and Power BI.

## Data Structure / Data Model
- **Player_Count_Trend** (Fact/Timeseries Table): Historical data for average player count, peak concurrent users (PCU), and player fluctuations/trends.
- **Game_Details_Dim** (Dimension Table): Detailed metadata and attributes for each game.

## Quick Start / Setup Requirements

System Requirements:
- SQL Server 2019 or higher
- Power BI Desktop (Free from Microsoft)
- Git
- Python 3.14

## Key Insights
- **Counter-Strike 2** and **Dota 2** remain the top-performing games.
- **PUBG** achieved the highest peak player count but is currently experiencing a downward trend.
- **Bongo Cat** has recently gained positive momentum.
- Strong **seasonality patterns** are clearly visible across different games.

## Dashboard Architecture / Dashboard Layout
- **Overview**: Core KPIs (Avg Players, Peak Players, Games Up/Down).
- **Trend Analysis**: Line charts visualizing player trends over time.
- **Game Comparison**: Benchmarking performance across different games.
- **Detail Table**: Monthly granular data breakdown.
