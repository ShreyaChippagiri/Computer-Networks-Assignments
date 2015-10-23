-----------------------------------------------------------------------------------------------------------------------------------------------
Please accept our submission via e-mail as the server is down. 
-----------------------------------------------------------------------------------------------------------------------------------------------
NAME: SURABHI R 

-----------------------------------------------------------------------------------------------------------------------------------------------
USN : 1PI10IS109

-----------------------------------------------------------------------------------------------------------------------------------------------
TEAM MEMBERS: 

ZAINA HAMID 	  - 1PI10IS124 
SHREYA CHIPPAGIRI - 1PI10IS134

-----------------------------------------------------------------------------------------------------------------------------------------------
PROBLEM STATEMENT: B1 

----------------------------------------------------------------------------------------------------------------------------------------------
EXECUTION: 

$python filename.py -i <host-node's id> -t <time of packet generation> -e <edge1:cost1,edge2:cost2,...> -n <total number of nodes> 

	 i = node id
	 t = time of this packet generation (keep time in 4byte unix time)
	 e = neighours containing the following information. 
	         1. neighbour id
	         2. cost of neighbour

	 n = number of neighbours


Example: 

Please execute the following commands on 6 terminals, and wait till you get identical matrices. Stop when all are same, using CNTL+C

	$ python ha2.py -i 1 -t 5 -e 2:5,4:10 -n 6

	$ python ha2.py -i 2 -t 5 -e 1:5,3:15,4:20 -n 6

	$ python ha2.py -i 3 -t 5 -e 2:15,4:25,5:30 -n 6

	$ python ha2.py -i 4 -t 5 -e 1:10,2:20,3:25,6:35 -n 6

	$ python ha2.py -i 5 -t 5 -e 3:30 -n 6

	$ python ha2.py -i 6 -t 5 -e 4:35 -n 6

-----------------------------------------------------------------------------------------------------------------------------------------------
UNDERSTANDING OF THE PROBLEM:

1. We need to implement Link State Advertisements and build  ONLY the network graph using these LSA packets. We intend to do this 
   using matrices.  

2. We need to be able to communicate with multiple nodes. In case of our assignment, each node is represented as a terminal/process. 
   Communication is via UDP. 

3. The select module has to be used because we need to send and receive on the same terminal. 

4. We need to be able to broadcast packets (from a node to its neighbours) periodically depending on the timeout value given by the user. 

5. The received information should be put into a matrix. 

6. The matrix should contain the information if its neighbours and it self. The information of the neighbours is ubdated dynamically
   as the advertisements are sent. If the node receives the same information for the second time, that information/packet has to be 
   dropped. If node1 receives information from node2 (and node2 is unaware of node1's neighbours), the message coming from node2 to 
   node1 is broadcasted to node1's neighbours.  

7. Case study: 

			    2
			A-------B 
			|       |
		      1 |	| 3       
			|	|
			D-------C
			    4 

  1. A, B, C, D start advertizing to its neighbours. For example A advertizes to B and D; B advertizes to C and A; etc.. 

  2. Say A sends a information(packet) about its neighbours to to B and D. B sends A's message to its neighbours except A. That is, it sends it
     to C. C updates information about A's neighbours in its own matrix. We are using a matrix to display messages in an understandable
     format.  

  3. Say, A sends the same information/packet again after the time period specified by the user(version 2). This will be dropped by B as it
     has previously received the message. 

  4. This happens at every node. This sequence stops when every node has information about every other node. i.e Every node's matrix is
     identical. 

  5. Sample matrix: 

			  A B C D
			A 0 2 0 1
			B 2 0 3 0
			C 0 3 0 4
			D 1 0 4 0

-----------------------------------------------------------------------------------------------------------------------------------------------
ANALYSIS OF THE CODE:

1. Command line arguments are taken from the user. Input validation is done so that an error message is printed when the wrong input is 
   entered. Default arguements are used in case no arguements are given. 

2. The information that is gathered from the command line arguements is first coverted into a list of lists, then to a list of tuples and 
   then finally to a dictionary. Key = nodeid, Value = cost. 

3. Finally, the host node's information is printed on the terminal. 

4. The port numbers that are assigned to the neighbours generated. By adding the nodeid to 12340.
   The rest of the port numbers aren't bound. The list of these port numbers is bound in the serverList.

5. A client socket is created and bound only to the first item in the list of port numbers. In case we bind all the port numbers, we 
   and error while running the program. 

6. A list of senders is maintained. This list contains a list of all the node id's from which the packet was received. 

7. A list of received messages is maintained in the messages list. The messages don't get appended to this list if it is being sent for the
   second time onwards. 

8. The flag m is maintained in order make sure that each of the nodes sends its information to all of the neighbours only once initially.

9. The message is formated accordingly. This is seen in the output. 

10. Explanation of the select module:  

	The select module waits for input from multiple sockets at the same time. Which only means that the server can handle multiple clients 		at the same time. The processing is done in such a way that the client requests behave in an interleaved fashion. 
	 - rlist is a list of socket objects waiting for the input. 
	 - wlist is a list of socket objects waiting for the output. 
	 - elist is a list of socket objects waiting for exceptions. 
	
	At the receiver side, 

	- First the select is called to wait for any input sockets that are ready. Then the data is received and processed. 
	- You have to first make sure that the packet has not been recieved before.  
	- If its a new message, then the martix is updated. 
	- The received message is then sent to its neighbours. This is the adverizing part. 
	- Please refer to the comments in the program for further clarity. 

	At the sender side, 

	- If  there is input from the keyboard, The system time is obtained and the message is broadcasted to its neighbours in a
          particular format.
	
	- time.sleep(t) is implemented to send the packet to its neighbours every 't' seconds. 


11. Finally, the client socket is closed.

-----------------------------------------------------------------------------------------------------------------------------------------------
MY CHALLENGES: 

There were several challenges that we faced in implementing this problem satement. 
1. It took me a while to understand what exactly was needed to be done. The matrix generation was a little complicated. Although with the
   help of my team mates I was successful in doing so. 

2. Next the method in which we could listen to and write to multiple ports was a problem. Using select module seemed to be the right 
   thing to do, although we had never implemented this in a python program before. 

3. The next challenge was using the select module. There were several examples available on the internet. I wasnt too sure which one to 
   refer to. Particularly, I found the following website useful, 
		http://ilab.cs.byu.edu/python/selectmodule.html

4. There were two ways of sending and receiving. 
	a. using only the input socket objects.  
	b. using the input and output socket objects.  

	Using the input object for reading and writing seemed to work for us. 

5. Next, There were several options or ways in which we could implement the timeout.
	a. Using the timeout option in select. 
        b. time.sleep() -- Although this has an effect of blocking. 
	c. Using time.time and comaring the time every 5 seconds. 

        I tried using the timeout option in select. It didn't work the right way. 
	We decided to stick with time.sleep(). 

6. I think the toughest part about this assignment was building the graph. Forwarding a message received by a node to it its neighbours
   was really difficult. We had understood how LSA works theoritically, but implementation took a while. 

7. Then we decided that as soon as you receive the packet, you had to send it. And the sender side had to handle broadcasting every "t"
   seconds, as specified by the user. 

8. It took us a while to properly format the matrix to print the result. 
-----------------------------------------------------------------------------------------------------------------------------------------------
THINGS UPLOADED: 

-output.png
-ha2.py
-README109.TXT 

-----------------------------------------------------------------------------------------------------------------------------------------------


