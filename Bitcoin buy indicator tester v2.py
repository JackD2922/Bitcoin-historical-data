#Bitcoin buy indicator tester v2
#this version tests 20 random 14 day periods

import relative_strength_index
import pandas as pd
import sqlite3
import numpy as np
import random

relativesi = relative_strength_index.FourteenDayRSI()
real_price = 0
#alreadyused = []
buy = 0 
buy_good = 0
rsi_score = 0

# Read the Excel file
df = pd.read_csv('/Users/jackdejeu/Desktop/Personal/Coding/Python/Bitcoin Project/BTC-USD.csv')

#print(df)

# Create an SQLite database connection
conn = sqlite3.connect('database.db')

# Insert the DataFrame into an SQLite table
df.to_sql('table_name', conn, if_exists='replace', index=False)

# Specifying which column correlates to which data in the file
#column_date = 'A'
#column_open = 'B'
#column_high = 'C'
#column_low = 'D'
#column_close = 'E'
#column_ajdclose = 'F'
#column_volume = 'G'

for i in range(20):

    #need to create an algorithm for picking which 7 days to select 
    #add in exclusion of already used numbers
    start_rowid = random.randint(1, 351)
    end_rowid = start_rowid + 14

    # Execute an SQL query to fetch the desired column values
    query1 = f"SELECT Close FROM table_name WHERE rowid >= {start_rowid} AND rowid <= {end_rowid}"
    result1 = conn.execute(query1).fetchall()

    query2 = f"SELECT Close FROM table_name WHERE rowid = {start_rowid + 15}"
    result2 = conn.execute(query2).fetchone()

    # Extract the values from result 1 and store them in an array
    closing_prices = [row[0] for row in result1]

    #this is the price the next day and is used to test if the stock actually went up
    real_price = float(result2[0])

    #this is the RSI
    rsi_pre = relativesi.rsi(closing_prices)

    if rsi_pre < 30:
        buy = buy + 1
        if real_price > closing_prices [12]:
            buy_good = buy_good + 1

if buy != 0:
    rsi_score = (buy_good / buy) * 100
    print("RSI accuracy = {:.2f}%".format(rsi_score))
else:
    # Assign a default value or any value that makes sense in your context
    print("nothing was bought")

print("number of good buys = " + str(buy_good))
print("Number of buys = " + str(buy))