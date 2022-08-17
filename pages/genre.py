import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.markdown("# 장르 추천 🌈")

# 데이터 프레임 불러오고 전처리 하기
df = pd.read_csv("webtoon_total_final.csv")

title_list = df["title"].tolist()

df = df[['title','score', 'genre']]
df.genre = df.genre.str.strip('['']')

#데이터 프레임 체크 박스 만들기
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gridoptions = gd.build()

# st.header('웹툰의 제목을 입력해주세요 :)')
# options = st.multiselect(
#      '웹툰 제목을 입력하고 Enter를 눌러주세요.',
#      title_list)
# select_area = st.empty()

# if not options:
#     print(st.empty().info("입력을 기다리는 중~~"))
    
grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)


   
st.write('## Selected')
selected_row = grid_table["selected_rows"]


st.dataframe(selected_row['title'])

# tmp = pd.get_dummies(df.genre)

# def col_change(df):
#     for col in df.columns:
#         if ',' in col:
#             col_sep = col.split(', ')
#             df[col_sep[0]] = df[col_sep[0]] + df[col]
#             df[col_sep[1]] = df[col_sep[1]] + df[col]
#             df.drop(columns=[f'{col}'], inplace=True)
#     return df

# col_change(tmp)

# genre_df = col_change(pd.get_dummies(df.genre))
# df = pd.concat([df.title, df.score, genre_df], axis=1)

# df.columns = df.columns.str.strip('\'')

# def one_genre(title):
#     """
#     장르 하나의 
#     """
#     g_row = df[df.title == title]
#     genres = g_row[df.columns[2:]]
#     return genres.values

# def genres(title_list):
#     genre_list = [0]*9
#     for title in title_list:
#         genre_list = genre_list + one_genre(title)
#     return genre_list

# # 시청 목록과 장르 유사도 높은 웹툰 중 평점 높은 10개
# score = genre_df.to_numpy()

# def genre_model(title_list):
#     local_score = np.append(score, genres(title_list), axis=0)
#     cosine_similar = cosine_similarity(local_score, local_score)
#     cosine_similar_data = pd.DataFrame(cosine_similar)

#     genre_user = cosine_similar_data.tail(1).T.sort_values(by=cosine_similar_data.columns[-1], ascending=False)
#     max_score = genre_user.values[1][0]
    
#     max_index = list(genre_user[(genre_user.values) == max_score].index)

#     if df.shape[0] in max_index:
#         max_index.remove(df.shape[0])

#     sorted_df = df.loc[max_index].sort_values(by='score', ascending=False)

#     if len(max_index) < 10:
#         return sorted_df
    
#     else:
#         min_score = sorted_df.iloc[9].score
#         ind = 0
#         for i in range(10):
#             if sorted_df.iloc[i].score == min_score:
#                 ind = i
#                 break
#         randnum = sorted_df[sorted_df.score == min_score].shape[0]
#         randlist = random.sample(range(ind, ind + randnum), 10 - ind)
#         tdf1, tdf2 = sorted_df[:ind], sorted_df.iloc[randlist]
#         sorted_df = pd.concat([tdf1, tdf2])

#         return sorted_df
   
# g = genre_model( list_input )

# st.dataframe(g)

