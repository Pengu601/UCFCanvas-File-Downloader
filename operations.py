import requests
from authentication import *
from tkinter import Tk
from tkinter.filedialog import askdirectory
import time
import os
import sys
from tqdm import tqdm
import zipfile

def clearTerminal():
    # time.sleep(10)
    if os.name == 'nt':
        os.system('cls')

    # For Linux/macOS
    else:
        os.system('clear')

def tokenToUser(token): #takes the Auth token and returns the user's name associated with it
    headers ={'Authorization': f'Bearer {token}'}
    response = requests.get('https://webcourses.ucf.edu/api/v1/users/self/favorites/courses', headers=headers)
    data = response.json()
    
    userId= data[0]['enrollments'][0]['user_id'] #gets the user id found from course enrollments
    
    response = requests.get(f'https://webcourses.ucf.edu/api/v1/users/{userId}/profile', headers= headers) #gets user profile info
    data = response.json()
    
    return data['name'] #returns the name associated to user profile (id)
    
#gets all the course names and the Course ID associated with it
def getCourses(headers, params):
    response = requests.get('https://webcourses.ucf.edu/api/v1/users/self/favorites/courses', headers=headers, params = params)
    data = response.json()
    
    courses = []
    for i in data: #appends the id of course then the course name into array
        courses.append(i['id'])
        courses.append(i['name'].rsplit('-', 1)[0])

    return courses
   
def downloadCourseFiles(courseID, courseName, headers, filePath, courseCount, courseAmount):
    #get directory path of where user wants to download course files
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    
    if(courseAmount == 1):
        print(f'You selected {courseName}') #if single course download, display name of course
        
    if(filePath == "0"): #if single course download, get filePath
        filePath = askdirectory(title='Select Folder to Download Course Files to') 

    #get request to download content from course
    request = requests.post(f'https://webcourses.ucf.edu/api/v1/courses/{courseID}/content_exports', headers=headers, params= {'export_type': 'zip'} )

    data = request.json()
    
    contentID = data['id'] #ID for content export job
    
    #Gets progress for Content Download
    progressURL = data['progress_url']
    progressID = progressURL.rsplit('/', 1)[-1] #gets the progress ID by taking the numbers after the last / in the url string
    
    #Until Download to server Completes, update progress completion
    if100 = 0
    
    #Displays download progress for requestion content export
    while(True): 
        progressRequestRAW = requests.get(f'https://webcourses.ucf.edu/api/v1/progress/{progressID}', headers = headers)
        progressRequest = progressRequestRAW.json()
        progressBar = progressRequest['completion'] #gets the current percentage of the download progress

        if(str(progressRequest['workflow_state']) == 'completed'): #if the file isn't ready to be downloaded, keep stalling
            time.sleep(1)
            break
        
        if(if100 == 1):
            continue
        
        if(progressBar == '100'):
            if100 = 1
        sys.stdout.write(f"\rDownloading... {int(progressBar)}%") #Displays download progress
        sys.stdout.flush()
        time.sleep(.05)
        

    #gets paginated list containing url needed for content download
    contentURLRAW = requests.get(f'https://webcourses.ucf.edu/api/v1/courses/{courseID}/content_exports/{contentID}', headers=headers)
    contentURL = contentURLRAW.json()

    #gets download url and file name from paginated list, and assign save path to the os to download the export to
    downloadURL = contentURL['attachment']['url']
    fileName = contentURL['attachment']['filename']
    savePath = os.path.join(filePath, fileName) #path to store file into
    
    with requests.get(downloadURL, stream=True) as downloadContent: #progress bar for extracting to directory
        # Get the total file size from the headers
        total_size = int(downloadContent.headers.get('content-length', 0))
        
        # Open the file to write in binary mode
        with open(savePath, 'wb') as file, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=f"Writing {fileName} to Directory", ascii=True
        ) as pbar:
            # Iterate over the response in chunks
            for chunk in downloadContent.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive chunks
                    file.write(chunk)
                    pbar.update(len(chunk))  # Update progress bar with chunk size
    
    extractFileContents(savePath, filePath, courseName, courseCount, courseAmount) #Unzips and rename file to course name
    
    print(f'Success! Downloaded and Extracted to {filePath}')
    
    time.sleep(3)
    root.destroy()
    
def extractFileContents(savePath, filePath, courseName, courseCount, courseAmount):
    newPath = os.path.join(filePath.strip(), courseName.strip())  #gets the new path for the extract folder
    
    if not os.path.exists(newPath):
        os.makedirs(newPath) #if folder doesnt already exist, create it

    with zipfile.ZipFile(savePath,'r') as zip_ref:
        zip_ref.extractall(newPath) #extract downloaded zip contents to folder
    
    os.remove(savePath) #remove zip file
    
    if(courseCount == courseAmount): #open directory only if all course files are downlaoded
        os.startfile(filePath)
    
    