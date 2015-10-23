import sys
import email,email.encoders,email.mime.base
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from socket import *
# Choose a mail server (e.g. Google mail server) and call it mailserver

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
recv = clientSocket.recv(2048)
print recv

#220 server response code indicates that the SMTP server is ready. An error message is printed otherwise. 
if recv[:3] != '220':
    print '220 reply not received from server.'
    exit(0)

#Send the Helo command and print the server response
heloCommand = 'HELO '+raw_input("HELO:")+'\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(2048)
print recv1

#250 server response code indates that the requested action has taken place and is complete. An error message is printed othewise.
if recv1[:3] != '250':
    print '250 reply not received from server.'
    exit(0)
t=1
b=1
while t:
	#The following segment of code sends "MAIL FROM" command and prints the server response
	mail_from = 'MAIL FROM:'+raw_input("MAIL FROM:")+'\r\n'	
	clientSocket.send(mail_from)
	recv1 = clientSocket.recv(2048)
	print recv1
	#The following segment of code sends "RCPT TO" command and prints the server response
	rcpt_to = 'RCPT TO:'+raw_input("RCPT TO:")+'\r\n'
	clientSocket.send(rcpt_to)
	recv1 = clientSocket.recv(2048)
	print recv1
	#The following segment of code sends "DATA" command and prints the server response. An option to send and attachement is also given 
	print 'DATA:\r\n'
	print 'Type att to send an attachment\n'
	print 'Type . to end your message\n'
	DataCommand = 'DATA\r\n'
	clientSocket.send(DataCommand)
	recv1 = clientSocket.recv(2048)
	print recv1
	a=[]
	while b:
		mes=raw_input()
		if mes!='.':
			#In case the user decides to send an attachment the following action is taken. The attachement can be a textfile or an 				image
			if mes=='att'or mes=='ATT':
					print 'Type 1 to send a .txt file\n'
					print 'Type 2 to send a .png file\n'
					gh=raw_input()
					#incase the user wants to send a *.txt file
					if gh=='1':
						msg = MIMEMultipart()
						print 'Type the complete path of your file including your file name'
						gh=raw_input()
						msg.set_payload(file(gh).read())
						email.encoders.encode_base64(msg)
						a.append(msg.as_string())
					#incase the user wants to send a *.png file					
					else:
						msg = MIMEMultipart()
						print 'Type the complete path of your file including the extension'
						gh=raw_input()
						img = MIMEImage(open(gh,"rb").read(), _subtype="png")
						img.add_header('Content-Disposition', 'attachment; filename="test image"')
						msg.attach(img)
						a.append(msg.as_string())
			#Else case where the user decides to send a plain message which is to be typed in the terminal			
			else:
				a.append(mes)
		#The following segment of code indicates the action to be taken when the user ends the message with a period		
		if mes=='.':
			message='\n'.join(a)
			clientSocket.send(message+'\r\n'+'.\r\n')
			recv1 = clientSocket.recv(2048)
			print recv1
			a=[]
			b=0
	print 'press enter to send another mail or type quit'
	d=raw_input()
	#The user should enter quit to exit the mail client
	if d=='quit'or d=='QUIT':
			t=0
			b=0
	else:
			t=1
			b=1		      
#The following segment sends the quit command to get the server response
heloCommand = 'QUIT\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(2048)
print recv1
#Close the TCP connection
clientSocket.close()
