# Sources
# https://www.codegrepper.com/code-examples/python/how+to+open+inspect+element+in+chrome+using+selenium

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
import time  
import os
from time import sleep, strftime
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains




# Creating an instance webdriver
c = webdriver.ChromeOptions()
#incognito parameter passed
c.add_argument("--incognito")
#set chromodriver.exe path
c.add_argument("--start-maximized")
c.add_argument("--auto-open-devtools-for-tabs")
c.add_experimental_option("excludeSwitches", ["enable-automation"])
c.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=c, executable_path=r'C:\Webdrivers\chromedriver.exe')
driver.get("https://www.mathsisfun.com/measure/mazes.html")



# Mode works for Everything Except Roads 
# hardButton = driver.find_element(By.XPATH, '//button[text()="Hard"]')
# hardButton.click()

# USER CHOOSES MODES (WORKS ON EVERYTHING EXCEPT ROADS)
# FOR SOME REASON DOUBLE DOTS AND BARRELS FAIL (REMOVE 1 TO THE HEIGHT OR WIDTH ONE OF THEM I FORGOT)


excelPath = r'C:\Users\S.Lin25\Downloads\MazeData.csv'
# checking to make sure the excel file is downloaded
while (not(os.path.exists(excelPath))):
    sleep(1)
    continue

# give time for user to close inspect element window
sleep(2)
df = pd.read_csv(excelPath, header = None)

w, h = df.shape[1], len(df)
print(df)
print(str(w) + " " + str(h))
walls = [[0 for x in range(w)] for y in range(h)] 
for i in range(h):
    for j in range(w):
        walls[i][j] = df.iloc[i, j]


# actual maze calculating algorithm


# 0 = no direction, 1 = up, 2 = down, 3 = left, 4 = right
directions = [[0 for x in range(w)] for y in range(h)] 
visited = [[False for x in range(w)] for y in range(h)]


queue = []
# (r, c)
queue.append((0, 0, 0))

# Simple BFS Algorithm
while (len(queue) != 0):
    first = queue[0]
    num = walls[first[0]][first[1]]
    queue.pop(0)
    
    if (visited[first[0]][first[1]]):
        continue
    visited[first[0]][first[1]] = True
    directions[first[0]][first[1]] = first[2]
    # if wall above is not present
    if (((1 << 3) & num) == 0):
        queue.append((first[0] - 1, first[1], 1))
    # if wall below is not present
    if (((1 << 2) & num) == 0):
        queue.append((first[0] + 1, first[1], 2))
    # if wall left is not present
    if (((1 << 1) & num) == 0):
        queue.append((first[0], first[1] - 1, 3))
    # if wall right is not present
    if ((1 & num) == 0):
        queue.append((first[0], first[1] + 1, 4))
    
curPos = (h - 1, w - 1)
listMoves = []
while (curPos != (0, 0)):
    listMoves.append(directions[curPos[0]][curPos[1]])
    # if moved up to reach spot, move down
    if (directions[curPos[0]][curPos[1]] == 1):
        curPos = (curPos[0] + 1, curPos[1])
    # if moved down to reach spot, move up
    elif (directions[curPos[0]][curPos[1]] == 2):
        curPos = (curPos[0] - 1, curPos[1])
    # if moved left to reach spot, move right
    elif (directions[curPos[0]][curPos[1]] == 3):
        curPos = (curPos[0], curPos[1] + 1)
    # if moved right to reach spot, move left
    elif (directions[curPos[0]][curPos[1]] == 4):
        curPos = (curPos[0], curPos[1] - 1)
listMoves.reverse()



translate = {1: Keys.ARROW_UP, 2: Keys.ARROW_DOWN, 3: Keys.ARROW_LEFT, 4: Keys.ARROW_RIGHT}
actions = ActionChains(driver)
for i in range(len(listMoves)):
    actions.send_keys(translate[listMoves[i]]).perform()
    sleep(0.1)

        
sleep(3)
driver.close()

# delete file


os.remove(excelPath)

