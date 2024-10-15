
import sqlite3
from operations import *
from cryptography.fernet import Fernet
import os

def getToken():
    key = loadKey() #gets encryption key
    authToken = checkTokens(key) #gets the auth token for user

    if(authToken == ""):
        authToken = input("Please enter Token: ")
        headers ={'Authorization': f'Bearer {authToken}'}
        storeToken(authToken, key) #stores encrypted auth token into db for future program uses
    else:
        headers = {'Authorization': f'Bearer {authToken}'}    
    
    return headers #returns the header used for post/get requests

def storeToken(authToken, key): #stores token into table if it doesn't exist already
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    fernet = Fernet(key)
    encryptedAuthToken = fernet.encrypt(authToken.encode()) #encrypts auth token using key
    cursor.execute("CREATE TABLE IF NOT EXISTS auth_token (id INTEGER PRIMARY KEY, user_token TEXT)")

    cursor.execute("INSERT INTO auth_token (user_token) VALUES (?)", (encryptedAuthToken.decode(),)) #insert encrypted auth token into db
    connection.commit()
    
    connection.close()
    
def checkTokens(key): #checks for any 
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    #checks to see if db is empty
    cursor.execute("SELECT name FROM sqlite_master ")
    tables = cursor.fetchall()
   
    if len(tables) == 0: #if db is empty, make user input new auth token 
        return ""
    
    #finds all auth tokens associated with db
    cursor.execute("SELECT * FROM auth_token")
    users = []
    fernet = Fernet(key)
    for row in cursor.fetchall():
        user = fernet.decrypt(row[1].encode()).decode() #decrypts the encrypted auth tokens getting pulled from db
        users.append(tokenToUser(user)) #converts the decrypted auth token to user's name and stores in array
    
    #displays all the available users to login as 
    for i in range(len(users)):
        print(f"{i+1}. {users[i]}")   
        if(i == (len(users))-1):
            print(f"{i+2}. Add New User") 
        
    print("--------------------------------")
    user = input(">> ")

    if(user == str(len(users)+1)): #if option was "Add New User", let user input new auth token to login as
        return ""
    
    cursor.execute("SELECT * FROM auth_token WHERE id = ?", (user,)) #get the chosen user's auth token
    row = cursor.fetchone()
    
    connection.close()

    decryptedToken = fernet.decrypt(row[1].encode()).decode() #decode the token
    return decryptedToken

KEY_FILE_PATH = os.path.expanduser("~/.my_app_encryption_key") #path to store the file where key is stored

def generateKey(): #generates an encryption key if not already existed on user's machine
    key = Fernet.generate_key()
    with open(KEY_FILE_PATH, 'wb') as key_file:
        key_file.write(key)
    
    os.chmod(KEY_FILE_PATH, 0o600) #raise the file's permission level so only admin can access

def loadKey(): #loads key if found on user's machine, else generates a new key
    if not os.path.exists(KEY_FILE_PATH): #if key doesn't exist, generate a key
        generateKey()
    
    with open(KEY_FILE_PATH, 'rb') as key_file:
        key = key_file.read() 
    
    return key