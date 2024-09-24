import streamlit as st
import pandas as pd
import pickle

# Load the preprocessed dataset



books = pd.read_csv(r"/Users/adithkumar/Desktop/P433/Books.csv", encoding='ISO-8859-1')
books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)


## Drop duplicate rows
books.drop_duplicates(keep='last', inplace=True) 
books.reset_index(drop = True, inplace = True)


with open('/Users/adithkumar/Desktop/P433/books_recommendation_system.pkl', 'rb') as f:
    dataset1 = pickle.load(f)

# Function to recommend books based on popularity
def popularity_based(dataframe, n):
    if 1 <= n <= len(dataframe):
        data = pd.DataFrame(dataframe.groupby('ISBN')['Book-Rating'].count()).sort_values('Book-Rating', ascending=False).head(n)
        result = pd.merge(data, books, on='ISBN')
        return result[['Book-Title', 'Book-Author', 'Publisher', 'Year-Of-Publication']]
    else:
        return "Invalid number of books entered!!"

# Streamlit UI
st.title('Books Recommendation System')

# Get user input for book name and number of recommendations
st.subheader('Enter your preferences:')
book_name = st.text_input("Enter a book name (for author-based recommendations):", "Harry Potter and the Sorcerer's Stone")
num_books = st.number_input("Enter the number of books to recommend:", min_value=1, max_value=20, value=5)

# Recommendation Type
rec_type = st.selectbox("Choose the type of recommendation:", 
                        ["Popularity Based", "Books by Same Author/Publisher"])

if st.button('Get Recommendations'):
    if rec_type == "Popularity Based":
        st.write(f"Top {num_books} Popular Books:")
        result = popularity_based(dataset1, num_books)
        st.dataframe(result)

    elif rec_type == "Books by Same Author/Publisher":
        # Recommend books by the same author or publisher (as per user input)
        book_data = dataset1[dataset1['Book-Title'].str.contains(book_name, case=False, na=False)]
        
        if not book_data.empty:
            author_name = book_data['Book-Author'].values[0]
            publisher_name = book_data['Publisher'].values[0]
            
            st.write(f"Books by the same author ({author_name}):")
            author_books = dataset1[dataset1['Book-Author'] == author_name]
            st.dataframe(author_books[['Book-Title', 'Book-Author', 'Publisher', 'Year-Of-Publication']].head(num_books))
            
            st.write(f"Books by the same publisher ({publisher_name}):")
            publisher_books = dataset1[dataset1['Publisher'] == publisher_name]
            st.dataframe(publisher_books[['Book-Title', 'Book-Author', 'Publisher', 'Year-Of-Publication']].head(num_books))
        else:
            st.write("Book not found in the dataset.")








