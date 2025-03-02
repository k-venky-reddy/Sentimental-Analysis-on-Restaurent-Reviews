import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/Sentiment Analysis of Restarent reviews/Restaurant_Reviews (1).tsv', sep='\t')

print(df)

df.head()

df.describe()

df.info()

df.groupby('Liked').describe()

df['Length'] = df['Review'].apply(len)
df.head()

df.Length.describe()

df_149 =df[df['Length'] == 149]['Review']
for message in df_149:
    print(message)

# Data Visualizations
from wordcloud import WordCloud
all_messages = ' '.join(df['Review'])
wordCloud = WordCloud(width=500, height=300, random_state=20, max_font_size=100).generate(all_messages)
plt.imshow(wordCloud, interpolation='bilinear')
plt.axis('off')
plt.show()

sns.set_style('darkgrid')
sns.countplot(x='Liked', data=df)
plt.title('Count of Reviews by Liked Status')
plt.xlabel('Liked')
plt.ylabel('Count')
plt.show()

g = sns.FacetGrid(df, col='Liked')
g.map(plt.hist, 'Length');

df.hist(column='Length', by='Liked', bins=50,figsize=(14,6));

# Data Preprocessing
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X =df['Review'].str.lower()
y = df['Liked']
X = cv.fit_transform(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state=101)

# Naives Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()

nb.fit(X_train,y_train)

predictions = nb.predict(X_test)

from sklearn.metrics import confusion_matrix,classification_report

print(confusion_matrix(y_test,predictions))

print(classification_report(y_test,predictions))

from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('bow', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('classifier', MultinomialNB()),])

X = df['Review']
y = df['Liked']
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state=101)

pipeline.fit(X_train,y_train)

predictions = pipeline.predict(X_test)

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))

#logistic regression

from sklearn import linear_model

logr=linear_model.LogisticRegression()

X = cv.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state=101)

logr.fit(X_train,y_train)

logpredictions = logr.predict(X_test)

print(confusion_matrix(y_test,logpredictions))

print(classification_report(y_test,logpredictions))
