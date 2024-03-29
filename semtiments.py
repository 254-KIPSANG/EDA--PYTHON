# -*- coding: utf-8 -*-


!pip install -q google-play-scraper
import pandas as pd
from google_play_scraper import reviews
from google_play_scraper import Sort

## top 20 apps
apps = {
    "Zenka": "com.zenkafinance.microloans",
    "cashpesa": "cash.pesa.loan.kenya",
    "meta": "com.metaloan",
}

SORT = Sort.NEWEST
N_REVIEWS = 10000
reviews_dict =  {k : {} for k in apps}

## Scraping reviews
for app in apps.keys():
    reviews_dict[app], _  = reviews(
         apps[app],
         lang='all',
         country='ke',
         sort= SORT,
         count=N_REVIEWS,
         filter_score_with=None
     )
    assert len(reviews_dict[app]) == N_REVIEWS

## saving reviews
df = pd.DataFrame()
for app in apps.keys():
    SAVE_DIR = app  + ".csv"
    temp_df = pd.DataFrame(
        reviews_dict[app],
        columns = ["reviewId", "content", "score", "reviewCreatedVersion", "at", "repliedAt", "replyContent", "user", "appVersion"]
    )
    temp_df.to_csv(SAVE_DIR, index = False)
    temp_df["app"] = app
    df = pd.concat((df ,temp_df))
df.to_csv("all_combined.csv", index = False)
print("DONE :) ")
df.head()

print(data.columns)

# Check for missing values
missing_values = data['content'].isnull().sum()
print("Number of missing values in 'content' column:", missing_values)

# Drop rows with missing values
data = data.dropna(subset=['content'])

# Convert all text to lowercase
data['content'] = data['content'].str.lower()

# Remove stopwords
stop_words = set(stopwords.words('english'))
data['content'] = data['content'].apply(lambda x: ' '.join(word for word in x.split() if word not in stop_words))

# Lemmatize each word
data['content'] = data['content'].apply(lambda x: ' '.join(Word(word).lemmatize() for word in x.split()))

# Remove non-ASCII characters
data['content'] = data['content'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))

# Display the preprocessed DataFrame
print(data.head())

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Concatenate all preprocessed text data into a single string
text = ' '.join(data['content'])

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Preprocessed Text')
plt.axis('off')
plt.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Define thresholds for positive, neutral, and negative scores
positive_threshold = 4
negative_threshold = 2

# Categorize words based on review scores
positive_text = ' '.join(data[data['score'] >= positive_threshold]['content'])
neutral_text = ' '.join(data[(data['score'] > negative_threshold) & (data['score'] < positive_threshold)]['content'])
negative_text = ' '.join(data[data['score'] <= negative_threshold]['content'])

# Generate word clouds for each sentiment category
positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_text)
neutral_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(neutral_text)
negative_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_text)

# Display the word clouds for each sentiment category
plt.figure(figsize=(15, 10))

plt.subplot(1, 3, 1)
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.title('Positive Review Word Cloud')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(neutral_wordcloud, interpolation='bilinear')
plt.title('Neutral Review Word Cloud')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.title('Negative Review ')
plt.axis('off')

plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Define thresholds for positive, neutral, and negative scores
positive_threshold = 4
negative_threshold = 2

# Categorize sentiments based on review scores
data['sentiment'] = pd.cut(data['score'], bins=[0, negative_threshold, positive_threshold, 5], labels=['Negative', 'Neutral', 'Positive'])

# Group the data by 'app' and 'sentiment', and count the occurrences
sentiment_counts = data.groupby(['app', 'sentiment']).size().unstack(fill_value=0)

# Plot the sentiment distribution for each app
plt.figure(figsize=(12, 8))
sentiment_counts.plot(kind='bar', stacked=True)
plt.title('Sentiment Distribution for Each App')
plt.xlabel('App')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Sentiment')
plt.tight_layout()
plt.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Categorize words based on sentiment
positive_text = ' '.join(data[data['sentiment'] == 'Positive']['content'])
neutral_text = ' '.join(data[data['sentiment'] == 'Neutral']['content'])
negative_text = ' '.join(data[data['sentiment'] == 'Negative']['content'])

# Generate word clouds for each sentiment category
positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_text)
neutral_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(neutral_text)
negative_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_text)

# Display the word clouds for each sentiment category
plt.figure(figsize=(15, 10))

plt.subplot(1, 3, 1)
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.title('Positive Review Word Cloud')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(neutral_wordcloud, interpolation='bilinear')
plt.title('Neutral Review Word Cloud')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.title('Negative Review Word Cloud')
plt.axis('off')

plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Plotting sentiment distribution
plt.figure(figsize=(8, 6))
sns.countplot(x='sentiment', data=data)
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer

# Calculate TF-IDF scores
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(data['content'])

# Visualize TF-IDF scores for top N terms
import pandas as pd
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
tfidf_means = tfidf_df.mean().sort_values(ascending=False)[:10]
tfidf_means.plot(kind='barh')
plt.title('Top 10 Terms by TF-IDF Score')
plt.xlabel('TF-IDF Score')
plt.ylabel('Term')
plt.show()
