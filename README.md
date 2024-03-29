# 🍷Vivino-Market-Analysis

Are you a wine enthusiast? Or a vintner looking to optimize his catalog and maximize profits? Welcome to the Vivino Market Analysis Repo, where you can dive deep into the complexities of the wine industry to bring you insights that matter. This repository is a treasure trove of data-driven analyses, market trends, consumer preferences, and strategic recommendations designed to cater to sommeliers, wine marketers, producers, and aficionados alike.

## 🚀Features

- **Vineyard Verdicts** - Ratings for various wines
- **Winery Watchlist** - Rankings for top and promising wineries
- **Flavor Fables** - Discover various flavor profiles
- **Grape Gallery** - Find the most popular grapes
- **Country Chronicles** Statistics and plots sorted by country

# 🏁Getting Started

## 📋Prerequisites
- Python 3.x
## 🛠️Installation

**Clone the Repository:**

```bash
git clone https://github.com/HazemEldabaa/wine-market-analysis.git
cd wine-market-analysis
```
**Create a Virtual Environment (Optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: \venv\Scripts\activate
```
**Install Dependencies:**

```bash
pip install -r requirements.txt
```
## 👩‍💻Usage
To run locally:

```bash
python streamlit run streamlit.py
```
To deploy online simply fork the repository on GitHub, then link your repo on the [Streamlit Community Cloud](https://streamlit.io/cloud) and deploy!

##  📁Project Structure
- queries.sql: Contains the main queries used for navigating the database.
- test.ipynb: Test notebook to experiment with plots and running queries through Python.
- requirements.txt: List of Python dependencies.
- vivino.db: The main Vivino scraped database
- wine_data_missing_data.csv: Additional scraped content from Vivino to compensate for missing and inconsistent data from the main database.
- streamlit.py: Final product, navigatable and dynamic analysis of the data on a front-end
## 📷Screenshots
### Streamlit Interface:
![Streamlit Interface](https://i.ibb.co/KVSkX9c/image.png)
### Relational DB Schema:
![Schema](https://i.ibb.co/v1VKQLC/vivino-db-diagram-horizontal.png)
