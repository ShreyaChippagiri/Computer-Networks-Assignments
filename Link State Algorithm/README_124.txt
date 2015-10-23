		----------------------------------------------------------------------------------------
					ASSIGNMENT #2 : LINK STATE ADVERTISEMENT
		----------------------------------------------------------------------------------------
Please accept our submission via e-mail as the server is down. 
-----------------------------------------------------------------------------------------------------------------------------------------------
__________________
 TEAM DETAILS
------------------
Zaina Hamid		1pi10is124
Surabhi Iyer		1pi10is109
Shreya Chippagiri	1pi10is134

__________________
 AIM
------------------
To implement Link State Advertisements and build a graph(matrix) using the LSA packets. With each receipt of link state advertisement, build the graph using link state advertisements.

__________________
 TO RUN
------------------
To run the program you have to enter the following command in each of the 'n' terminals. Where n=number of nodes in your graph

python ha2.py -i <node id> -t <timeperiod>  -e <edge costs in the form 3:1, 4:1, etc...> -n <total number of nodes>'

Please refer to the sample output at the end of this document.

Once you run this command in each of your terminals, You have 6 terminals each with the message : 
Hit Enter to begin sending and receiving messages!!
Hit Enter in each of these terminals and wait for about a minute or more.(until the cost matrix is the same on all the 'n' terminals)

ONLY when the cost matrix is the same across all 'n' terminals, press 'cntrl+c' in each of the terminals to stop sending and receiving at that node.

_______________________________
 UNDERSTANDING OF THE PROBLEM
-------------------------------

We are implementing Link State Advertisements, which basically means to communicate to my neighbors and every other node in my graph, through the link/s I'm immediately connected to by sending LSA packets.(Hence the name Link State) The link/s I'm immediately connected to also tells me which of the nodes are my immediate neighbors. To communicate I'm connected to my neighbor ports(calculated using neighbor:cost info given in the command line argument). We have 'n' number of terminals, bound to a port each.

We first start building the graph with our own information(entered through command line) for the edge costs from myself to my neighbors and back. This we call the initial matrix.

To enable us to send and receive packets simultaneously on the socket we use the select module has to be used. The socket is bound to MY port number, calculated as a base+ID of the node. (12340 + node ID in our case)

The user can send and receive packets at the same time:
At the RECEIVER's end
I receive the message from the socket and process(break, analyse, and update my matrix) this message only if it hasn't been received earlier.
The message is analysed, and from this message we extract the actual sender of the message, each of its neighbors, their respective cost and update the matrix with the cost values respectively.

At the SENDER's end
Firstly, for myself, a message is to be created, that may be circulated amongst all nodes in graphs. This message as mentioned is to be created with the values 'my node ID;number of my neighbors;time this msg is created;edge costs to my neighbors(1:2,3:4,...)'
Once this message is created, I broadcast this message to my immediate neighbors on the ports we calculated.
This message needs to be sent ONLY once to all my immediate neighbors.

Forwarding messages received
When I received messages, I would have stored them if they were unique. Each of these messages needs to be forwarded to all my neighbors, except the actual sender of the message. This enables nodes not connected to each other to update their matrices on the basis of messages being forwarded to them from their respective neighbors. 

Broadcasting my packets needs to be done periodically using a time interval, whose value we take in usign command line arguments.
We require identical cost matrices, at each of the 'n' terminals and ONLY then our program should stop. That is each node, should know the cost matrix for the entire graph.

_________________________
 ANALYSIS OF THE CODE:
-------------------------

1. Command line arguments are taken in. Incase of any error or incorrect input tags, an error message prompting you the right format is displayed and the program exits.
In case no arguments are specified, we use default arguments, but this will not work, as at each of the terminals the node ID is used to bind to a port, and its edge costs are needed. Hence distinct arguments have to be given for Node ID , and other input at the command line.

2. These command line arguments are then processed, formatted appropriately using lists, tuples and a dictionary. Hence, now we have extracted My node ID, processed my port number using my node ID(12340+nodeID), Neighbors and their edge costs as a dictionary, Total number of nodes in my graph and the time between sending intervals.

3. We then create a matrix 'mat' of the size 'nxn' which is first initialised to all zero values. Then using information of my immediate neighbors, and respective edge costs, we update and print this INITIAL matrix.

4. A list called 'neighbors' had been created, that maintains the ID of my immediate neighbors. This list is used to calculate a list of port numbers to which I should connect to (neighbor ID+12340). 'serverList' is the list that contains the port numbers of my immediate neighbors to whom packets are to be sent.

5. A client socket is created for a UDP connection and bound to my port number(myID+12340)

