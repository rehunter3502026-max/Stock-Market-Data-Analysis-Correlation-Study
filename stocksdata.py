from google.colab import drive
drive.mount('/content/drive')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from copy import copy
from scipy import stats
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

stocks_df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Python & ML in Finance/Part 2. Financial Analysis in Python/stock.csv')
stocks_df

stocks_df = stocks_df.sort_values(by = ['Date'])
stocks_df
print('Total Number of stocks : {}'.format(len(stocks_df.columns[1:])))
print('Stocks under consideration are:')

for i in stocks_df.columns[1:]:
  print(i)

stocks_df.isnull().sum()

stocks_df.info()

def show_plot(df, fig_title):
  df.plot(x = 'Date', figsize = (15,7), linewidth = 3, title = fig_title)
  plt.grid()
  plt.show()

show_plot(stocks_df, 'RAW STOCK PRICES (WITHOUT NORMALIZATION)')

def interactive_plot(df, title):
  fig = px.line(title = title)
  
  # Loop through each stock (while ignoring time columns with index 0)
  for i in df.columns[1:]:
    fig.add_scatter(x = df['Date'], y = df[i], name = i) # add a new Scatter trace

  fig.show()

interactive_plot(stocks_df, 'Prices')

df = stocks_df['sp500']

# Define a dataframe names df_daily_return 
df_daily_return = df.copy()

#Loop through every element in the dataframe
for j in range(1, len(df)):

  # Calculate the percentage of change from the previous day
  df_daily_return[j] = ((df[j]- df[j-1])/df[j-1]) * 100

# put zero in the first line item
df_daily_return[0] = 0
df_daily_return

def daily_return(df):
  df_daily_return = df.copy()

  # Loop through each stock (while ignoring time columns with index 0)
  for i in df.columns[1:]:
    
    # Loop through each row belonging to the stock
    for j in range(1, len(df)):

      # Calculate the percentage of change from the previous day
      df_daily_return[i][j] = ((df[i][j]- df[i][j-1])/df[i][j-1]) * 100
    
    # set the value of first row to zero since the previous value is not available
    df_daily_return[i][0] = 0
  
  return df_daily_return

stocks_daily_return = daily_return(stocks_df)

cm = stocks_daily_return.drop(columns = ['Date']).corr()

plt.figure(figsize=(10, 10))
ax = plt.subplot()
sns.heatmap(cm, annot = True, ax = ax);
stocks_daily_return.hist(figsize=(10, 10), bins = 40);
