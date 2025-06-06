# Movie Data EDA - Professional Analysis with Insightful Storytelling & Streamlit Dashboard

# 📦 Import Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import streamlit as st

# 📊 Display Settings
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 📁 Load Data
df = pd.read_csv("movies.csv", sep=';', encoding='ISO-8859-1', on_bad_lines='skip')

# 🧹 Basic Cleaning
df.dropna(subset=['gross', 'company'], inplace=True)
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df['gross'] = pd.to_numeric(df['gross'], errors='coerce')
df.dropna(inplace=True)
df['year'] = df['year'].astype(int)
df['ROI'] = (df['gross'] - df['budget']) / df['budget']
df['release_month'] = pd.to_datetime(df['released'], errors='coerce').dt.month

# Streamlit App
st.title("🎬 Movie Data Exploratory Analysis Dashboard")
st.markdown("Explore trends, profits, and insights from 4000 movies.")

# Sidebar Filters
selected_genre = st.sidebar.multiselect("Select Genre(s)", df['genre'].unique(), default=df['genre'].unique())
selected_rating = st.sidebar.multiselect("Select Rating(s)", df['rating'].dropna().unique(), default=df['rating'].dropna().unique())
filtered_df = df[(df['genre'].isin(selected_genre)) & (df['rating'].isin(selected_rating))]

# 💹 Correlation Heatmap
st.subheader("🔗 Feature Correlation")
correlation_matrix = filtered_df[['budget', 'gross', 'score', 'votes', 'runtime', 'ROI']].corr()
fig, ax = plt.subplots()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)
st.markdown("**Insight:** Movies with higher budgets tend to earn more at the box office. " \
"However, this doesn't always mean they are more profitable. We also added a new column called ROI (Return on Investment)," \
" which shows how much profit a movie made compared to its cost. " \
"For example, if a movie had a budget of $10 million  and made $30 million, " \
"its ROI would be 2.0 — meaning it earned 200% of its cost back.")


# 📈 Budget vs Gross
st.subheader("💰 Budget vs Gross")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x='budget', y='gross', hue='rating', ax=ax)

st.pyplot(fig)
st.markdown("**Insight:** In general, movies with bigger budgets make more money, but there are also lower-budget movies that did really well. So, spending more doesn't always guarantee success.")

# 📊 Top Grossing Movies
st.subheader("🏆 Top 10 Grossing Movies")
top_grossing = filtered_df.sort_values(by='gross', ascending=False).head(10)
st.plotly_chart(px.bar(top_grossing, x='name', y='gross', color='company', title="Top 10 Highest Grossing Movies"))
st.markdown("**Insight:** These are the highest earning movies. As expected, most of them come from big production companies like Warner Bros. or Universal.")

# 🌟 Top Rated Movies (filtered by vote count)
st.subheader("🎖️ Top Rated Movies (Votes > 100K)")
top_rated = filtered_df[filtered_df['votes'] > 100000].sort_values(by='score', ascending=False).head(10)

fig,ax = plt.subplots()
sns.barplot(data=top_rated, x='score', y='name', palette='viridis',ax=ax)
st.pyplot(fig)
st.markdown("**Insight:** These are the top-rated movies on IMDb, based on user reviews. We included only those with more than 100,000 votes to make sure the ratings are reliable.")

# 🏢 Most Productive Companies
st.subheader("🏭 Most Movie-Producing Companies")
top_companies = filtered_df['company'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_companies.values, y=top_companies.index,ax=ax)
st.pyplot(fig)
st.markdown("**Insight:** These studios have produced the most number of movies in the dataset. Bigger studios usually release more films every year.")

# 📅 Movies Over Time
st.subheader("📆 Movie Releases Over Time")
fig, ax = plt.subplots()
sns.histplot(filtered_df['year'], bins=30, kde=True,ax=ax)
st.pyplot(fig)
st.markdown("**Insight:** The number of movies released has grown over the years, with a big rise in the 2000s and 2010s.")

# 📉 ROI Distribution
st.subheader("📊 ROI Distribution")
fig, ax = plt.subplots()
sns.boxplot(data=filtered_df, x='rating', y='ROI',ax=ax)
st.pyplot(fig)
st.markdown("**Insight:** Return on Investment (ROI) shows how profitable a movie was based on how much it earned compared to its budget. Some movies with lower ratings still made a lot of money, which means they were financially successful even if not critically praised.")

# 🧠 Insightful Summary
st.subheader("🧠 Final Insights")
st.markdown("""
- 💰 Movies with bigger budgets usually earn more, but not all high-budget films are profitable.
- 📈 ROI (Return on Investment) helps us understand how much money a movie made **compared to its cost**. It's a great way to find low-budget movies that made huge profits.
- 🌟 Top-rated movies often have a lot of votes, showing they are popular and respected.
- 🏢 Studios like Warner Bros. and Universal lead in terms of output and earnings.
- 🗓️ Movie production has increased a lot since 2000.
- 🎯 Some low-rated movies still made great profits — meaning popularity and profitability don’t always go hand in hand.
""")
