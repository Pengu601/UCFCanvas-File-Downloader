from operations import *
from tkinter.filedialog import askdirectory
from tkinter import Tk

def mainMenu(headers, params):

    clearTerminal() #clears the terminal output
    
    print("--------------------------------")
    print("1. Courses")  
    print("5. Exit")
    print("--------------------------------")
    choice = input(">> ")
    
    if(choice == '1'):
        courseFileMenu(headers, params)
    
    if(choice == '5'): #exits the program
        return -1
        
    
def courseFileMenu(headers, params):
    courses = getCourses(headers, params) #gets course names and the id corresponding to them
    
    while(1):
        clearTerminal()
        
        print("--------------------------------")
        print("1. Download Course Files (Course Specific)")
        print("2. Download All Course Files")      
        print("5. Back")
        print("--------------------------------")
        choice = input(">> ")
        
        clearTerminal()
            
        courseCount = 1
        if(choice == '1'):
            print("--------------------------------")

            count = 1
            for i in range(len(courses)):
                if(i)%2 == 0:
                    continue
                print(str(count) + '. ' + courses[i])
                count+= 1

            print(f"{count}. Back")
            print("--------------------------------")

            choice = input(">> ")

            if(choice == str(count)):
                continue
            try:
                choiceIndex = int(choice)
                if 1 <= choiceIndex <= count-1:
                    selectedCourse = courses[(choiceIndex*2)-1]
                    selectedCourseId = courses[(choiceIndex*2)-2]
                    
                    clearTerminal()
                    
                    downloadCourseFiles(selectedCourseId, selectedCourse, headers, "0", courseCount, 1)
                    
                else:
                    print("Invalid selection")
            except ValueError:
                print('Please enter a valid number.')
        
        if(choice == '2'):
            
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            
            filePath = askdirectory(title='Select Folder to Download Course Files to') 
            
            for i in range(len(courses)):
                if(i)%2 == 1:
                    print(f"\rDownloading Course {courseCount} of {int(len(courses)/2)} - {courses[i]}")
                    
                    downloadCourseFiles(courses[i-1], courses[i], headers, filePath, courseCount, int(len(courses))/2)
                    
                    clearTerminal()
                    courseCount += 1
                    
            root.destroy()
            
        if(choice == '5'):
            break
    