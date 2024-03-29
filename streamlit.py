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
        st.header('Highlight wines to increase sales.')
        st.text('''The wines with the highest average ratings and the most ratings tend to be the most popular wines, 
use this phenomenon to your advantage by selecting the top wines to boost sales!''')
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
        footer = """
<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: purple;
color: white;
text-align: center;
padding: 10px;
}
</style>
<div class="footer">
    Developed with ❤ by HazemEldabaa
</div>
"""
        st.markdown(footer, unsafe_allow_html=True)

    def page_two():
        st.header('Countries to target for a limited marketing budget.')
        st.text('''The countries with the most users are the best to target for a limited marketing budget. The more 
users, the more potential customers.''')
        limit = st.number_input("Number of countries to target", min_value=1, value=1)
        query = f"""SELECT name AS country_name, users_count, code 
    FROM countries
    ORDER BY users_count DESC
    LIMIT {limit}
    """
        df = pd.read_sql_query(query, engine)
        df.set_index('code', inplace=True)
        st.dataframe(df)

    # Navigation
        if st.button('Previous'):
            st.session_state.page = 'page_one'
            st.rerun()
        if st.button('Next'):
            st.session_state.page = 'page_three'
            st.rerun()
        footer = """
<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: purple;
color: white;
text-align: center;
padding: 10px;
}
</style>
<div class="footer">
    Developed with ❤ by HazemEldabaa
</div>
"""
        st.markdown(footer, unsafe_allow_html=True)

    def page_three():
        col1, col2, col3 = st.columns([9, 2, 9])
        with col1:
            st.header('Award the overall best wineries!')
            st.text('''The wineries with the highest total rank 
(Sum of all their ranks in previous awards) 
are the best wineries. Award them to increase 
their reputation and sales!''')
            limit = st.number_input("Number of wineries to award", min_value=1, value=3)
            query = f"""
                        SELECT
                        wynnery as winery_name,
                        SUM(rank) as total_rank,
                        wines.winery_id

                        FROM vintage_toplists_rankings
                        JOIN temp ON vintage_toplists_rankings.vintage_id = temp.id_vintage_id
                        JOIN vintages on vintage_id = vintages.id
                        JOIN wines on vintages.wine_id = wines.id
                        GROUP BY wynnery
                        ORDER BY total_rank DESC
                        LIMIT {limit}
                        """
            df = pd.read_sql_query(query, engine)
            df.set_index('winery_id', inplace=True)
            st.dataframe(df)
        with col2:
            st.write("")
        with col3:
            st.header('Award the most promising wineries!')
            st.text('''Promising wineries are the ones with 
the highest rank difference (Current 
rank - Previous rank). Award them to 
increase their awareness and boost 
their drive to excel!''')
            limit1 = st.number_input("Number of up and coming wineries to award", min_value=1, value=3)

            query1 = f"""
                        SELECT
                        wynnery as winery_name,
                        rank - previous_rank AS rank_difference,
                        wines.winery_id
                        FROM vintage_toplists_rankings
                        JOIN temp ON vintage_toplists_rankings.vintage_id = temp.id_vintage_id
                        JOIN vintages on vintage_id = vintages.id
                        JOIN wines on vintages.wine_id = wines.id
                        GROUP BY wynnery
                        ORDER BY rank_difference DESC
                        LIMIT {limit1}
                        """
            df1 = pd.read_sql_query(query1, engine)
            df1.set_index('winery_id', inplace=True)

            st.dataframe(df1)

        if st.button('Previous'):
            st.session_state.page = 'page_two'
            st.rerun()
        if st.button('Next'):
            st.session_state.page = 'page_four'
            st.rerun()
        footer = """
<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: purple;
color: white;
text-align: center;
padding: 10px;
}
</style>
<div class="footer">
    Developed with ❤ by HazemEldabaa
</div>
"""
        st.markdown(footer, unsafe_allow_html=True)
    def page_four():
        st.header('Identify wines of Vibrant Essence.')
        st.text('''Vibrant wines have all the following keywords in their flavor profile: (coffee, toast, green apple,
cream, citrus)''')
        limit = st.number_input("Minimum number of user confirmations", min_value=1, value=10)
        query = f"""
        SELECT
        w.id AS wine_id,
        w.name AS wine_name,
        GROUP_CONCAT(k.name, ', ') AS keyword_names,
        group_name,
        kw.count as user_confirmations  
    FROM wines w
    JOIN keywords_wine kw ON w.id = kw.wine_id
    JOIN keywords k ON kw.keyword_id = k.id
    WHERE k.name IN ('coffee', 'toast', 'green apple', 'cream', 'citrus')
    AND kw.count >= {limit}
    GROUP BY w.id, w.name
    HAVING COUNT(DISTINCT k.name) >= 5;
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
        footer = """
