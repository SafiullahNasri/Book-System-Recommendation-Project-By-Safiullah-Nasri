import streamlit as st
import pickle
import pandas as pd
import time

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="📚 Book Recommender",
    page_icon="📖",
    layout="wide"
)

# -----------------------------
# Custom CSS (Enhanced Modern UI)
# -----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.title {
    font-size: 55px;
    font-weight: bold;
    text-align: center;
    color: #ffffff;
    letter-spacing: 1px;
    margin-bottom: 10px;
    animation: fadeIn 1.2s ease-in-out;
}

.card {
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border-radius: 20px;
    padding: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
    transition: all 0.3s ease;
    text-align: center;
}

.card:hover {
    transform: translateY(-10px) scale(1.03);
    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
}

.card img {
    border-radius: 12px;
}

h4 {
    color: #1a1a1a;
    margin-top: 10px;
}

p {
    color: #555;
    font-size: 14px;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 220px;
    font-size: 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #0072ff, #00c6ff);
}

hr {
    border: 1px solid rgba(255,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
books = pickle.load(open('books (1).pkl','rb'))
popular_df = pickle.load(open('popular (1).pkl','rb'))
pt = pickle.load(open('pt (1).pkl','rb'))
similarity_scores = pickle.load(open('similarity_cross.pkl','rb'))

# -----------------------------
# Safe Rating Column Detection
# -----------------------------
def get_rating(row):
    for col in ['avg_rating', 'average_rating', 'rating', 'Avg-Rating']:
        if col in row:
            return row[col]
    return 'N/A'

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(book_name):
    index = books[books['Book-Title'] == book_name].index[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == books.iloc[i[0]]['Book-Title']]
        item = [
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ]
        data.append(item)

    return data

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="title">📚 Smart Book Recommender</div>', unsafe_allow_html=True)
st.write("\n")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["🔥 Popular Books", "🎯 Get Recommendations"])

# -----------------------------
# Popular Books
# -----------------------------
with tab1:
    st.subheader("Trending Books")

    cols = st.columns(5)
    for i in range(min(20, len(popular_df))):
        with cols[i % 5]:
            rating = get_rating(popular_df.iloc[i])

            st.markdown(f"""
            <div class='card'>
                <img src='{popular_df.iloc[i]['Image-URL-M']}' width='100%'>
                <h4>{popular_df.iloc[i]['Book-Title']}</h4>
                <p>{popular_df.iloc[i]['Book-Author']}</p>
                <p>⭐ {rating}</p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# Recommendation Section
# -----------------------------
with tab2:
    st.subheader("Find Your Next Favorite Book 🚀")

    selected_book = st.selectbox(
        "Type or select a book",
        books['Book-Title'].values
    )

    if st.button('Recommend'):
        with st.spinner('Finding best books for you...'):
            time.sleep(1)
            recommendations = recommend(selected_book)

        cols = st.columns(5)
        for i in range(len(recommendations)):
            with cols[i]:
                st.markdown(f"""
                <div class='card'>
                    <img src='{recommendations[i][2]}' width='100%'>
                    <h4>{recommendations[i][0]}</h4>
                    <p>{recommendations[i][1]}</p>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------
# Footer (Your Credit Added)
# -----------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:white; font-size:16px;'>
🚀 Project Developed by <b>Safiullah Nasri</b><br>
Data Scientist | AI Engineer | Data Analyst
</p>
""", unsafe_allow_html=True)