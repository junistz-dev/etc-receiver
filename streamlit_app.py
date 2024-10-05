from function import decompress_image, decrypt_image
from PIL import Image
import streamlit as st
import io

download_ready = False
image_bytes = None
mime_type = "image/jpeg"  # Default MIME type for JPEG


def convert_image_to_bytes(image, image_format):
    img_io = io.BytesIO()
    image.save(img_io, format=image_format)  # Use format argument
    return img_io.getvalue()


def is_valid_secret_key(secret_key):
    try:
        key_parts = [int(part) for part in secret_key.split('-')]
        if len(key_parts) != 4:
            return False
        for part in key_parts:
            if not (0 <= part <= 65535):
                return False
        return True
    except ValueError:
        return False


st.markdown("""
    <h1 style='text-align: center;'>
        ETC <span style='color: #B3EBF2;'>Receiver</span> Application
    </h1>
    """,
            unsafe_allow_html=True)

image = Image.open("Sender Image.png")
st.image(image, use_column_width=True)

st.write(
    "This receiving function allows you to upload a TXT file and download the Original Image with JPEG file."
)

with st.form("receiver_form"):
    uploaded_file = st.file_uploader("Upload a TXT file", type=["txt"])

    secret_key = st.text_input(
        "Enter the secret key (4 parts separated by hyphens)",
        placeholder="23516-1642-598-6027")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if uploaded_file is None:
            st.error("No TXT file uploaded. Please upload a TXT file.")
        elif not secret_key:
            st.error("Please enter the secret key.")
        elif not is_valid_secret_key(secret_key):
            st.error(
                "Invalid secret key. Please enter 4 numbers between 0 and 65535, separated by hyphens."
            )
        else:
            download_ready = True
            decompressed_image = decompress_image(uploaded_file)
            decrypted_image = decrypt_image(decompressed_image, secret_key)

            st.image(decrypted_image,
                     caption="Decrypted Image",
                     use_column_width=True)

            # Set format to JPEG
            image_format = "JPEG"
            image_bytes = convert_image_to_bytes(decrypted_image, image_format)

if download_ready:
    st.download_button(label="Download Decrypted Image (JPEG)",
                       data=image_bytes,
                       file_name="decrypted_image.jpeg",
                       mime=mime_type)
