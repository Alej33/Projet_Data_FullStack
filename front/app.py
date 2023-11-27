import streamlit as st
import requests

# URL of your FastAPI backend
BACKEND_URL = "http://localhost:8000"

def show_homepage():
    st.title("Welcome to the Book Exchange Site") 

    response = requests.get(f"{BACKEND_URL}/books")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            st.subheader(book['title'])
            # Display other book details
    else:
        st.error("Failed to retrieve books.")

def add_book_post():
    st.title("Add a New Book")
    with st.form(key='book_form'):
        title = st.text_input("Title")
        genre = st.text_input("Genre")
        desired_genre = st.text_input("Desired Genre")
        country = st.text_input("Country")
        city = st.text_input("City")
        description = st.text_area("Description")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            book_data = {
                "title": title,
                "genre": genre,
                "desired_genre": desired_genre,
                "country": country,
                "city": city,
                "description": description
            }
            response = requests.post(f"{BACKEND_URL}/join-us/add-post", data=book_data)
            if response.status_code == 201:
                book_added_successfully()
            else:
                st.error("Failed to add the book. Error: " + response.text)

def book_added_successfully():
    st.title("Book Added Successfully!")
    st.write("Your book has been added to the exchange.")

    # Button to return to the homepage
    if st.button("Back to Homepage"):
        show_homepage()

def main():
    # Directly call the homepage function
    show_homepage()

if __name__ == "__main__":
    main()
