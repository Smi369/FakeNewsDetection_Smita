import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Initialize PorterStemmer and stopwords
ps = PorterStemmer()
stop_words = stopwords.words('english')

# Function to preprocess text data
def preprocess_text(text):
    # Remove non-alphabetic characters and convert to lowercase
    text = re.sub('[^a-zA-Z]', ' ', text).lower()
    # Tokenize the text into words
    words = text.split()
    # Remove stopwords and perform stemming
    words = [ps.stem(word) for word in words if word not in stop_words]
    # Join the stemmed words back into a single string
    processed_text = ' '.join(words)
    return processed_text

# Reading the data
df = pd.read_csv('train.csv')

# Dropping null values
df = df.dropna()

# Preprocessing the text data
df['text'] = df['text'].apply(preprocess_text)

# Splitting the dataframe
X_train, X_test, Y_train, Y_test = train_test_split(df['text'], df['label'], test_size=0.30, random_state=40)

# Vectorizing the text data using TF-IDF
tfidf_vect = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = tfidf_vect.fit_transform(X_train)
tfidf_test = tfidf_vect.transform(X_test)

# Training Naive Bayes model
nb_model = MultinomialNB()
nb_model.fit(tfidf_train, Y_train)

# Training Random Forest model
rf_model = RandomForestClassifier()
rf_model.fit(tfidf_train, Y_train)

# Training K-Nearest Neighbors model
knn_model = KNeighborsClassifier()
knn_model.fit(tfidf_train, Y_train)

# Evaluating models
nb_accuracy = nb_model.score(tfidf_test, Y_test)
rf_accuracy = rf_model.score(tfidf_test, Y_test)
knn_accuracy = knn_model.score(tfidf_test, Y_test)

# Saving the trained models
joblib.dump(nb_model, 'nb_model.pkl')
joblib.dump(rf_model, 'rf_model.pkl')
joblib.dump(knn_model, 'knn_model.pkl')
joblib.dump(tfidf_vect, 'tfidf_vect.pkl')

print("Models trained and saved successfully.")
