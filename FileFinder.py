import os 
import time
from tkinter import Tk
from tkinter.filedialog import askdirectory
import operator
from colorama import Fore, init, Back
from pathlib import Path
import win32security
from console_progressbar import ProgressBar
import time

init(strip=False)
os.system("cls || clear")
red = Fore.RED
lred = Fore.LIGHTRED_EX
black = Fore.BLACK
lblack = Fore.LIGHTBLACK_EX
white = Fore.WHITE
lwhite = Fore.LIGHTWHITE_EX
lcyan = Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lmagenta = Fore.LIGHTMAGENTA_EX
yellow = Fore.YELLOW
lyellow = Fore.LIGHTYELLOW_EX
blue = Fore.BLUE
lblue = Fore.LIGHTBLUE_EX
reset = Fore.RESET
green = Fore.GREEN
lgreen = Fore.LIGHTGREEN_EX
cyan = Fore.CYAN

help_message = f"""
{lred}     ╔══════════════════════════════════╗                 _____ ___ _      _____ _           _                      
{lyellow}     ║   ► Commands:                    ║                |  ___|_ _| | ___|  ___(_)_ __   __| | ___ _ __ 
{lred}     ║                                  ║                | |_   | || |/ _ \ |_  | | '_ \ / _` |/ _ \ '__|
{lyellow}     ║   • filefinder                   ║                |  _|  | || |  __/  _| | | | | | (_| |  __/ |  
{lred}     ║   • choosepath                   ║                |_|   |___|_|\___|_|   |_|_| |_|\__,_|\___|_|
{lyellow}     ║   •                              ║
{lred}     ║   • cls                          ║
{lyellow}     ║                                  ║
{lred}     ╚══════════════════════════════════╝"""



def checkVersion():
    r = requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/settings.json')  # Get the latest version
    last_version = r.text
    js_version = json.loads(last_version)
    last_version = js_version['version']
                                   

### Zapisywać do pliku za każdym odczytem //DONE
### Pierwsza linia tekstu = nagłówek [sciezka ] [data] [rozmiar] [ JAK SIE UDA WLASCICIEL ] //DONE
### Rozdzielac srednikami //DONE FileCounter
### Dane bez naglowkow  ///DONE
### Zlapac focus  
### ProgressBar, EstTime, Percentage @!!! //UNDONE

path = os.getcwd()
def choosePath():
    global path
    root = Tk()
    root.withdraw()
    path = askdirectory(title='Select Folder')

_owner_sid_cache = {}
def getOwner(FILENAME):
    # open (FILENAME, "r").close ()
    sd = win32security.GetFileSecurity (FILENAME, win32security.OWNER_SECURITY_INFORMATION)
    owner_sid = sd.GetSecurityDescriptorOwner ()
    if str(owner_sid) not in _owner_sid_cache:
        name, _domain, _type = win32security.LookupAccountSid (None, owner_sid)
        _owner_sid_cache[str(owner_sid)] = name
    return _owner_sid_cache[str(owner_sid)]

def getFiles():
    
    listOfFiles = []
    
    open("output.txt", "w").close()
    with open("output.txt","r+") as f:
        f.truncate(0)
        f.write("Nazwa Pliku; "+"Data Modyfikacji; "+"Rozmiar; "+"Wlasciciel pliku; ")
        f.write('\n')
    pb = ProgressBar(total=sum([len(files) for r, d, files in os.walk(path)]),prefix='', suffix='', decimals=3, length=50, fill='█', zfill='░')
    for root, dirs, files in os.walk(path):
        start = time.time()
        for file in files:
            listOfFiles.append(os.path.join(root,file))
            
            
            os.system("cls  || clear")
            for name in listOfFiles:
                start = time.time()
                

                file_size = round((os.path.getsize(name)/1048576),3)
                file_date = time.ctime(os.path.getctime(name))
            if(file_size/1048576)<10:
                with open("output.txt","a+") as f:
                    
                    f.write(str(name)+";  "+str(file_size)+";  "+str(file_date)+";  ")
                    pb.print_progress_bar(sum(1 for _ in open('output.txt')))
                    

                    #print("Est. time: "+str((duration/sum(1 for _ in open('output.txt')))*(sum([len(files) for r, d, files in os.walk(path)]))-sum(1 for _ in open('output.txt'))))
                    ## ZLOTO sum([len(files) for r, d, files in os.walk(path)])
                    try:
                        f.write(getOwner(name))
                    except:
                        f.write("Couldn't get owner of the file")
                        
                    f.write('\n')

            else:
                print("No files found")
            if(not listOfFiles):
                print("No files found")

        

def commandListening():
    argument = input().split()
    command = argument[0]
    if len(argument) == 0:
        print(f"\n   Unknown command. Type help to see the available commands.")
    elif command.lower() == "cls" or command.lower() == "clear":
        os.system("cls  || clear")
        print(help_message)
    elif command.lower() == "filefinder":
        getFiles()
    elif command.lower() == "choosepath":
        choosePath()


if __name__ == "__main__":
    checkVersion()
    os.system("clear || cls & title FileFinder")
    print(help_message)
    while True:
        if os.name == "nt":
            py = "python"
            print(f"\n    {reset}{lred} root@windows:~/FileFinder# » ", end="")
            commandListening() 
                
