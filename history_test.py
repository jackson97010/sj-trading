import datetime
import shioaji as sj
from login_test import login  # Assuming login_test.py is in the same directory
from shioaji.constant import Action, StockPriceType, OrderType
import pandas as pd
from shioaji import TickFOPv1, BidAskFOPv1, Exchange
import matplotlib.pyplot as plt
import seaborn as sns

api = login()

# Define the starting date and ending date
start_date = str(datetime.date(2024, 12, 15))
end_date = str(datetime.date.today())

# Generate a business date range and convert it to strings in "YYYY-MM-DD" format
date_range = pd.bdate_range(start=start_date, end=end_date)
date_str = date_range.strftime("%Y-%m-%d")

dataframes = []


# Option 1: Iterate directly over the date strings
for date in date_str:
    ticks = api.ticks(
        contract=api.Contracts.Stocks["2330"],
        date=date  # Using the formatted date string
    )
    df = pd.DataFrame({**ticks})
    df.ts = pd.to_datetime(df.ts)
    dataframes.append(df)
    
final_df = pd.concat(dataframes, ignore_index=True)
final_df.to_csv("tick_data_2330.csv", index=False)


filtered_volume = final_df.loc[(final_df['volume'] <= 499) & (final_df['volume'] >= 25), 'volume']
print(filtered_volume)
print("Volume Statistics:")
print("Mean:", filtered_volume.mean())
print("Median:", filtered_volume.median())
print("Standard Deviation:", filtered_volume.std())
    # Set up the plotting area
plt.figure(figsize=(10, 6))
    
    # Generate a histogram with KDE overlay using Seaborn
sns.histplot(filtered_volume, bins=50, kde=True, color='steelblue')
plt.title('Distribution of Volume')
plt.xlabel('Volume')
plt.ylabel('Frequency')
    
    # Show the plot
plt.show()