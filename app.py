from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import os 

app=Flask(__name__)
df=pd.read_csv('netflix_data.csv')
#create dictionary to store plots
if not os.path.exists('static'):
    os.makedirs('static') 
    

# Visualization 1: Top 10 Genres
def plot_genres():
    plt.figure(figsize=(10,6))
    top_genres = df['genre'].value_counts().head(10)
    sns.barplot(x=top_genres.values, y=top_genres.index, palette='viridis')
    plt.title("Top 10 Genres on Netflix")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig('static/genre_plot.png')
    plt.close()

# Visualization 2: Movies vs TV Shows Over Years
def plot_trend():
    content_trend = df.groupby(['release_year', 'type']).size().reset_index(name='count')
    plt.figure(figsize=(10,6))
    sns.lineplot(data=content_trend, x='release_year', y='count', hue='type', marker='o')
    plt.title("Movies vs TV Shows Over the Years")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Releases")
    plt.tight_layout()
    plt.savefig('static/trend_plot.png')
    plt.close()

# Visualization 3: Top 10 Countries
def plot_countries():
    top_countries = df['country'].value_counts().head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette='magma')
    plt.title("Top 10 Countries with Most Netflix Content")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig('static/country_plot.png')
    plt.close()

# Content added per year
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='year_added', order=df['year_added'].value_counts().sort_index().index)
plt.title("Content Added to Netflix per Year")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("static/yearly_content_plot.png")
plt.close()

# Top 10 directors
top_directors = df['director'].dropna().str.split(', ').explode().value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_directors.values, y=top_directors.index, palette='mako')
plt.title("Top 10 Directors on Netflix")
plt.xlabel("Number of Titles")
plt.tight_layout()
plt.savefig("static/top_directors_plot.png")
plt.close()



@app.route('/')
def index():
    plot_genres()
    plot_trend()
    plot_countries()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)