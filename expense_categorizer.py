import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import gensim.downloader as api

keywords = {
      'Fast Food' : ['McDonalds', 'KFC', 'Burger', 'Vosime', 'pizza', 'mianchi', 'kebab'],
      'Groceries' : ['ALBERT', 'TESCO', 'LIDL', 'KAUFLAND', 'HRUSKA', 'GLOBUS', 'TERRA VITAE', 'Potraviny', 'Food'],
      'Entertainment' : ['Playstation', 'Nintendo', 'Microsoft', 'Spotify', 'Netflix', 'Cinema', 'Steam', 'kino', 'zahrada'],
      'Income' : ['COMVERGA'],
      'Subscription' : ['OPENAI', 'SUBSCR', 'MONTHLY', 'PLEXINCPASS', 'KiwiCo', 'VPN', 'Google Storage', 'hostinger', 'morgen', 'Netusers'],
      'Coffee Shop' : ['KAFE', 'KAVA', 'Coffee', 'Coffee House', 'Starbucks', 'CAFE', 'smoke', 'hookah', 'prazirna', 'Espresso', 'Dok'],
      'Savings' : ['Stavebko', 'Fond', 'Spořící', 'Penzijko'],
      'Insurance' : ['UPLUS'],
      'Hobby' : ['aurapol', 'Dobrovsky', 'knihy', 'books', 'keyboards', 'computers', 'keygem'],
      'Sport' : ['Sportisimo', 'Queen Club', 'Sport', 'Gym'],
      'Shopping' : ['Zmrzlina', 'GECO', 'PRIM', 'Metalshop', 'Elektro', 'Alza', 'Zoo', 'Aktin', 'Dracik', 'suvenyry'],
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
      def __init__(self, df):
            self.vectorizer = TfidfVectorizer()
            self.model = LogisticRegression()
            self.word_vectors = api.load("glove-wiki-gigaword-100")
            df['Concatenated_Details'] = df[['Transaction detail 1', 'Transaction detail 2', 'Transaction detail 3']].fillna('').agg(' '.join, axis=1)
            df['Category'] = df['Concatenated_Details'].apply(categorize_transaction)
            self.df = df
            self.labeled_data = df[df['Category'] != 'Uncategorized']
            self.unlabeled_data = df[df['Category'] == 'Uncategorized']
            
      def embed_sentence(self, sentence):
        words = sentence.split()
        word_embeddings = [self.word_vectors[word] for word in words if word in self.word_vectors]
        if word_embeddings:
            return np.mean(word_embeddings, axis=0)
        else:
            return np.zeros(100)
      
      def prepare_data(self):
            df = self.labeled_data.dropna(subset=['Concatenated_Details', 'Category'])
            X = df['Concatenated_Details'].apply(self.embed_sentence)
            X = np.vstack(X.values)
            y = df['Category']
            return train_test_split(X, y, test_size=0.2, random_state=42)
      
      def train_model(self, X_train, y_train):
            self.model.fit(X_train, y_train)
            
      def evaluate_model(self, X_test, y_test):
            y_pred = self.model.predict(X_test)
            print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
            print(classification_report(y_test, y_pred))
      
      def save_model(self, model_path, vectorizer_path):
            joblib.dump(self.model, model_path)
            joblib.dump(self.vectorizer, vectorizer_path)
            
      def load_model(self, model_path, vectorizer_path):
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            
      def categorize(self, description):
            description_vec = self.vectorizer.transform([description])
            category = self.model.predict(description_vec)[0]
            return category