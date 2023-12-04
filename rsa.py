"""
Author: Kaan Kahraman
Email: 22093045@mail.baskent.edu.tr

Purpose:
- This file 'rsa.py' contains the implementation of the RSA encryption and decryption algorithms. 
- It includes functions for generating RSA key pairs, encrypting plaintext, and decrypting ciphertext.
- This script is utilized by the 'main.py' Streamlit web application encryption and decryption processes.

Project: Bil443 Cryptography and Security
"""
import random


def greatest_common_divisor(num1, num2):
    while num2 != 0:
        num1, num2 = num2, num1 % num2
    return num1


def find_multiplicative_inverse(exponent, phi_value):
    inverse = 0
    previous_inverse = 0
    next_inverse = 1
    current_phi_value = phi_value

    while exponent > 0:
        quotient = current_phi_value // exponent
        remainder = current_phi_value - quotient * exponent
        current_phi_value = exponent
        exponent = remainder

        temp_inverse = next_inverse - quotient * previous_inverse
        next_temp_inverse = inverse - quotient * current_phi_value

        next_inverse = previous_inverse
        previous_inverse = temp_inverse
        inverse = current_phi_value
        current_phi_value = next_temp_inverse

    if current_phi_value == 1:
        return inverse + phi_value


def is_prime(number):
    if number == 2:
        return True
    if number < 2 or number % 2 == 0:
        return False
    for current_number in range(3, int(number**0.5) + 2, 2):
        if number % current_number == 0:
            return False
    return True


def generate_key_pair(prime1, prime2):
    if not (is_prime(prime1) and is_prime(prime2)):
        raise ValueError('Both numbers must be prime.')
    elif prime1 == prime2:
        raise ValueError('The primes cannot be equal')

    n_value = prime1 * prime2
    phi_value = (prime1 - 1) * (prime2 - 1)

    exponent = random.randrange(1, phi_value)
    gcd_value = greatest_common_divisor(exponent, phi_value)
    while gcd_value != 1:
        exponent = random.randrange(1, phi_value)
        gcd_value = greatest_common_divisor(exponent, phi_value)

    private_key = find_multiplicative_inverse(exponent, phi_value)
    return [[exponent, n_value], [private_key, n_value]]


def encrypt(public_key, plaintext):
    key, n_value = public_key
    cipher = [pow(ord(character), key, n_value) for character in plaintext]
    return cipher


def decrypt(private_key, ciphertext):
    key, n_value = private_key
    plaintext_characters = [
        str(pow(char, key, n_value)) for char in ciphertext
    ]
    plaintext = [chr(int(char_value)) for char_value in plaintext_characters]
    return ''.join(plaintext)
