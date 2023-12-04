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
        
def multiplicative_inverse(exponent, totient):
    multiplicative_inv = 0
    prev_coefficient = 0
    current_coefficient = 1
    new_coefficient = 1
    working_totient = totient

    while exponent > 0:
        quotient = working_totient // exponent
        remainder = working_totient - quotient * exponent
        working_totient = exponent
        exponent = remainder

        next_coefficient = current_coefficient - quotient * prev_coefficient
        update_coefficient = multiplicative_inv - quotient * new_coefficient

        current_coefficient = prev_coefficient
        prev_coefficient = next_coefficient
        multiplicative_inv = new_coefficient
        new_coefficient = update_coefficient

    if working_totient == 1:
        return multiplicative_inv + totient



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

    private_key = multiplicative_inverse(exponent, phi_value)
    return [[exponent, n_value], [private_key, n_value]]


def encrypt(pk, plaintext):
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    aux = [str(pow(char, key, n)) for char in ciphertext]
    # Return the array of bytes as a string
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)
