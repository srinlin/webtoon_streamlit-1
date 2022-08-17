import streamlit as st 
import pandas as pd
from PIL import Image

from genre_model import genre_model
    
st.set_page_config(
    page_title="웹툰 추천 application",
    page_icon="📚",
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

st.header('웹툰의 제목을 입력해주세요 :)')
options = st.multiselect(
     '웹툰 제목을 입력하고 Enter를 눌러주세요.',
     title_list)
select_area = st.empty()

if not options:
    print(st.empty().info("입력을 기다리는 중~~"))
    
st.dataframe(genre_model(options)[["title","score"]])   
