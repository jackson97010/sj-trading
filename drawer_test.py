import datetime
import shioaji as sj
from login_test import login  # Assuming login_test.py is in the same directory
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Login and get tick data
api = login()

# Define the date for tick data (e.g., February 3, 2025)
date = str(datetime.date(2025, 2, 3))

ticks = api.ticks(
    contract=api.Contracts.Stocks["2330"],
    date=date  # Using the formatted date string
)
df = pd.DataFrame({**ticks})

# Convert the 'ts' column to datetime objects
df['ts'] = pd.to_datetime(df['ts'])

# Extract only the time portion from the timestamp
df['time'] = df['ts'].dt.time

# Define a helper function to parse time strings with or without fractional seconds
def parse_time(s):
    try:
        return pd.to_datetime(s, format='%H:%M:%S.%f')
    except ValueError:
        return pd.to_datetime(s, format='%H:%M:%S')
    
df['time_dt'] = df['time'].apply(parse_time)

# Create the plot with two y-axes sharing the same x-axis (time)
fig, ax1 = plt.subplots(figsize=(12,6))

# Plot Price (using the 'close' column) on the left y-axis
ax1.plot(df['time_dt'], df['close'], marker='o', linestyle='-', color='red', label='Price')
ax1.set_xlabel('Time')
ax1.set_ylabel('Price', color='red')
ax1.tick_params(axis='y', labelcolor='red')

# Format the x-axis to display time properly
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)
ax1.grid(True)

# Create a second y-axis for Volume using twinx()
ax2 = ax1.twinx()
ax2.plot(df['time_dt'], df['volume'], marker='o', linestyle='-', color='blue', label='Volume')
ax2.set_ylabel('Volume', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

fig.tight_layout()
plt.title('Price and Volume vs Time')
plt.show()
