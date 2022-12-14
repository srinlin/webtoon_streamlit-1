import streamlit as st 
import pandas as pd
from PIL import Image

from genre_model import genre_model
    
st.set_page_config(
    page_title="์นํฐ ์ถ์ฒ application",
    page_icon="๐",
    layout="wide",
)

image = Image.open('wating.jpg')

st.image(image)
st.title("""
         Welcome to Webtoon recommender system! 
         Shown is the Webtoon recommender system of Naver and Kakao! 
         ***
          """)

webtoon = pd.read_csv("webtoon_total_final.csv")
title_list = webtoon["title"].tolist()

st.header('์นํฐ์ ์ ๋ชฉ์ ์๋ ฅํด์ฃผ์ธ์ :)')
options = st.multiselect(
     '์นํฐ ์ ๋ชฉ์ ์๋ ฅํ๊ณ  Enter๋ฅผ ๋๋ฌ์ฃผ์ธ์.',
     title_list)
select_area = st.empty()

if not options:
    print(st.empty().info("์๋ ฅ์ ๊ธฐ๋ค๋ฆฌ๋ ์ค~~"))
    
st.dataframe(genre_model(options)[["title","score"]])   
