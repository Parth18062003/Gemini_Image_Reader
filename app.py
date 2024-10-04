import streamlit as st
from PIL import Image
import io
import google.generativeai as genai
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()
# Streamlit application
def main():
    st.title("Image Description and Q&A with Gemini")
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Read the image and display it
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Convert image to RGB if it is in RGBA mode
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image.save(temp_file, format='JPEG')
            temp_file_path = temp_file.name

        # Upload the file to Gemini
        myfile = genai.upload_file(temp_file_path)  # Pass the path to the temporary file
        st.success("File uploaded successfully!")

        # Ask a question about the image
        question = st.text_input("Ask a question about the image:")
        if st.button("Get Answer"):
            if question:
                # Generate content based on the uploaded image and the user's question
                model = genai.GenerativeModel("gemini-1.5-flash")
                result = model.generate_content([myfile, "\n\n", question])

                # Display the result
                st.success("Response from Gemini:")
                st.write(result.text)

        # Clean up the temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()
