"""
Author: Kaan Kahraman
Email: 22093045@mail.baskent.edu.tr

Purpose:
- This file 'main.py' is the main script for a Streamlit web application.
- It is designed for demonstrating encryption and decryption functionalities as part of the Bil443 Cryptography and Security class. 
- The app provides a user interface for uploading files, encrypting them using RSA algorithm implemented in 'rsa.py', and downloading the encrypted or decrypted files.

Project: Bil443 Cryptography and Security
"""
import streamlit as st
import rsa

# Initialize session state variables if they don't exist
if 'public_key' not in st.session_state:
    st.session_state['public_key'] = None
if 'private_key' not in st.session_state:
    st.session_state['private_key'] = None


# Encryption function
def encrypt_file(file_content, pub_key):
    # Assuming file_content is a string
    return rsa.encrypt(pub_key, file_content)


# Decryption function
def decrypt_file(file_content, priv_key):
    # file_content should be a list of integers
    return rsa.decrypt(priv_key, file_content)


# Title of the app
st.title('File Encryption/Decryption App')

# Input for prime numbers
st.header("RSA Key Generation")
p = int(st.text_input("Enter a prime number (p)", value="3"))
q = int(st.text_input("Enter a different prime number (q)", value="2"))

# Checkbox to skip prime check
skip_prime_check = st.checkbox(
    "Skip prime number check (Not recommended unless you are sure)")

if skip_prime_check:
    st.warning(
        "Warning: Skipping the prime number check can lead to incorrect key generation and insecure encryption. Use this option only if you are certain about the primality of the numbers."
    )

# Generate RSA Keys based on user input
if st.button('Generate RSA Keys'):
    if skip_prime_check or (rsa.is_prime(p) and rsa.is_prime(q) and p != q):
        st.session_state['public_key'], st.session_state[
            'private_key'] = rsa.generate_key_pair(p, q)
        st.success("RSA Keys generated successfully!")
    else:
        st.error("Both numbers must be prime and different.")

# Encryption Section
if st.session_state['public_key'] and st.session_state['private_key']:
    st.write("Generated n Value ", st.session_state['public_key'][1])
    st.write("Public Key (Share this) ", st.session_state['public_key'][0])
    st.write("Private Key (Keep this secret!) ",
             st.session_state['private_key'][0])
    st.header("Encryption")
    uploaded_file_encrypt = st.file_uploader("Choose a file to encrypt",
                                             key="file_uploader_encrypt",
                                             type=["txt"])
    if st.button('Encrypt File', key="encrypt_file_button"):
        if uploaded_file_encrypt:
            file_content = uploaded_file_encrypt.getvalue().decode(
            )  # Decode to string
            encrypted_file = encrypt_file(file_content,
                                          st.session_state['public_key'])
            encrypted_data = ','.join(map(
                str, encrypted_file))  # Convert to string for download
            st.download_button(label="Download Encrypted File",
                               data=encrypted_data,
                               file_name="encrypted_file.txt",
                               mime='text/plain')
        else:
            st.error("Please upload a file.")

    # Decryption Section
    st.header("Decryption")
    uploaded_file_decrypt = st.file_uploader("Choose a file to decrypt",
                                             key="file_uploader_decrypt",
                                             type=["txt"])
    key = int(
        st.text_input("Enter the private key please. Current Key: ",
                      value=f"{st.session_state['private_key'][0]}"))
    if st.button('Decrypt File', key="decrypt_file_button"):
        if uploaded_file_decrypt and key:

            file_content = uploaded_file_decrypt.getvalue().decode(
            )  # Decode to string
            encrypted_data = list(map(
                int,
                file_content.split(',')))  # Convert back to list of integers
            decrypted_file = decrypt_file(
                encrypted_data, [key, st.session_state['private_key'][1]])
            st.download_button(label="Download Decrypted File",
                               data=decrypted_file,
                               file_name="decrypted_file.txt",
                               mime='text/plain')
        else:
            st.error("Please upload a file.")
