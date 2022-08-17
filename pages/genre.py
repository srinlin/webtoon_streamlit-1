import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd

st.markdown("# 장르 추천 🌈")
st.sidebar.markdown("# 장르 추천 🌈")

st.write("""
### 장르 추천
""")

webtoon = pd.read_csv("webtoon_total_final.csv")

# Sidebar - genre
sorted_unique_genre = sorted(webtoon.genre.unique())
selected_genre = st.sidebar.multiselect('genre', sorted_unique_genre)


if len(selected_genre) > 0:
   webtoon = webtoon[webtoon.genre.isin(selected_genre)]
   
st.dataframe(webtoon)

