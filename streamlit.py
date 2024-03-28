import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import base64
import requests
st.set_page_config(layout="wide")

st.title('Vivino Market Analysis')
# Database connection
engine = create_engine('sqlite:///vivino.db')
col1, col2, col3 = st.columns([2,7,2])
def get_image_base64_from_url(url):
    response = requests.get(url)
    # Make sure the request was successful
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        return None

def add_bg_from_base64(image_base64):
    if image_base64 is not None:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{image_base64}");
                background-size: cover;
            }}
            </style>
            """, unsafe_allow_html=True)
    else:
        st.error("Failed to load background image.")

image_url = 'https://s1.1zoom.me/b5050/551/Grapes_Wine_Black_background_Stemware_512143_1920x1080.jpg'
image_base64 = get_image_base64_from_url(image_url)
add_bg_from_base64(image_base64)

with col1:
    st.text('')
    
    
    
    
    
    
    
    
    
    
with col2:

    def page_one():
        st.header('Highlight wines to increase sales')
        limit = st.number_input("Number of wines to highlight", min_value=1, value=10)
        query = f"""
        SELECT * 
        FROM wines
        ORDER BY ratings_average DESC, ratings_count DESC
        LIMIT {limit}
        """
        df = pd.read_sql_query(query, engine)
        df.set_index('id', inplace=True)
        df = df[['name', 'ratings_average', 'ratings_count','is_natural']]
        st.dataframe(df)

        if st.button('Next'):
            st.session_state.page = 'page_two'
            st.rerun()

    def page_two():
        st.header('Which country to target for a limited marketing budget?')

        limit = st.number_input("Number of countries to target", min_value=1, value=1)
        query = f"""SELECT * 
    FROM countries
    ORDER BY users_count DESC
    LIMIT {limit}
    """
        df = pd.read_sql_query(query, engine)
        st.dataframe(df)

    # Navigation
        if st.button('Previous'):
            st.session_state.page = 'page_one'
            st.rerun()
        if st.button('Next'):
            st.session_state.page = 'page_three'
            st.rerun()

    def page_three():
        st.header('Give awards to the best wineries')
        limit = st.number_input("Number of wineries to award", min_value=1, value=3)
        query = f"""
        SELECT
        wines.name AS wine_name,
        wines.winery_id,
        wines.ratings_average,
        vintages.wine_id,
        vintage_toplists_rankings.vintage_id,
        toplists.name AS toplist_name,
        COUNT(winery_id) AS winery_count,
        ROUND(AVG(vintage_toplists_rankings.rank), 2) AS avg_rank
    FROM wines
    JOIN vintages ON wines.id = vintages.wine_id
    JOIN vintage_toplists_rankings ON vintages.id = vintage_toplists_rankings.vintage_id
    JOIN toplists ON vintage_toplists_rankings.top_list_id = toplists.id
    GROUP BY wines.winery_id
    ORDER BY avg_rank asc, winery_count desc, wines.ratings_average desc
    LIMIT {limit}
        """
        df = pd.read_sql_query(query, engine)
        df.set_index('winery_id', inplace=True)
        st.dataframe(df)
        if st.button('Previous'):
            st.session_state.page = 'page_two'
            st.rerun()
        if st.button('Next'):
            st.session_state.page = 'page_four'
            st.rerun()

    def page_four():
        st.header('Identify wines of Vibrant Essence')
        st.text('Vibrant wines have all the following keywords: coffee, toast, green apple, cream, citrus')
        limit = st.number_input("Minimum number of user confirmations", min_value=1, value=10)
        query = f"""
        SELECT
        w.id AS wine_id,
        w.name AS wine_name,
        kw.count AS keyword_count,
        k.name AS keyword_name,
        group_name
    FROM wines w
    JOIN keywords_wine kw ON w.id = kw.wine_id
    JOIN keywords k ON kw.keyword_id = k.id
    WHERE k.name IN ('coffee', 'toast', 'green apple', 'cream', 'citrus')
    AND kw.count >= {limit}
    GROUP BY w.id, w.name
    HAVING COUNT(DISTINCT keyword_name) >= 5;
        """
        df = pd.read_sql_query(query, engine)
        df.set_index('wine_id', inplace=True)
        st.dataframe(df)
        if st.button('Previous'):
            st.session_state.page = 'page_three'
            st.rerun()
        if st.button('Next'):
            st.session_state.page = 'page_five'
            st.rerun()

    def page_five():
        col1, col2, col3 = st.columns([9, 2, 9])
        with col1: 
            st.header('Find the most common grapes all over the world')
            limit = st.number_input("Number of grapes", min_value=1, value=3)
            query = f"""
            SELECT
            gp.grape_id,
            g.name AS grape_name,
            COUNT(gp.country_code) AS country_count
            FROM most_used_grapes_per_country gp
            JOIN grapes g ON gp.grape_id = g.id
            GROUP BY gp.grape_id
            ORDER BY country_count DESC
            LIMIT {limit};  
            """
            df = pd.read_sql_query(query, engine)
            df.set_index('grape_id', inplace=True)
            st.dataframe(df)
            if st.button('Previous'):
                st.session_state.page = 'page_four'
                st.rerun()
            if st.button('Next'):
                st.session_state.page = 'page_six'
                st.rerun()
        with col2:
            st.write("")
        with col3:
            st.header('For each grape, give us the best rated wines.')
            limit1 = st.number_input("Number of wines", min_value=1, value=5, key='wines_limit')

            if not df.empty:
                grapes = df['grape_name'].tolist()
                for grape in grapes:
                    st.subheader(f"Top {limit1} wines for {grape}")
                    query1 = f"""
                    SELECT
                    wine.name AS wine_name,
                    wine.ratings_average,
                    wine.id
                    FROM
                        wines wine
                    WHERE
                        wine.name LIKE '%{grape}%'
                    ORDER BY
                        wine.ratings_average DESC
                    LIMIT {limit1};
                    """
                    df1 = pd.read_sql_query(query1, engine)
                    df1.set_index('id', inplace=True)
                    df1 = df1[['wine_name', 'ratings_average']]
                    st.dataframe(df1)
                    
            else:
                st.write("No grapes found.")
        
    def page_six():
        st.header('Average wine rating for each country')
        query = """
        SELECT
        c.name AS country_name,
        AVG(w.ratings_average) AS avg_rating
        FROM countries c
        JOIN regions r ON c.code = r.country_code
        JOIN wines w ON r.id = w.region_id
        GROUP BY c.name
        ORDER BY avg_rating DESC;
        """

        df = pd.read_sql_query(query, engine)

        fig = plt.figure(figsize=(10, 6))
        plt.bar(df['country_name'], df['avg_rating'], color='skyblue')
        plt.ylim(4., 4.6)
        plt.xlabel('Country Name')
        plt.ylabel('Average Wine Rating')
        plt.title('Average Wine Rating by Country')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

        st.header('Average vintage wine rating for each country')
        query1 = """
        SELECT
        c.name AS country_name,
        AVG(v.ratings_average) AS avg_rating
        FROM countries c
        JOIN regions r ON c.code = r.country_code
        JOIN wines w ON r.id = w.region_id
        JOIN vintages v ON w.id = v.wine_id
        GROUP BY c.name
        ORDER BY avg_rating DESC;
        """

        df1 = pd.read_sql_query(query1, engine)

        # Step 3: Plot the results using Matplotlib
        fig1 = plt.figure(figsize=(10, 6))
        plt.bar(df1['country_name'], df1['avg_rating'], color='skyblue')
        plt.xlabel('Country Name')
        plt.ylabel('Average Wine Rating')
        plt.title('Average Wine Rating by Country')
        plt.xticks(rotation=45, ha='right')  # Rotate country names for better readability
        plt.tight_layout()  # Adjust layout to fit country names
        st.pyplot(fig1)
        if st.button('Previous'):
            st.session_state.page = 'page_five'
            st.rerun()
            # Render the appropriate page
    if 'page' in st.session_state:
        if st.session_state.page == 'page_one':
            page_one()
        elif st.session_state.page == 'page_two':
            page_two()
        elif st.session_state.page == 'page_three':
            page_three()
        elif st.session_state.page == 'page_four':
            page_four()
        elif st.session_state.page == 'page_five':
            page_five()
        elif st.session_state.page == 'page_six':
            page_six()
    else:
        # Default page
        page_one()

with col3:
    st.text('')

