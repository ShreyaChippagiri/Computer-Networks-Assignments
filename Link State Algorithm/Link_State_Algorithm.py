import socket
import string
import random 
import sys, getopt
from socket import *
from select import *
from sys import *
import time

#Declaring command line arguments and giving them default values
i = 1			#<nodeid> 
t = 1			#<periodic broadcast time period> 
e = "1:1,2:4,3:2,5:7"	#<edge costs>
n = 10 			#number of nodes
ip_addr = '127.0.0.1'	#loopback address
oplist = ["-i","-t","-e","-n"]

m = 1			#usage explained below - while sending

#to take the command line arguments
try:
	opts, args = getopt.getopt(sys.argv[1:],"i:t:e:n:",["nodeid=","time=","edgecost=","nonodes="])
except getopt.GetoptError: #incase of error 
	print 'ERROR, Please follow the following format : '
	print '\nasn2.py -i <node id> -t <time>  -e <edge costs in the form 3:1, 4:1, etc...> -n <total number of nodes>'
  	sys.exit()

#assigning values to variables
for opt, arg in opts:
    	if opt not in(oplist):
		print 'ERROR, Please follow the following format: '
		print '\nasn2.py -i <node id> -t <time>  -e <edge costs in the form 3:1, 4:1, etc...> -n <total number of nodes>'
     		sys.exit()

      	elif opt in ("-i", "--nodeid"):
        	i = int(arg) 
      	elif opt in ("-t", "--time"):
        	t = float(arg)
      	elif opt in ("-e", "--edgecost"):
        	e = arg.split(',')	#storing the edges as elements of a list e(each element's format is - 'neighbor:cost')
		edges = arg
      	elif opt in ("-n", "--number"):
        	n = int(arg) 

l1 = [] 
l2 = [] 
neighbors = []

#spliting the colon between the neighbor and the cost. Storing this as a list 'sp', and then appending each of these lists into l1.
for item in e: 
	sp = item.split(':')
	neighbors.append(sp[0])
	l1.append(sp)	#l1 is a list of lists

#Converting the above result into a tuple of tuples. 
tuple_of_tuples = tuple(tuple(x) for x in l1)

#Converting the above tuple of tuples in to a list of tuples to convert to a dictionary further
for item in tuple_of_tuples: 
	l2.append(item)

#converting a list of tuples into a dictionary
#dictionary where key is the neighbor, and value is the edge cost
d = {} 
d = dict(l2)

print '\n\t___________________________________________________'
print '\t\t    WELCOME TO LINK STATE'	
print '\t---------------------------------------------------'
print '\t\tMy Node id: ', i      			# <Name of current chatter> 
print '\t\tMy IP Address: ',ip_addr   			#<ipv6 address to be used by this program> 
print '\t\tMy port number: ',int(i)+12340		# <port number on which this program will receive chat msgs from others> 
print '\t\tEdges: ', d
print '\t\tNumber of Nodes: ',n
print '\t\tTime interval: ',t
print '\t___________________________________________________'
print '\t---------------------------------------------------'


#creating a nxn matrix to be updated
mat = [[0 for s in range(n)] for j in range(n)]	

#Updating the matrix with initial values, MY neighbors' edge costs
for key in d:
	mat[i-1][int(key)-1] = int(d[key])	#-1 for all indeces because matrix starts from 0th index, but neighbors are natural numbers
	mat[int(key)-1][i-1] = int(d[key])	#if 1 is the cost from node a to b, cost from b to a is also 1. hence invert the indeces

for s in range(n):
	print "\t",s+1, " : ", mat[s], "\n"	#printing the initial matrix.

serverList = [] #will contain port numbers 
for neigh in neighbors:
	box = 12340 + int(neigh)		#port number of each neighbor is 12340 + node ID	
	serverList.append(box)

print '\nNeighbor ports : ',serverList				#printing my neighbor ports.
	
servername = '' 
sockList = [] 
sockList.append(sys.stdin)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('', int(i)+12340))
sockList.append(clientSocket)

print "Hit Enter to begin sending and receiving messages!!" 

senders = []	#to store node IDs sending me messages
messages = []	#to store unique messages I receive from neighbors

while True:
    rlist, wlist, elist = select(sockList, [], sockList)
    if not (rlist, wlist, elist):
        print "No socket ready for any operation!!\n"
    for rsock in rlist:
        if rsock == clientSocket:
	    to_proc = []	#list to store parts of message received
	    to_proc1 = []	#list to store neighbor:cost values

	    #RECEIVING DATA
            msg, serverAddr = rsock.recvfrom(2048)
            print "From ", serverAddr[1] ,", received data: ", msg, "\n"

#message received is of the format 'actual sender;number of its neighbors;time it was created;edge costs for its neighbors(a:1,b:2)'

	    #PROCESSING RECEIVED DATA
	    to_proc = msg.split(';')
	    if to_proc[0] not in senders: #Processing only for messages that we receive the first time. to_proc[0] - ID of the actual sender
		messages.append(msg)
		senders.append(int(to_proc[0]))
		to_proc1 = to_proc[3].split(',')	#proc 1 contains all the 'neighbor:cost' for the node to_proc[0](actual sender of msg)
		for zee in to_proc1:	#each 'neighbor:cost'
			one = []	#a list that stores a pair of nodes, & the edge cost between them:[actual sender, neighbor, cost]
			one.append(int(to_proc[0]))
			one.append(int(zee.split(':')[0]))
			one.append(int(zee.split(':')[1]))		
			mat[one[0]-1][one[1]-1] = one[2]	#updating my matrix as explained above
			mat[one[1]-1][one[0]-1] = one[2]	#inverting the indeces

		for s in range(n):
			print "\t",s+1, " : ", mat[s], "\n"	#printing the matrix

        if rsock == sys.stdin:
	    #SENDING/BROADCASTING THE FIRST MSG(its own data) TO ITS NEIGHBORS
            if m == 1:
		m=0 # so that I send my initial msg only once
		tim = time.strftime("%I:%M:%S")
		message = str(i)+";"+str(len(neighbors))+";"+tim+";"+edges	#creating my message to be sent
		for z in range(len(serverList)): 
		     clientSocket.sendto(message, (servername, serverList[z]))	#sending this message to all my neighbors

	    rto_proc=[]			#to store parts of the message that we forward
	    for amsg in messages:	#amsg is each of the messages that we have uniquely received.
		    rto_proc = amsg.split(';')
		    for z in range(len(serverList)):	#for each of the neighbors
			if int(rto_proc[0]) != serverList[z]-12340: # to check the msg of the actual sender(rto_proc[0]) doesn't go back to it
				clientSocket.sendto(amsg, (servername, serverList[z]))

	    time.sleep(t) 	
clientSocket.close()

