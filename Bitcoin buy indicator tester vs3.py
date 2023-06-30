import relative_strength_index
import pandas as pd
import sqlite3
from tkinter import *

relativesi = relative_strength_index.FourteenDayRSI()
buy = 0
buy_good = 0
rsi_score = 0
skips = 0
periods_checked = 0

# Read the Excel file
df = pd.read_csv('/Users/jackdejeu/Desktop/Personal/Coding/Python/Bitcoin Project/BTC-USD.csv')

# Create an SQLite database connection
conn = sqlite3.connect('database.db')

# Insert the DataFrame into an SQLite table
df.to_sql('table_name', conn, if_exists='replace', index=False)

# Determine the maximum rowid in the table
# max_rowid = conn.execute("SELECT max(rowid) FROM table_name").fetchone()[0]

#for start_rowid in range(1, max_rowid - 14):
for start_rowid in range(1, 351):
    end_rowid = start_rowid + 13

    # Execute an SQL query to fetch the desired column values
    query1 = f"SELECT Close FROM table_name WHERE rowid >= {start_rowid} AND rowid <= {end_rowid}"
    result1 = conn.execute(query1).fetchall()

    query2 = f"SELECT Close FROM table_name WHERE rowid = {start_rowid + 14}"
    result2 = conn.execute(query2).fetchone()

    # Check if the result sets have the expected number of rows
    # if len(result1) != 13 or result2 is None:
    #     skips = skips + 1
    #     continue  # Skip this period if data is missing

    # Extract the values from result 1 and store them in an array
    closing_prices = [row[0] for row in result1]

    # This is the price the next day and is used to test if the stock actually went up
    real_price = float(result2[0])

    # This is the RSI
    rsi_pre = relativesi.rsi(closing_prices)

    # counting how many periods are checked
    periods_checked = periods_checked + 1

    if rsi_pre < 30:
        buy = buy + 1
        if real_price > closing_prices[12]:
            buy_good = buy_good + 1


root = Tk()
root.title('Analysis')
root.geometry("500x200")

# Create a text widget to display the output
output_text = Text(root, width=70, height=15, wrap=WORD)
output_text.pack()

def print_to_text_widget(message):
    indented_message = "    " + message
    output_text.insert(END, message)

print_to_text_widget(f"Using the historical bitcoin price data provided, {periods_checked} 14-day periods were checked.")

if buy != 0:
    rsi_score = (buy_good / buy) * 100
    print_to_text_widget("The Relative Strength Index as a buying predictor had an accuracy of {:.2f}%.".format(rsi_score))
else:
    print_to_text_widget("No bitcoin bought\n")

print_to_text_widget(f"Using the RSI, there were {buy} bitcoin bought. Of these purchases of bitcoin, the real closing price of bitcoin was higher the next day {buy_good} times.")


# Configure the font size of the text widget
output_text.configure(font=("Arial", 14))

root.mainloop()