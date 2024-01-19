import streamlit as st
import backend_league as bl

st.set_page_config(layout="wide", page_title="Home")

st.sidebar.success("Select a page above")

st.title("Data Analysis and Visualization (League of Legends)")
st.header("Overview", divider="orange")

col1, col2 = st.columns(2)

with col1:
    # general info
    st.subheader("Account info:")

    container = st.container(border=True)
    general_info = bl.data[-2][0].split("\n")
    for info in general_info:
        container.write(info)

with col2:
    prev_ranks = [season.split(" ")[0] for season in bl.data[-1]]
    selected_option = st.selectbox("Previous Ranks:", prev_ranks, None,
                                   placeholder="Choose a season")
    for elem in bl.data[-1]:
        if selected_option and elem.startswith(selected_option):
            st.info(elem.split(" ")[1])

st.divider()

mid_col1, mid_col2 = st.columns(2)

with mid_col1:
    st.image("winrate_plot.png")

with mid_col2:
    with st.expander("See the explanation for the chart:"):
        explanation = """
        The Chart on the left demonstrates win rate for the games played over time.
        Win rate which is above 50% is considered to be high and it is low for 
        other way around. On the chart, Green and red boxes indicate positive and negative 
        win rates respectively.
        """
        st.write(explanation)
        st.info("It can be observed that my current win rate is above 50.")

        button_wr = st.button("See current winrate")
        if button_wr:
            current_wr = bl.df['winrate'].iloc[0] * 100
            st.success(f"{current_wr}%")
            st.balloons()

st.divider()

bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.image("champ_plot.png")

with bottom_col2:
    with st.expander("See the explanation for the chart:"):
        explanation = """
        The chart on the left basically demonstrates play counts of each champion for
        all game modes. 
        """
        st.write(explanation)
        max_count = str(bl.df_champ["Played"].max())
        min_count = str(bl.df_champ["Played"].min())
        st.info("Maximum play count: " + max_count)
        st.info("Minimum play count: " + min_count)

st.divider()

st.subheader("Details about most played champion (Ranked):")

# details container
detail_container = st.container(border=True)

for elem in bl.data[:-2]:
    detail_container.write(elem[0])
    detail_container.info(elem[1])
    detail_container.divider()

