import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

keywords = {
      'Fast Food' : ['McDonalds', 'KFC', 'Burger', 'Vosime', 'pizza', 'mianchi', 'kebab', 'pizzzza'],
      'Groceries' : ['ALBERT', 'TESCO', 'LIDL', 'KAUFLAND', 'HRUSKA', 'GLOBUS', 'TERRA VITAE', 'Potraviny', 'Food'],
      'Entertainment' : ['Playstation', 'Nintendo', 'Microsoft', 'Spotify', 'Netflix', 'Cinema', 'Steam', 'kino', 'zahrada'],
      'Income' : ['COMVERGA'],
      'Subscription' : ['OPENAI', 'SUBSCR', 'MONTHLY', 'PLEXINCPASS', 'KiwiCo', 'VPN', 'Google Storage', 'hostinger', 'morgen', 'Netusers'],
      'Coffee Shop' : ['KAFE', 'KAVA', 'Coffee', 'Coffee House', 'Starbucks', 'CAFE', 'smoke', 'hookah', 'prazirna', 'Espresso', 'Dok'],
      'Savings' : ['Stavebko', 'Fond', 'Spořící', 'Penzijko'],
      'Insurance' : ['UPLUS'],
      'Hobby' : ['aurapol', 'Dobrovsky', 'knihy', 'books', 'keyboards', 'computers', 'keygem'],
      'Sport' : ['Sportisimo', 'Queen Club', 'Sport', 'Gym'],
      'Shopping' : ['Zmrzlina', 'GECO', 'PRIM', 'Metalshop', 'Elektro', 'Alza', 'Zoo', 'Aktin', 'Dracik', 'suvenyry', 'Google Play Apps', 'Ebay'],
      'Restaurant/Bars' : ['Bistro', 'Restaurant', 'Restaurace', 'Hostinec', 'Pub', 'Bar', 'Krcma', 'Hospoda', 'Laborka', 'Romana'],
      'Auto/Moto/Transport' : ['Moto', 'Auto', 'MOL', 'Rasin', 'CARS', 'EDALNICE', 'Shell', 'parking', 'dpmp', 'trains', 'mhd'],
      'ATM' : ['bankomat', 'výběr'],
      'Rent&Other' : ['JIŘINA', 'Gabriel', 'Jiří', 'Izabela', 'Daniel', 'Revolut'],
      'Fees' : ['poplatek', 'fee', 'pokuta'],
      'Health&Beauty' : ['Lekarna', 'DM', 'Teta', 'Clinic']
}

def categorize_transaction(description):
    description_lower = description.lower()
    for category, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword.lower() in description_lower:
                return category
    return 'Uncategorized'

class ExpenseCategorizer:
      def __init__(self, df, model_name="xlm-roberta-base"):
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.classifier = LogisticRegression(max_iter=100)
            self.scaler = StandardScaler()
            df['Concatenated_Details'] = df[['Transaction detail 1', 'Transaction detail 2', 'Transaction detail 3']].fillna('').agg(' '.join, axis=1)
            df['Category'] = df['Concatenated_Details'].apply(lambda x: categorize_transaction(x) if x.strip() != '' else 'Uncategorized')
            self.df = df
            self.labeled_data = df[df['Category'] != 'Uncategorized']
            self.unlabeled_data = df[df['Category'] == 'Uncategorized']
            
      def embed_sentence(self, sentence):
            inputs = self.tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
            outputs = self.model(**inputs)
            # Use the mean of the token embeddings as the sentence embedding
            sentence_embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy().flatten()
            return sentence_embedding
      
      def prepare_data(self):
            df = self.df.dropna(subset=['Concatenated_Details'])
            X = np.array([self.embed_sentence(desc) for desc in df['Concatenated_Details']])
            y = df['Category']
            X_scaled = self.scaler.fit_transform(X)
            return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
      
      def train_model(self, X_train, y_train):
            self.classifier.fit(X_train, y_train)
            
      def evaluate_model(self, X_test, y_test):
            y_pred = self.classifier.predict(X_test)
            print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
            print(classification_report(y_test, y_pred, zero_division=0))
      
      def save_model(self, model_path, vectorizer_path):
            joblib.dump(self.classifier, model_path)
            joblib.dump(self.scaler, 'scaler.pkl')
            joblib.dump(self.tokenizer, vectorizer_path)
            
      def load_model(self, model_path, vectorizer_path):
            self.classifier = joblib.load(model_path)
            self.scaler = joblib.load('scaler.pkl')
            self.tokenizer = joblib.load(vectorizer_path)
            
      def categorize(self, description):
            description_vec = self.embed_sentence(description).reshape(1, -1)
            description_vec_scaled = self.scaler.transform(description_vec)
            category = self.classifier.predict(description_vec)[0]
            return category