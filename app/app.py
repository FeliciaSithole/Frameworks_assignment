
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('../data/metadata.csv')

# Basic cleaning
df = df.dropna(subset=['publish_time', 'title'])
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df = df.dropna(subset=['publish_time'])
df['year'] = df['publish_time'].dt.year

# App title
st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers.")

# Year selection
year_range = st.slider("Select publication year range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Display sample data
st.subheader("Sample Papers")
st.dataframe(df_filtered[['title', 'authors', 'journal', 'year']].head(10))

# Publications per year
st.subheader("Publications by Year")
year_counts = df_filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=year_counts.index, y=year_counts.values, palette='viridis', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = df_filtered['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, palette='magma', ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
st.pyplot(fig2)
