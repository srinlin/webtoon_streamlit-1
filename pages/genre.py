import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
import numpy as np
import random

from sklearn.metrics.pairwise import cosine_similarity

from IPython.core.display import HTML

st.markdown("# ์ฅ๋ฅด ์ถ์ฒ ๐")

# ๋ฐ์ดํฐ ํ๋ ์ ๋ถ๋ฌ์ค๊ณ  ์ ์ฒ๋ฆฌ ํ๊ธฐ
df_origin = pd.read_csv("webtoon_total_final.csv")

raw_title_list = df_origin["title"].tolist()

df = df_origin[['title','score', 'genre']]
df.genre = df.genre.str.strip('['']')

#๋ฐ์ดํฐ ํ๋ ์ ์ฒดํฌ ๋ฐ์ค ๋ง๋ค๊ธฐ
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gridoptions = gd.build()

# st.header('์นํฐ์ ์ ๋ชฉ์ ์๋ ฅํด์ฃผ์ธ์ :)')
# options = st.multiselect(
#      '์นํฐ ์ ๋ชฉ์ ์๋ ฅํ๊ณ  Enter๋ฅผ ๋๋ฌ์ฃผ์ธ์.',
#      raw_title_list)
# select_area = st.empty()

# if not options:
#     print(st.empty().info("์๋ ฅ์ ๊ธฐ๋ค๋ฆฌ๋ ์ค~~"))
    
grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)


   
st.write('## Selected')

selected_row = grid_table["selected_rows"]

# ์ ํํ ํ์ ์ ๋ชฉ๋ค์ ๋ฆฌ์คํธ ํํ๋ก ์ถ์ถํ๋ค.
st.dataframe(selected_row)

df2 = pd.DataFrame(selected_row)

if len(df2) == 0:
    title_input=[]
else:
    title_input = df2.title.tolist()

# ์ฅ๋ฅด ์ ์ฌ๋ ๊ณ์ฐํ๋ ํจ์ ๋ง๋ค๊ธฐ
tmp = pd.get_dummies(df.genre)

def col_change(df):
    for col in df.columns:
        if ',' in col:
            col_sep = col.split(', ')
            df[col_sep[0]] = df[col_sep[0]] + df[col]
            df[col_sep[1]] = df[col_sep[1]] + df[col]
            df.drop(columns=[f'{col}'], inplace=True)
    return df

col_change(tmp)

genre_df = col_change(pd.get_dummies(df.genre))
df = pd.concat([df.title, df.score, genre_df], axis=1)

df.columns = df.columns.str.strip('\'')

def one_genre(title):
    """
    ์ฅ๋ฅด ํ๋์ 
    """
    g_row = df[df.title == title]
    genres = g_row[df.columns[2:]]
    return genres.values

def genres(title_list):
    genre_list = [0]*9
    for title in title_list:
        genre_list = genre_list + one_genre(title)
    return genre_list

# ์์ฒญ ๋ชฉ๋ก๊ณผ ์ฅ๋ฅด ์ ์ฌ๋ ๋์ ์นํฐ ์ค ํ์  ๋์ 10๊ฐ
score = genre_df.to_numpy()

def genre_model(title_list=[]):
    if not title_list:
        st.write("์์ง ์ ํํ ์นํฐ์ด ์์ต๋๋ค")
        return pd.DataFrame()
    
    local_score = np.append(score, genres(title_list), axis=0)
    cosine_similar = cosine_similarity(local_score, local_score)
    cosine_similar_data = pd.DataFrame(cosine_similar)

    genre_user = cosine_similar_data.tail(1).T.sort_values(by=cosine_similar_data.columns[-1], ascending=False)
    max_score = genre_user.values[1][0]
    
    max_index = list(genre_user[(genre_user.values) == max_score].index)

    if df.shape[0] in max_index:
        max_index.remove(df.shape[0])

    sorted_df = df.loc[max_index].sort_values(by='score', ascending=False)

    if len(max_index) < 10:
        indlist = sorted_df.index
        return df_origin.loc[indlist]
    
    else:
        min_score = sorted_df.iloc[9].score
        ind = 0
        for i in range(10):
            if sorted_df.iloc[i].score == min_score:
                ind = i
                break
        randnum = sorted_df[sorted_df.score == min_score].shape[0]
        randlist = random.sample(range(ind, ind + randnum), 10 - ind)
        tdf1, tdf2 = sorted_df[:ind], sorted_df.iloc[randlist]
        sorted_df = pd.concat([tdf1, tdf2])
        indlist = sorted_df.index

        return df_origin.loc[indlist]
   
g = genre_model(title_input)

if len(g) == 0:
    st.write('์นํฐ ํญ๋ชฉ์์ ์ต์ ํ๋์ ์นํฐ์ ์ ํํด์ฃผ์ธ์!')
    
elif len(g) != 0:
    df_result = g[['title', 'artist', 'genre','story','score','image']]
    def to_img_tag(path):
        return '<img src="'+ path + '" width="100" >'
    a= HTML(df_result.to_html(escape=False,formatters=dict(image=to_img_tag)))
    st.write(a)