6. Using select module, under my while loop, I have two parts going on. 
	A. RECEIVING from other nodes 
	B. SENDING to other nodes
	
	A. RECEIVING from other nodes:
	Message from my neighbor is received on the port serverAddr[1] and it is stored in 'msg'. This msg is of the format 'my node ID;number of my neighbors;time this msg is created;edge costs to my neighbors(1:2,3:4,...)' and needs to be split with the delimiter as ';'. Once that is done we want to check if 'msg' has already been received. If to_proc[0] is in the list of senders 'senders' who have sent me messages no further processing goes on for this packet. Hence the excess time interval between the matrix display sometimes.

If the message is coming for the first time, we append its ID to the list 'senders' and append the 'msg' to the list 'messages' This is used in the sender part further below. 
We then extract neighbor & cost information for this message's actual sender, append these 3 values into a list by the name 'one' and use values from this list to update the matrix 'mat'. 'one' is a list that contains [actual sender, neighbor, cost]

This matrix 'mat' is then printed

	B. SENDING to other nodes - Under this there are two types. 1.When I broadcast to all my neighbors in the beginning & 2. When I forward messages/packets that I have received to all my neighbors except the actual sender of the message.

		1. Here we use the variable m, so that the initial message is created and broadcasted to all my neighbors exactly once. The packet is created in this format 'my node ID;number of my neighbors;time this msg is created;edge costs to my neighbors(1:2,3:4,...)'. To calculate time we use time.strftime("%I:%M:%S"), and have imported the time library. This message is then broadcasted to all my neighbors, whose port numbe ris in 'serverList'

		2. Here we send the unique messages stored in 'messages' one by one to all my neighbors(ports in 'serverList') except to the actual sender of the message. To make sure we don't send 'amsg' to the actual sender, we split it with ';' as a delimiter, and make sure we dont send it to the port number whose ID is rto_proc[0]. 


7. To allow the sender part to be executed at a time interval of every 't' seconds as mentioned in the command line, we use the fucntion 'time.sleep(t)' This makes sure there is a time interval of t seconds between every message being sent.

8. We then close the client socket.

______________________
  CHALLENGES FACED
----------------------

1. It was difficult to understand the idea of the select module, and analyse its working, and hence use it in our favor. My team mates had a clear idea, and they helped me understand it.

2. We had the idea clear in our mind, and our code seemed to show the same, but were trapped amongst silly logical errors for 2 days that led to incomplete output being displayed. We were not able to boil down to the exact point of the error, adnwe tried different methods of sending and receiving, but our result seemed to get more confusing. We finally went back to the second version of our code, and fixed it to work right. 

3. Even now the time taken to complete the calculation of final matrix is slightly more. You need to wait for about a minute or 2 and in the end before quitting ensure all the cost matrices are the same.

4. Working throught a series of splits, and lists gets confusing to analyse and update.

5. It took us some thinking and reading to do to understand why we could either use time.sleep of the timeout option of the select module.

6. The select module part, and the establishing the connection between the nodes was handled by Surabhi, and the logic of processing, formatting and updating the information was handled by Shreya and myself.

____________________
   SAMPLE OUTPUT
--------------------

Please open 6 terminals, and enter the following command into each one of them. The output needs to be checked on after a minute or so, to ensure the matrices displayed at all the terminals are identical.

python ha2.py -i 1 -t 5 -e 2:5,4:10 -n 6

python ha2.py -i 2 -t 5 -e 1:5,3:15,4:20 -n 6

python ha2.py -i 3 -t 5 -e 2:15,4:25,5:30 -n 6

python ha2.py -i 4 -t 5 -e 1:10,2:20,3:25,6:35 -n 6

python ha2.py -i 5 -t 5 -e 3:30 -n 6

python ha2.py -i 6 -t 5 -e 4:35 -n 6


In the end, you should have the following matrix displayed at all the 6 terminals. We have also added a snapshot incase of any confusion., The snapshot is under the name 'output.png'

	1  :  [0, 5, 0, 10, 0, 0] 

	2  :  [5, 0, 15, 20, 0, 0] 

	3  :  [0, 15, 0, 25, 30, 0] 

	4  :  [10, 20, 25, 0, 0, 35] 

	5  :  [0, 0, 30, 0, 0, 0] 

	6  :  [0, 0, 0, 35, 0, 0] 

Once you see the same output on all the 6 nodes, please press cntrl+c and end the program at each of the terminals to ensure no more sending/receiving of messages takes place.

_______________________________________________________________________________________________________________________________________________
-----------------------------------------------------------------------------------------------------------------------------------------------
