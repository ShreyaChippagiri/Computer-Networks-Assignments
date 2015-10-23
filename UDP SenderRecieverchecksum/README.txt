____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
GROUP MEMBERS: 
Surabhi R (USN-1PI10IS109)
Zaina Hamid (USN-1PI10IS124)
Shreya C (USN-1PI10IS134)

The assignment was done in collaboration with the following members: 
Abeer(USN-1PI10IS121)
Aishwaryia(USN-1PI10IS078) 
____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
HOW TO COMPILE AND RUN THE PROGRAM: RECEIVER
In order to compile the program type the following command in the terminal: 

1. user@ubuntu:~$ python asn3.py -N 10 -s 30 -p 12345 -w 3 -r 20
OR 
2. user@ubuntu:~$ python asn3.py --numpak 10 --ackperc 30 --portno 12345 --winsize 3 --packper 20
OR 
3. user@ubuntu:~$ python asn3.py 

where,
	-p: (UDP) server port number.
    	-s: Corruption percentage of acks sent.
    	-r: Corruption percentage of packets received.
    	-N: total number of packets to be received (minimum of 10)
    	-w: window size

The commandline arguements can be specified in any order. The commandline arguements need not be specified(3rd Case), in which case the hard coded default values are used. 
Incase any of the values are missing or the number of packets is less than 10, the program exits, and needs to be re-run in the same way as mentioned above.
____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULES IMPORTED: 
1. import sys
This module provides a number of functions and variables that can be used to manipulate different parts of the Python runtime environment.
The module was mainly used to implement the commandline arguements 

2. import string
The string module contains a number of useful constants and classes, as well as some deprecated functions that are also available as methods on strings.
This module was used as there were some functions in the program that was performed on strings. 
 
3. import socket
This module implements an interface to the socket communication layer. The client and server sockets were created using this module.

4. import random
This module was imported to generate a random list of numbers to identify which packet/ack to corrupt.

5. import datetime 
This module was imported to print the system time during the execution of the program. 
____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
DESCRIPTION OF THE PROGRAM: 

First the program takes the commandline arguements provided by the user and prints it on the screen. We validated the input so that the user does not make any mistake in giving the input. 
You can type, 
user@ubuntu:~$ python asn3.py -h in case he/she does not know how to enter the commandline arguements - HELP. 
The values are hardcoded to choose default values incase the user does not choose to provide the input values. 

Then the list of packets(sequence numbers) that are to be corrupted before the receiver accepts and stores them are generated. This is done by generating a list of random numbers that serve as the sequence number of the incoming packets that are to be corrupted. The number of packets in the list to be corrupted is calculated according to the value (in percentage) given by the user or 20% by default. The checksum for each packet that has been corrupted is changed to zero. 

Next, the list of packets whose acks are corrupted when the receiver responds is generated. This is done by generating a list of random numbers among the packets that have been successfully received. This list of random numbers serves as the sequence number of packets whose ack has to be corrupted. The number of elemets in the list is calculated according to the value (in percentage) given by the user or 30% by default. The checksum for each ack that has been corrupted is changed to zero. 

The receiver then establishes a connection with the client via port 12345 by default or the port specified by the user. Once the connection is made, the sender starts sending the packets to the receiver. Before that, the receiver sends to the sender the window size and the expected number of packets (as mentioned in the question). 

Once the sender starts sending the packets, the receiver needs to accept them so long as the packet is not corrupt. This is handled in the while loop. The packet (in the form of the 'message' that has been received) is split into three parts (sequence number, checksum, data). 
if the checksum has not been changed to zero(packet not corrupted), the ack for the packet is not to be corrupted and the packet has been received, the sequence number and the checksum is sent to the client/Sender from the receiver (the sendingack() function is called). 
 
The packets that are corrupted are added to the 'corruptedlist' otherwise, the packets are added to the 'receivedpacketslist'. 

We also have a function called 'sendingack()'. This fuction is to send the ack back to the sender for all the packets that the receiver has received(Including corrupted and non corrupted acks). The ack packet contains the : "sequence number, checksum". This function is called everytime the packet arrives the receiver end. 
At the sender end the incoming ack is split to check the checksum. 

Finally, the main fuction in which all the code resides is called. The command line arguements are passed as parameters to the main. 
____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
HOW TO COMPILE AND RUN THE PROGRAM: SENDER : python asn3_sender.py

FORMAT OF THE INPUT : We have hardcoded the values of the server port, ServerName, and Timeout. The values for the window size and the total number of packets are received from the Receiver/Server, which have been inturn accepted from the command line argument.
____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

DESCRIPTION OF THE PROGRAM : The SR Sender code has been developed by us to test our RECEIVER program with the checksum logic taken from Abeer's and Aishwarya's code. Our sender code works perfectly only when paired up against our receiver code. 

We haven't handled Re-transmission in the sender code, However if packets are re-transmitted by the sender, the receiver will now accept the packet successfully, and re-send the ack for that packet, while displaying the message : 
Packet number : x has been received "AGAIN" as a result of retransmission! At the time : ',str(datetime.now())

Once the connection is established, we are sending a test message to the receiver before sending the packets. We then receive the number of packets and the window size inorder to create packets to be sent, and send the same within the range of the window.
Using the total number of packets, we create the packets with the format "sequence_number, checksum, data" and add them to the list of packets to be sent.

The SendData() function is called, that starts sending packets that are within the range of window. The window will not move forward until it receives/has already received the ack for the packet at the base of the window. If the packet to be sent is not in the window, we wait till the ack for the base is received, and call the function RecvAck()

In the function RecvAck(), we receive the ack packet from the receiver that has the format "sequence_number, checksum"
If the checksum value has been modified to '0' - We consider the ack packet to be corrupted and display the message PACKET x CORRUPTED!!
If the checksum value has not been modified, we add this sequence number to the list of packets that have been sent successfully(ack received) and move the window's base to the next unacked/untransmitted packet.
The movement of the window means the sender can continue sending packets and the SendData function is called again.

This process, oscillation between the sender and the receiver function continues till the window is stuck at a position(as we have not considered re-transmission)
Re-Transmission, when the packets are sent again, will be received successfully and ack-ed successfully. 

CHALLENGES FACED - Working on the sender and receiver code to match each other, was very difficult. It took us time to understand the flow, while coding the same in python - translating our thoughts into code was even tougher. There were several minute details that we had to make sure were handled, which otherwise would lead to errors that were very difficult to debug.
____________________________________________________________________________________________________________________________________________________________________
--------------------------------------------------------------------------------------------------------------------------------------------------------------------


Thankyou


 
