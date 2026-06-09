from flask import Flask, render_template, url_for, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split


app = Flask(__name__)

# ── Train model once at startup ──────────────────────────────────────
df = pd.read_csv("spam_data.csv", encoding="latin-1")
df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)

# Features and Labels
df['label'] = df['type'].map({'ham': 0, 'spam': 1})
X = df['message']
y = df['label']

# Extract features with CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

# Naive Bayes Classifier
clf = MultinomialNB()
clf.fit(X_train, y_train)
print(f"Model accuracy: {clf.score(X_test, y_test):.4f}")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']
    data = [message]
    vect = cv.transform(data).toarray()
    my_prediction = clf.predict(vect)
    return render_template('result.html', prediction=my_prediction[0])


if __name__ == '__main__':
    app.run(debug=True)