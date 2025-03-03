import unittest
import os
import sys

# Add the src directory to sys.path to allow importing modules from it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from encryption import encrypt_data, decrypt_data

class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt(self):
        password = "test_password"
        original_data = "This is a secret note."
        encrypted = encrypt_data(original_data.encode(), password)
        decrypted = decrypt_data(encrypted, password)
        self.assertEqual(original_data, decrypted.decode())

    def test_wrong_password(self):
        password = "correct_password"
        wrong_password = "incorrect_password"
        original_data = "Another secret note."
        encrypted = encrypt_data(original_data.encode(), password)
        with self.assertRaises(ValueError):
            decrypt_data(encrypted, wrong_password)

if __name__ == "__main__":
    unittest.main()
