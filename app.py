#必要なLibraryをimport
import requests, os, time, json
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import urllib.parse
from geopy.geocoders import GoogleV3
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pointbiserialr
import matplotlib.pyplot as plt
import japanize_matplotlib
import streamlit as st

# ページレイアウト
st.set_page_config(layout="wide")

# 訓練データの読み込み
df = pd.read_csv('物件情報.csv')

# Streamlitアプリの作成
st.title('HONNE!!')
st.markdown('#### 物件価格アプリ')


# 都道府県の選択
prefecture = st.sidebar.selectbox('都道府県を選択してください:', df['City'].unique())
filtered_df = df[df['City'] == prefecture]  # Filter DataFrame by selected 'City'

city = st.sidebar.selectbox('区を選択してください:', filtered_df['Street'].unique())
# 区の選択
filtered_df = df[df['Street'] == city]
# 地名の選択
#umber = st.sidebar.selectbox('地名を選択してください:', filtered_df['Number'].unique())
#filtered_df = df[df['Number'] == number]
type = st.sidebar.selectbox('部屋のタイプを選択してください：', filtered_df['Type'].unique())
filtered_df = df[df['Type'] == type]
# Sidebar selectboxes
min_space = filtered_df['Space'].min()
max_space = filtered_df['Space'].max()

space_range = st.sidebar.slider('広さを選択してください(㎡)：', min_value=min_space, max_value=max_space, value=(min_space, max_space))

filtered_df = df[(df['Space'] >= space_range[0]) & (df['Space'] <= space_range[1])]

bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300]

# ビニングを実行し、新しい列 'SpaceGroup' に結果を格納
filtered_df['SpaceGroup'] = pd.cut(filtered_df['Space'], bins=bins, labels=['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300'])

# Filter the DataFrame based on the selected space range
#filtered_df = df[df['Space'] == space_range]

#days_range = st.sidebar.selectbox('築日数を選択してください(日)：', filtered_df['Space'])

#filtered_df = df[df['DaysAgo']==days_range]


st.write('都道府県:', prefecture)
st.write('区:', city)
st.write('部屋のタイプ:', type)
st.write('部屋の広さ:', space_range)
#st.write('築日数：', days_range)

# Create a boxplot based on the selected data
plt.figure(figsize=(10, 6))
sns.boxplot(x='Space', y='Price', data=filtered_df)
plt.xlabel('Space (㎡)')
plt.xticks(rotation=90)
plt.ylabel('Price(万円)')
plt.title(f'Price Distribution by Space for {prefecture}, {city}, Type: {type}')
st.pyplot(plt)


# Assuming you have a DataFrame named 'df' and you want to select the 'Latitude' and 'Longitude' columns
# Create a new DataFrame containing only those columns
location_df = filtered_df[['latitude', 'longitude']]

location_df = location_df.dropna(subset=['latitude'])

# Display the map with the selected columns
st.map(location_df, use_container_width=True)
