import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

def train_and_save():
    # Load your dataset
    df = pd.read_csv('job_applicant_dataset.csv')
    
    # We learn the relationship between Resume + JD and the 'Best Match' label
    df['combined_text'] = df['Resume'].fillna('') + " " + df['Job Description'].fillna('')
    
    # Initialize Vectorizer
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    X = tfidf.fit_transform(df['combined_text'])
    y = df['Best Match']
    
    # Train Logistic Regression (The ML Model)
    model = LogisticRegression()
    model.fit(X, y)
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
        
    # Save the artifacts
    with open('models/ats_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/vectorizer.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
        
    print("Success: models/ats_model.pkl and models/vectorizer.pkl created.")

if __name__ == "__main__":
    train_and_save()