import pandas as pd
from dash import Dash
from basic_layout import BasicLayout
from starting_layout import StartingLayout
from expense_categorizer import ExpenseCategorizer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

if __name__ == '__main__':
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    
    df = pd.read_csv('bank_transactions.csv')
    
    # Create model for categorizing expenses and predict 
    categorizer = ExpenseCategorizer(df)
    X_train, X_test, y_train, y_test = categorizer.prepare_data()
    categorizer.train_model(X_train, y_train)
    categorizer.evaluate_model(X_test, y_test)
    categorizer.save_model('transaction_model.pkl', 'transaction_vectorizer.pkl')
    categorizer.load_model('transaction_model.pkl', 'transaction_vectorizer.pkl')
    categorizer.unlabeled_data['Predicted_Category'] = categorizer.unlabeled_data['Concatenated_Details'].apply(categorizer.categorize)
    final_df = pd.concat([categorizer.labeled_data, categorizer.unlabeled_data])
    
    # Save the final categorized transactions to a new CSV file
    final_df.to_csv('final_categorized_transactions.csv', index=False)
    
    layout = BasicLayout(final_df, app)
    
    app.run(debug=True)
