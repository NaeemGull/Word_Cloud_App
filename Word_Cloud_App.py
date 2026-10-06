from django.core.files import uploadedfile
from pyautogui import resolution
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import PyPDF2
from docx import Document
import plotly.express as px
import base64
from io import BytesIO

# Function for file reading 
def read_text(file):
    return file.getvalue().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    return "\n".join([page.extract_text() for page in pdf.pages])


# Function to filter text
def filter_stopwords(text, additional_stopwords):
    words = text.split()
    all_stopwords = STOPWORDS.union(set(additional_stopwords))
    filtered_words = [word for word in words if word.lower() not in all_stopwords]
    return " ".join(filtered_words)

# Function get to create download link for the plot
def get_image_download_link(buffer, format_):
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:image/{format_};base64,{image_base64}" download="wordcloud.{format_}">Download Word Cloud</a>'

# Function to generate a download link for a DataFrame as a CSV file
def get_table_download_link(df, filename, file_label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{file_label}</a>'

# Streamlit app layout code
st.title("Word Cloud Generator")
st.subheader("Upload a text file, PDF, or Word document to generate a word cloud.")


uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
# st.set_option('deprecation.showfileUploaderEncoding', False)


if uploaded_file:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)

    # Check the file type and read the file accordingly
    if uploaded_file.type == "text/plain":
        text = read_text(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = read_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
        st.stop()

    # Generate word count table
    words = text.split()
    word_count = pd.DataFrame({'Word' : words}).groupby('Word').size().reset_index(name='Count').sort_values(by='Count', ascending=False)

    # Sidebar : Checkbox and Multiselect for stopwords
    use_standard_stopwords = st.sidebar.checkbox("Use standard stopwords", True)
    top_words = word_count['Word'].head(50).tolist()
    additional_stopwords = st.sidebar.multiselect("Select additional stopwords", sorted(top_words))

    if use_standard_stopwords:
        all_stopwords = STOPWORDS.union(set(additional_stopwords))

    else:
        all_stopwords = set(additional_stopwords)

    text = filter_stopwords(text, all_stopwords)

    if text:
        # word cloud dimensions
        width = st.sidebar.slider("Width", 400, 2000, 1200, 50)
        height = st.sidebar.slider("Height", 200, 2000, 800, 50)

        # Generate the word cloud
        st.subheader("Generate Word Cloud")
        fig, ax = plt.subplots(figsize=(width/100, height/100))
        wordcloud_img = WordCloud(width=width, height=height, background_color='white', max_words=200, stopwords=all_stopwords).generate(text)
        ax.imshow(wordcloud_img, interpolation='bilinear')
        ax.axis('off')

        # Save plot functionality
        format_ = st.sidebar.selectbox("Select format for download", ["png", "jpg", "svg",  "pdf"])
        resolution = st.sidebar.slider("Select Resolution (DPI)", 50, 300, 100, 10)

        # Generate word count table
        st.subheader("Word Count Table")
        words = text.split()
        word_count = pd.DataFrame({'Word' : words}).groupby('Word').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
        st.write(word_count)
    st.pyplot(fig)
    if st.button("Save as png"):
        buffered = BytesIO()
        plt.savefig(buffered, format=format_, dpi=resolution)
        st.markdown(get_image_download_link(buffered, format_), unsafe_allow_html=True)


    # Word count table at the end
    st.sidebar.markdown("---")
    st.sidebar.subheader("Subscribe to our Channel to learn Data Science in Urdu")

    # Add a youtube video 
    st.sidebar.video("https://youtu.be/TS8wb9IMHA4?si=30Gpx-oEl4NsXNGM")
    st.sidebar.markdown("---")

    # Add author name and info 
    st.sidebar.markdown("Create by: Naeem Sulemani")
    # st.sidebar.markdown("contact: [Email] (mail to : naeemgul953@gmail.com)")






    # filter out stopwords
    text = filter_stopwords(text,["said", "say", "says", "will", "one", "went", "goes", "just", "like", "also", "get", "got", "even", "back", "much", "many", "make", "made", "take", "took", "see", "seen", "come", "came"])







    




