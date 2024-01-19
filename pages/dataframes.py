import streamlit as st
import backend_league as bl

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.title("Dataframes")

col1, col2 = st.columns(2, gap="large")

# df
with col1:
    st.header("Recent Games", divider="orange")

    df_portion = st.slider("Select range of rows to display", 0, len(bl.df)-1, (0, len(bl.df)-1))
    st.write("Showing rows:", df_portion[0], "-", df_portion[1])

    portion_button = st.button("Show Head", type="primary", key="but1")
    if portion_button:
        df_portion = (0, 5)

    st.write(bl.df.iloc[df_portion[0]:df_portion[1] + 1])


# champion df
with col2:
    st.header("Champions Played", divider="orange")

    df_champ_portion = st.slider("Select range of rows to display",
                                 0, len(bl.df_champ)-1, (0, len(bl.df_champ)-1))
    st.write("Showing rows:", df_champ_portion[0], "-", df_champ_portion[1])

    champ_portion_button = st.button("Show Head", type="primary", key="but2")
    if champ_portion_button:
        df_champ_portion = (0, 5)

    st.write(bl.df_champ.iloc[df_champ_portion[0]:df_champ_portion[1] + 1])

