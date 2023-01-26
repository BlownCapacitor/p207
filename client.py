import socket
from tkinter import *
import tkinter as tk
from  threading import Thread
import random
from PIL import ImageTk, Image
from tkmacosx import Button 
import platform

screen_width = None
screen_height = None
SERVER = None
PORT  = None
IP_ADDRESS = None
canvas1 = None
canvas2 = None
nameEntry = None
nameWindow = None
gameWindow = None
ticketGrid  = []
currentNumberList = []
flashNumberList =[]
markedNumberList = []
flashNumberLabel = None
flashNumberLabel2 = None
playerName = None
nameEntry = None
nameWindow = None
gameOver = False

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    thread = Thread(target=recieveMessage)
    thread.start()
    askPlayerName()

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_width
    global screen_height

    nameWindow  = Tk()
    nameWindow.title("Tambola Game: Login")
    nameWindow.geometry('800x533')


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/tambola2.jpeg")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/4.05,screen_height/7.55, text = "Enter Name:", font=("Chalkboard SE",60), fill="black")
    canvas1.create_text( screen_width/4,screen_height/7.5, text = "Enter Name:", font=("Chalkboard SE",60), fill="#32a852")
    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x = screen_width/7, y=screen_height/5.5 )
    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=9, command=saveName, height=1, bg="#80deea", bd=3)
    button.place(x = screen_width/5.5, y=screen_height/4)
    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()

def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global flashNumberLabel
    global flashNumberLabel2


    gameWindow  = Tk()
    gameWindow.title("Tambola Game: Play")
    gameWindow.geometry('800x533')


    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/tambola2.jpeg")
    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")
    canvas2.create_text( screen_width/4.05,50, text = "TAMBOLA", font=("Chalkboard SE",60), fill="black")
    canvas2.create_text( screen_width/4,50, text = "TAMBOLA", font=("Chalkboard SE",60), fill="#32a852")
    flashNumberLabel = canvas2.create_text(screen_width/4.01,501, text = "Waiting For Your Opponent To Join", font=("Chalkboard SE",30), fill="black")
    flashNumberLabel2 = canvas2.create_text(screen_width/4,500, text = "Waiting For Your Opponent To Join", font=("Chalkboard SE",30), fill="#b30000")
    createTicket()
    placeNumbers()
    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def createTicket():
    global gameWindow
    global ticketGrid
    xPos = 105
    yPos = 130
    for row in range(0, 3):
        rowList = []
        for col in range(0, 9):
            if(platform.system() == 'Darwin'):
                boxButton = Button(gameWindow,
                font = ("Chalkboard SE",18),
                borderwidth=3,
                pady=23,
                padx=-22,
                bg="#9ce4e6",
                highlightbackground='#fff176',
                activebackground='#c5e1a5')

                boxButton.configure(command = lambda boxButton=boxButton : markNumber(boxButton))
                boxButton.place(x=xPos, y=yPos)
            else:
                boxButton = tk.Button(gameWindow, font=("Chalkboard SE",30), width=3, height=2,borderwidth=5, bg="#9ce4e6")
                boxButton.configure(command = lambda boxButton=boxButton : markNumber(boxButton))
                boxButton.place(x=xPos, y=yPos)

            rowList.append(boxButton)
            xPos += 64
        ticketGrid.append(rowList)
        xPos = 105
        yPos +=82

def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1
        numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50 , 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        }

        counter = 0
        while (counter < len(randomColList)):
            colNum = randomColList[counter]
            numbersListByIndex = numberContainer[str(colNum)]
            randomNumber = random.choice(numbersListByIndex)

            if(randomNumber not in currentNumberList):
                numberBox = ticketGrid[row][colNum]
                numberBox.configure(text=randomNumber, fg="#2e1c26")
                currentNumberList.append(randomNumber)

                counter+=1

def markNumber(button):
    global markedNumberList
    global flashNumberList
    global playerName
    global SERVER
    global currentNumberList
    global gameOver
    global flashNumberLabel
    global flashNumberLabel2
    global canvas2

    buttonText = int(button['text'])
    markedNumberList.append(buttonText)
    if(platform.system() == 'Darwin'):
        button.configure(state='disabled',disabledbackground='#c5e1a5', disabledforeground="black", highlightbackground="#c5e1a5")
    else:
        button.configure(state='disabled',background='#c5e1a5', foreground="black")

    winner =  all(item in flashNumberList for item in markedNumberList)

    if(winner and sorted(currentNumberList) == sorted(markedNumberList)):
        message = playerName + 'Wins!'
        SERVER.send(message.encode())
        return
    if(len(currentNumberList) == len(markedNumberList)):
        winner =  all(item in flashNumberList for item in markedNumberList)
        if(not winner):
            gameOver = True
            message = 'Better Luck Next Time!'
            canvas2.itemconfigure(flashNumberLabel, text = message, font = ('Chalkboard SE', 40))
            canvas2.itemconfigure(flashNumberLabel2, text = message, font = ('Chalkboard SE', 40))
            loseGame()

def loseGame():
    global ticketGrid
    global flashNumberList
    for row in ticketGrid:
        for numberBox in row:
            if(numberBox['text']):
                if(int(numberBox['text']) not in flashNumberList):
                    if(platform.system() == 'Darwin'):
                        numberBox.configure(state='disabled', disabledbackground='#ffbb00',
                            disabledforeground="white")
                    else:
                        numberBox.configure(state='disabled', background='#ffbb00',
                           foreground="white")

def recieveMessage():
    global SERVER
    global currentNumberList
    global flashNumberLabel
    global flashNumberLabel2
    global canvas2
    global gameOver
    
    numbers = [str(i) for i in range(1,91)]

    while True:
        chunk = SERVER.recv(2048).decode()
        if(chunk in numbers and flashNumberLabel and not gameOver):
            flashNumberList.append(int(chunk))
            canvas2.itemconfigure(flashNumberLabel, text = chunk, font = ('Chalkboard SE', 60))
            canvas2.itemconfigure(flashNumberLabel2, text = chunk, font = ('Chalkboard SE', 60))
        elif('Wins!' in chunk):
            gameOver = True
            canvas2.itemconfigure(flashNumberLabel, text = chunk, font = ('Chalkboard SE', 40))
            canvas2.itemconfigure(flashNumberLabel2, text = chunk, font = ('Chalkboard SE', 40))
   
setup()

