
from authentication import *
from menu import *

def main():
    
    headers = getToken() #gets auth token from user
    
    params = {
        'enrollment_state' : 'active', #used to only get courses that are currently active
    } 

    end = 0
    while(end != -1):
        end = mainMenu(headers, params) #opens menu for user until they exit
    
if __name__ == "__main__":
    main()
