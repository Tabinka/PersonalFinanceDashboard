#import pandas as pd
#from dash import Dash
#from basic_layout import BasicLayout
#from starting_layout import StartingLayout
#from expense_categorizer import ExpenseCategorizer
from langchain.document_loaders import CSVLoader
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

loader = CSVLoader("./bank_transactions.csv", encoding="utf-8")
documents = loader.load()
prompt = """ Analyse my bank statement transactions and categorize them based on transaction detail columns. Some of them are in english, some of them are in czech language, but I want my categories to be in english language. """

data = []
# get content of each document, and add to the data list
for index, doc in enumerate(documents):
    data.append(doc.page_content)

# Concatenate the data list using new-line, and append to the prompt text.
prompt_with_data = prompt + "\n\n" + "\n\n".join(data)

# Execute the prompt using streaming method
for chunks in llm.stream(prompt_with_data):
    print(chunks, end="")

#if __name__ == '__main__':
#    app = Dash(__name__, external_stylesheets=external_stylesheets)

    #df = pd.read_csv('bank_transactions.csv')
    # Create model for categorizing expenses and predict
  #  categorizer = ExpenseCategorizer(df)
  #  X_train, X_test, y_train, y_test = categorizer.prepare_data()
  #  categorizer.train_model(X_train, y_train)
   # categorizer.evaluate_model(X_test, y_test)
    #categorizer.save_model('transaction_model.pkl', 'transaction_vectorizer.pkl')
    #categorizer.load_model('transaction_model.pkl', 'transaction_vectorizer.pkl')

    #non_empty_unlabeled = categorizer.unlabeled_data[categorizer.unlabeled_data['Concatenated_Details'].str.strip() != '']
    #non_empty_unlabeled['Predicted_Category'] = non_empty_unlabeled['Concatenated_Details'].apply(categorizer.categorize)

    #final_df = pd.concat([categorizer.labeled_data, categorizer.unlabeled_data, non_empty_unlabeled])

    # Save the final categorized transactions to a new CSV file
    #final_df.to_csv('final_categorized_transactions.csv', index=False)

    #layout = BasicLayout(final_df, app)
#    layout = StartingLayout(app)

#    app.run(debug=True)
