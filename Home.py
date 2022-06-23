import streamlit as st
import pandas as pd
import time
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler



# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib

user= ""


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

st.title("Student Mark Prediction")

st.subheader("Login Section")
username = st.text_input("User Name")
password = st.text_input("Password",type='password')
if st.button("Login"):
	create_usertable()
	hashed_pswd = make_hashes(password)
	result = login_user(username,check_hashes(password,hashed_pswd))
	if result:
		st.success("Logged In as {}".format(username))
	else:
		st.warning("Incorrect Username/Password")


