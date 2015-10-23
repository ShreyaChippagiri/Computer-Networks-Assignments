#UDP client program
import time
import sys, getopt
from socket import *
from datetime import datetime

#hard coding the values of the sender
serverPort = 12345
serverName = '127.0.0.1'
TIOUT = 5
window=0
npack=0

#ESTABLISHING THE CONNECTION
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.sendto('STARTING UDP CONNECTION - from sender\n\n', (serverName, serverPort)) #just to test

#TAKING NUMBER OF PACKETS AND WINDOW SIZE FROM THE RECEIVER
count=0
while count<2:
	recdMessage, serverAddress = clientSocket.recvfrom(2048)
	if count==0:
		window=int(recdMessage)
	elif count==1:
		npack=int(recdMessage)
	count=count+1
print "\nWindow size is : " + str(window)
print "Total number of packets to be sent are : " + str(npack)

sender = []
ackedpackets = []
ackedpacketslist = []
nosent = 0

data=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
def CalcCheckSum(seq,cha='\0'):
	sum=list(bin(ord(cha)+seq))
	return sum[-1]


winsize = {'base':0, 'end':window}
#creating the packets
print '\nAll the packets to be sent are :' 
for seqno in xrange(0,npack):
		if seqno % 26 == 0 : #when the alphabets are exhausted
			datano = 0
		packet=""
		packet=packet+str(seqno)
		packet=packet+','
		packet=packet+str(CalcCheckSum(seqno,data[datano]))
		packet=packet+','
		packet=packet+data[datano]
		datano=datano+1 
		sender.append(packet)
		print packet #printing all the packets that are to be sent 

sent = 1
flag=0

#SENDING PACKETS WITHIN A WINDOW
def SendData():
	global flag
	global sent
	global nosent
	global refertime
	while sent:
		if nosent in range(winsize['base'], winsize['end']):
		#size <window:	
			print '\nPacket being sent : ',nosent, 'Window = [',winsize['base'],',', winsize['end'],']'
			clientSocket.sendto(sender[nosent], (serverName, serverPort))	
			start = str(datetime.now())
			print 'Sent Following Packet: (',sender[nosent],') ,at Time:',start 
			nosent = nosent +1
		elif npack == winsize['end']:
			sent=0
		else:
			flag=0	
			print "\nWAITING for receive ack"
			RecvAck()

finish = 0
def RecvAck():
	global size
	global finish
	global refertime
	while finish == 0:
		socket.settimeout(clientSocket,TIOUT)
		try:
			reack=clientSocket.recv(2048)
			print '\n\nAck received as :  (',reack,')'
			strings=reack.split(',')
			seq=int(strings[0]) #checking the sequence number for which the ack is received successfully
			#if seq in range(winsize['base'], winsize['end']):
			print 'Recieved Ack For Seq No:',seq, 'at Time:',str(datetime.now())
			if strings[1] == '0':
				print '\nPACKET', seq, 'CORRUPTED!!'
			else:
				ackedpacketslist.append(seq)
				ackedpackets.append(reack)
				print 'WINDOW : [',winsize['base'],',', winsize['end'],']'
				print '\nPACKETS ack-ed as off now are : ',ackedpackets
				print 'SEQUENCE NUMBERS ackedpackets : ', ackedpacketslist
				while winsize['base'] in ackedpacketslist:
					print 'Moving the window'	
					winsize['base'] = winsize['base']+1
					winsize['end'] = winsize['end']+1
					flag =1	
				
			if (flag):
				print '\n SENDING again'
				SendData()
		except:
			print "TIMEOUT OCCURED!!!"
			break

SendData() #calling the function to start sending data
clientSocket.close()
