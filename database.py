import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session
from flask import Flask, request, send_file
import io

def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="root", db="fnd")
    c = _conn.cursor()

    return c, _conn


def aa_log(username, password):
    try:
        c, conn = db_connect()
        j = c.execute("select * from admin where username='" +
                      username+"' and password='"+password+"'")
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))
    

def owner_reg(username,password,email,mobile,address):
    try:
        c, conn = db_connect()
        print(username,password,email,address)
        id="0"
        status = "pending"
        j = c.execute("insert into user (id,username,password,email,mobile,address,status) values ('"+id +
                      "','"+username+"','"+password+"','"+email+"','"+mobile+"','"+address+"','"+status+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    


import re

def clean_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
    
def predict_act(username,image,new_article,prediction_label):
    try:
        c, conn = db_connect()
        print(username,image,new_article,prediction_label)
        id="0"
        status = "pending"

        new_article = clean_text(new_article)
        
        
        j = c.execute("insert into predict (id,username,image,news,prediction) values ('"+id +
                      "','"+username+"','"+image+"','"+str(new_article)+"','"+prediction_label+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    


def owner_login(username, password):
    try:
        c, conn = db_connect()
        
        j = c.execute("select * from user where username='" +
                      username+"' and password='"+password+"' and status='activated'  "  )
        c.fetchall()
        
        conn.close()
        return j
    except Exception as e:
        return(str(e))
    
def vu1():
    c, conn = db_connect()
    c.execute("select * from user  ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def vn1():
    c, conn = db_connect()
    c.execute("select * from predict where prediction='True'  ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def van2():
    c, conn = db_connect()
    c.execute("select * from predict   ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


def vu3(b,d):
    try:
        c, conn = db_connect()
        id="0"
        
        j = c.execute("update user set status='activated' where username='"+b+"' and email='"+d+"' ")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    
def vu5(b,d):
    try:
        c, conn = db_connect()
        id="0"
        
        j = c.execute("update user set status='rejected' where username='"+b+"' and email='"+d+"' ")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
# -------------------------------Registration-----------------------------------------------------------------
