import simple_moving_average 
import pandas as pd
import sqlite3
import numpy as np
import random
import math

ma = simple_moving_average.SDSMA()
variance_sma = np.zeros(20)
alreadyused = []
s = 0 
sma_score = 0

# Read the Excel file
df = pd.read_csv('/Users/jackdejeu/Desktop/Personal/Coding/Python/Bitcoin Project/BTC-USD.csv')

#print(df)

# Create an SQLite database connection
conn = sqlite3.connect('database.db')

# Insert the DataFrame into an SQLite table
df.to_sql('table_name', conn, if_exists='replace', index=False)

# Specifing which column corrleates to which data in the file
#column_date = 'A'
#column_open = 'B'
#column_high = 'C'
#column_low = 'D'
#column_close = 'E'
#column_ajdclose = 'F'
#column_volume = 'G'

#this section of the program tests buy indicators with historical data at 20 random times
for i in range(20):

#need to create an algorithm for picking which 7 days to select 
    #add in exclusion of already used numbers
    start_rowid = random.randint(1, 357)
    end_rowid = start_rowid + 7

# Execute an SQL query to fetch the desired column values
    query1 = f"SELECT Close FROM table_name WHERE rowid >= {start_rowid} AND rowid <= {end_rowid}"
    result1 = conn.execute(query1).fetchall()

    query2 = f"SELECT Close FROM table_name WHERE rowid = {start_rowid + 8}"
    result2 = conn.execute(query2).fetchone()


    # Extract the values from result 1 and store them in an array
    numbers = [row[0] for row in result1]

    # Extract the values from result 2 and store them in an float
    real_price = float(result2[0])

    #getting the simple moving average
    smapre = ma.sma(numbers)

    #calculating the Sum of Squares for the simple moving average and the real price the next day
    variance_sma[i] = smapre - real_price

    if variance_sma[i] > 0:
        sma_score = sma_score + 1

print(sma_score)