<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: purple;
color: white;
text-align: center;
padding: 10px;
}
</style>
<div class="footer">
    Developed with ❤ by HazemEldabaa
</div>
"""
        st.markdown(footer, unsafe_allow_html=True)
    def page_five():
        col1, col2, col3 = st.columns([9, 2, 9])
        with col1: 
            st.header('Popular grapes globally.')
            st.text('''The grapes that are used in the most 
countries are the most common grapes. Use 
this information to target the most popular 
grapes for your marketing campaigns.''')
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
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            if st.button('Previous'):
                st.session_state.page = 'page_four'
                st.rerun()
            if st.button('Next'):
                st.session_state.page = 'page_six'
                st.rerun()
        with col2:
            st.write("")
        with col3:
            st.header('Best wines per grape.')
            st.text('''The wines with the highest ratings for  
each grape are the best wines. Use this 
information to target the best wines 
for your marketing campaigns.''')
            limit1 = st.number_input("Number of wines", min_value=1, value=5, key='wines_limit')
            csv_file_path = 'wine_data_missing_data.csv'
            csv_data = pd.read_csv(csv_file_path)
            csv_data.to_sql('temp', engine, if_exists='replace', index=False, method='multi')

            if not df.empty:
                grapes = df['grape_name'].tolist()
                for grape in grapes:
                    st.subheader(f"Top {limit1} wines for {grape}")
                    query1 = f"""
                    SELECT
                    wine.name AS wine_name,
                    wine.ratings_average,
                    wine.id,
                    t.grappe as grape_name
                    FROM
                        wines wine
                    JOIN temp t ON wine.id = t.wine_id
                    WHERE
                        t.grappe IN ('{grape}')
                    ORDER BY
                        wine.ratings_average DESC
                    LIMIT {limit1};
                    """
                    df1 = pd.read_sql_query(query1, engine)
                    df1.set_index('id', inplace=True)
                    df1 = df1[['wine_name', 'ratings_average', 'grape_name']]
                    st.dataframe(df1)
                    
            else:
                st.write("No grapes found.")
            footer = """
<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: purple;
color: white;
text-align: center;
padding: 10px;
}
</style>
<div class="footer">
    Developed with ❤ by HazemEldabaa
</div>
"""
        st.markdown(footer, unsafe_allow_html=True)
    def page_six():
        st.header('Average wine rating for each country')
        st.text('''The average wine rating for each country is a good indicator of the quality of wines produced in 
that country.''')
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
        plt.bar(df['country_name'], df['avg_rating'], color='magenta')
        plt.ylim(4., 4.6)
        plt.xlabel('Country Name')
        plt.ylabel('Average Wine Rating')
        plt.title('Average Wine Rating by Country')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

        st.header('Average vintage wine rating for each country')
        st.text('''The average vintage wine rating for each country is a good indicator of the quality of 
vintage wines produced in that country.''')
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
        plt.bar(df1['country_name'], df1['avg_rating'], color='magenta')
        plt.xlabel('Country Name')
        plt.ylabel('Average Wine Rating')
        plt.title('Average Wine Rating by Country')
        plt.xticks(rotation=45, ha='right')  # Rotate country names for better readability
        plt.tight_layout()  # Adjust layout to fit country names
        st.pyplot(fig1)
        if st.button('Previous'):
            st.session_state.page = 'page_five'
            st.rerun()
        footer = """
<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: purple;
color: white;
text-align: center;
padding: 10px;
}
</style>
<div class="footer">
    Developed with ❤ by HazemEldabaa
</div>
"""
        st.markdown(footer, unsafe_allow_html=True)
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

