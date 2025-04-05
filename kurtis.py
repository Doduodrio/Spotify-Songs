import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r'C:\Users\kurti\Downloads\Spotify-Songs\ignore\dataset.csv', encoding='utf-8')

# scatter plot of song tempo and popularity
'''
# data = data[data['tempo'] > 0]
# plt.scatter(data['tempo'], data['popularity'], alpha=0.5)
# plt.xlabel('Tempo')
# plt.ylabel('Popularity')
# plt.show()
'''

# bar graph of track genres and average popularity
'''
average_popularity = data.groupby('track_genre')['popularity'].mean()

plt.figure(figsize=(18, 6))
average_popularity.sort_values().plot(kind='bar', color='skyblue')
plt.title('Average Popularity of Songs by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Popularity')
plt.xticks(rotation=90)  
plt.tight_layout()
plt.show()
'''