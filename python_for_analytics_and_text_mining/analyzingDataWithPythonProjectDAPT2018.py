import pandas as pd
from pandas import ExcelWriter
import numpy as np
import matplotlib


# Read csv into a Pandas data frame
df = pd.read_csv("C:/Users/englerttw/Desktop/python_project/cwurData.csv", index_col=0) #File found on Kaggle.com --> https://www.kaggle.com/mylesoneill/world-university-rankings
#print(df)

print(df.shape)  # size of the data

print((df.dtypes))  # data types

print(df.columns)  # column names

df_Top1000 = df[["institution", "country"]]  # pick columns for the dataframe
print(df_Top1000)

#Select only the Top 10 Universitys on the List
top10 = df_Top1000[0:10]
print(top10)

# Write our Data Frame to an xlsx file
# save multiple tabs to one xlsx file
writer = ExcelWriter("C:/Users/englerttw/Desktop/python_project/World_University_Ratings.xlsx")
df_Top1000.to_excel(writer, sheet_name='Top_1000') #Sheet1 displays the global rank, institution name and country for all 1000 records
top10.to_excel(writer, sheet_name='Top_10') #Sheet2 displays the global rank, institution name, and country for the top 10 ranked universities
df.to_excel(writer, sheet_name='Raw_Data') #sheet3 displays all of the raw data
writer.save()