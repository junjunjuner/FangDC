import pandas as pd
import pypinyin    #python汉字转拼音库
from pypinyin import pinyin, lazy_pinyin
df=pd.read_excel("城市列表及ID.xlsx")
city=df['二级'].drop_duplicates()
print(len(city))
# for c in city:
#     city_pinyin=''.join(lazy_pinyin(c))
#     print(city_pinyin)

# print(city)