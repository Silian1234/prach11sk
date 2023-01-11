import random
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

def keyGenerator(keyCount):
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    fullPassword = []
    for n in range(keyCount):
        password =''
        for i in range(50):
            password += random.choice(chars)
        if password not in fullPassword:
            fullPassword.append(password)
    return fullPassword

print(keyGenerator(50))