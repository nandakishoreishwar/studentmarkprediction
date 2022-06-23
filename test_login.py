import streamlit as st
import pandas as pd
import time
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler



# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib

user= ""

def ClassifierPrediction(data):
	weights = open('LRmodel81.pkl','rb')
	classifier = pickle.load(weights)
	encoder = LabelEncoder()
	nonnumeric_columns = [data.columns[index] for index, dtype in enumerate(data.dtypes) if dtype == 'object']
	for column in nonnumeric_columns:
		data[column] = encoder.fit_transform(data[column])
	scaler = StandardScaler()
	x = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
	return classifier.predict(x)



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

menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)
sucess = False


if choice == "Home":
	y=[]
	if len(y)==0:
		st.subheader("Home")
		file = st.file_uploader('Upload a CSV')
		print(file)
		if file :
			df = pd.read_csv(file)
			st.write(df)
			predict = st.button("Predict")
			if predict: 
				y = ClassifierPrediction(df)
				if len(y)!=0:
					st.balloons()
					df['final']=y
					st.write(df)

elif choice == "Login":
	st.subheader("Login Section")

	username = st.text_input("User Name")
	password = st.text_input("Password",type='password')
	if st.button("Login"):
		create_usertable()
		hashed_pswd = make_hashes(password)

		result = login_user(username,check_hashes(password,hashed_pswd))
		if result:
			st.success("Logged In as {}".format(username))
			user=username
		else:
			st.warning("Incorrect Username/Password")


elif choice == "SignUp":
	st.subheader("Create New Account")
	new_user = st.text_input("Username")
	new_password = st.text_input("password",type='password')

	if st.button("Signup"):
		create_usertable()
		add_userdata(new_user,make_hashes(new_password))
		st.success("You have successfully created a valid Account")
		st.info("Go to Login Menu to login")






#task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
#			if task == "Add Post":
#				st.subheader("Add Your Post")
#
#			elif task == "Analytics":
#				st.subheader("Analytics")
#			elif task == "Profiles":
#				st.subheader("User Profiles")
#				user_result = view_all_users()
#				clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
#				st.dataframe(clean_db)