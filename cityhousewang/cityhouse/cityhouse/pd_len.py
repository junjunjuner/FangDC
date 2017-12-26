import pandas as pd
df1=pd.read_csv("城市房产-城市数据.csv")
df2=pd.read_csv("城市房产链接.csv")
c1=df1['city'].dropna().drop_duplicates().values
print(len(c1))
c2=df2['city'].dropna().drop_duplicates().values
print(len(c2))
co1=df1['county'].dropna().drop_duplicates().values
print(len(co1))
co2=df2['county'].dropna().drop_duplicates().values
print(len(co2))
for city in c2:
    if city not in c1:
        print("city:",city)
for county in co2:
    if county not in co1:
        print(county)