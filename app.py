import streamlit as st
from tfidf_model import predict_movie_rating
from io import StringIO

def main():

    #set page configuration
    st.set_page_config('Screenplay Rating App', page_icon=':film_projector:')

    st.title(":film_projector: Screenplay Rating App")
    st.markdown("---")
    st.markdown("Welcome to the **Screenplay Rating App**! \n\nDeveloped by a bunch of MDSI students at the University of Technology Sydney, this app predicts the classification your screenplay will get assigned.")
    st.image('assets/classification_image.jpg', use_column_width=True)

    st.markdown("---")
    st.markdown("### Get started by uploading your screenplay as a .txt file")
    # Example usage: Provide a new screenplay text
    uploaded_file = st.file_uploader("Choose a .txt file to upload")
    st.markdown("---")
    
    if uploaded_file is not None:
        
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        screenplay_text = stringio.read()
    
    # st.write(f"Screenplay_text: {screenplay_text}")
        with st.spinner("Rating your screenplay..."):
            predicted_rating = predict_movie_rating(screenplay_text)
    # Example usage: Provide a new screenplay text
        predicted_rating = predict_movie_rating(screenplay_text)
        print(f"Predicted Rating: {predicted_rating}")

    # Generate the findings
        st.write(f"Your screenplay will likely recieve a classification of: {predicted_rating}")
        if predicted_rating == 'G':
            st.image('assets/g_rating.svg')
        elif predicted_rating == 'PG':
            st.image('assets/pg_rating.svg')
        elif predicted_rating == 'M':
            st.image('assets/m_rating.svg')
        elif predicted_rating == 'MA15':
            st.image('assets/ma_rating.svg')
        elif predicted_rating == 'R18':
            st.image('assets/r_rating.svg')
        
if __name__== "__main__":
    main()