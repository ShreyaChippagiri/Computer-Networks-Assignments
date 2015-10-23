ASSIGNMENT 1
Name: Shreya Chippagiri
USN: 1PI10IS134


Team Members: 
Zaina Hamid(1PI10IS124)
Surabhi Ravishankar (1PI10IS109)
______________________________________________________________________________________________________________________________________________

COMMAND LINE ARGUEMENTS TO RUN THE CODE: 

To run the code, open three terminal screens either in three different computers or in the same system. The method to run both the mentioned methods is as follows:

THREE CONSOLES ACROSS THREE DIFFERENT SYSTEMS(different IPv6 addresses)

Type the command as follows:

python asn1.py -n <Your Name> -a <Your ipv6 address to be used by this program>  -p <Your port number on which this program will receive chat msgs from others> -d <The ipv6 address of 2nd party>,<The ipv6 address of 3rd party> -r <port number of 2nd party>,<port number of 3rd party>'

Sample : python asn1.py -n Shreya -a fe80::52e5:49ff:fe1b:f172 -p 12222 -d fe80::52e5:49ff:fe1b:f182,fe80::52e5:49ff:fe1b:f139 -r 13333,11111

Where 
-n : Shreya 							My name
-a : fe80::52e5:49ff:fe1b:f172	 				Current running system's IPv6 address
-p : 12222							Port number bound to my system
-d : fe80::52e5:49ff:fe1b:f182,fe80::52e5:49ff:fe1b:f139	IPv6 addresses of the other 2 systems
-r : 13333,11111						Port numbers the other 2 systems are bound to

This same command has to be run in the other 2 consoles, by changing the IPv6 address and port number of the host system, and the IPv6 address and port numbers of the other 2 parties you are connecting to.

THREE CONSOLES ON THE SAME SYSTEM (loopback addresses)

Type the command as follows:
python asn1.py -n <Your Name> -a <Your ipv6 address to be used by this program>  -p <Your port number on which this program will receive chat msgs from others> -d <The ipv6 address of 2nd party>,<The ipv6 address of 3rd party> -r <port number of 2nd party>,<port number of 3rd party>'

Sample : python asn1.py -n Shreya -a ::1 -p 12222 -d ::1,::1 -r 11111,13333
Where 
-n : Shreya 		My name
-a : ::1		Current running system's IPv6 address(LOOP BACK)
-p : 12222		Port number bound to my system
-d : ::1, ::1		IPv6 addresses of the other 2 consoles, on the same system(LOOP BACK)
-r : 13333,11111	Port numbers the other 2 consoles are bound to

This same command has to be run on the other 2 consoles in the same system, hence we use the loopback address(::1) as the destination adress of both the other systems. The only thing that we need to change in the name of the user and The port number. 

INCASE YOU RUN THE CODE WITHOUT ANY ARGUMENTS:

In this case the program will use the default values, however connectivity wont be established, and the default portnumber value will be used for the three consoles, which does not let the program be successfull. Hence give command line arguments in the right format

INCASE WRONG COMMAND LINE ARGUMENTS ARE GIVEN:

If we use any other character while giving the command line arguments, instead of n,a,p,d,r : The program assumes the user needs help, displays the message asking the user to run the program with the command line arguments in the right format, and exits.

______________________________________________________________________________________________________________________________________________

PROBLEM STATEMENT: B1 

Implement 3-party chat using UDP based on IPv6. For the program specify the command 
line arguments as follows 
    -n <name of chatter> 
    -a <ipv6 address to be used by this program> 
    -p <port number on which this program will receive chat msgs from others> 
    -d <ipv6 address of 2nd party>,<ipv6 address of 3rd party> 
    -r <port number of 2nd party>,<port number of 3rd party> 
The program will receive inputs on command line and send the same to other chat partners. 
When the program receives the input from other chat partners, it should display the same on 
console along with its id. 

______________________________________________________________________________________________________________________________________________

UNDERSTANDING THE PROBLEM STATEMENT: 

From what I have understood. The program has to behave like a sender and a receiver at the same time to send and receive messages. 
The messages that are being sent from one computer should be broadcasted to two other computers. 
This can be achieved by creating two functions, 
	1. server funciton	
	2. client function 

The server function is responsible for displaying messages that are sent from other computers or users. 

The client function is responsible for sending messages to the other computers (users). 
The server and the client function should behave in an interleaved fashion. So threading was used. 

The port numbers and the IPv6 addresses have to interchanged for each user. 

The program should run in three different terminals in three different computers. 
______________________________________________________________________________________________________________________________________________

APPROACH:  
First we programmed a udp client  and then a udp server. We made sure that it worked for Ipv6. 
After a bit of reading, we realized that the only difference between ipv6 and ipv4 is that we had to change, 
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
to, 
sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)

Another difference was that, the loopback address was “::1”. 

After we got the UDP client and server programs communicating with each other, our next step was to combine the client and server program into a single program. To achieve this we wrote the client and server programs in two separate functions. 

The client sends messages and the server receives them. 

We used command line arguments so that the user can input their desired source and destination ports. 

Please note that there was no point in setting the default values of the command line arguments because we have to keep changing the port numbers all the time.
______________________________________________________________________________________________________________________________________________

ANALYSIS OF THE CODE: 

In first few lines of code, the default values for, 
	1. name (Name of current chatter) 
	2. ipv6addr (ipv6 address to be used by this program) 
	3. portno  (port number on which this program will receive chat messages from others) 
	4. ipv6party  (ipv6 address of 2nd Chatter/Party,ipv6 address of 3rd Chatter/party)
	5. portparty (port number of 2rd Chatter/party,port number of 3rd Chatter/party)
	   was taken. 
	ipv6party and portparty is a list containing two elements. 

	The command line arguments also allow the user to enter in their own values. The code was the same was entered. And in case there were 		any errors in the command line arguments we terminate the program and give the user instructions on how to run the program. 

Next is the CLIENT FUNCTION. 
	This part of the code contains the client part of the code that is used to send the data. In this function, the message to be sent is 		taken as a raw input. 

	send_addr1 = (ipv6party[0],int(portparty[0]),0,0)
	send_addr2 = (ipv6party[1],int(portparty[1]),0,0) 

	Set the address, and port number of the respective party to chat with in a tuple. 

	sock.sendto(name+': '+MESSAGE, send_addr1)
	sock.sendto(name+': '+MESSAGE, send_addr2)		

	Sends the message to the respective party along with the name. 

	When the user enters ‘end’, a message saying “Party1 Exited the Chat’ is sent to the other two parties and the socket is closed. Any 		further messages aren’t sent to the other 2 parties. 

Next Is the SERVER FUNCTION. 
	This part of the code deals with receiving the messages from the other  two parties. 
	sock.recvfrom(1024) 
	Receives the UDP message. And the buffer is 1024. 

Next is the MAIN. 
	After taking the command line arguments from the user, this part of the code is entered. Here,  


	sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) creates a socket. 
	AF_INET6 indicates IPv6 transport mechanism. SOCK_DGRAM indicates the socket type which is datagram. 

	sock.bind(('',portno))  this method binds the address to the socket. This binding takes place for the current user and the current port 	number. 

	Lastly, the threads are spawned.

	threading.Thread(target = server).start()	
	threading.Thread(target = client).start()

	One thread is spawned for the server function and the other thread is spawned for the client function. They are executed in an 		  interleaved fashion. This enables the program to send and receive the messages to and from multiple clients. 

______________________________________________________________________________________________________________________________________________

CHALLENGES FACED: 
	1. There were several challeges that we faced. Most of the time we didnt get the output that we expected. We had to use a trial and 		   error method in order to solve them. It was time consuming. 
	2. I using getaddrinfo() in order extract the IPv6 address. It was giving me errors while binding it. 
	3. There was an issue in the python program when I tried splitting the command line arguements. So I had to use a slightly 
	   more complicated method to do that. 
	4. I tried using the select module to write this program and I wasnt able to get the desired output. 
	   So I started from scratch and figured out that threading can also be used. The program started responding the way I wanted it to.  
	5. After alot of trying I learnt that the binding of the socket required a tuple to be passed as a parameter. This was rather a  		   careless mistake. 
	6. This was rather a simple program. I feel that it took us more time than required to figure this out. We could have finished the 
	   program a lot sooner. 
	7. The fact that we couldn't test this program at home due to lack of computers was a problem. I tried to get this to work by installing
	   ubuntu in virtual box and using a bridged network in order to get a sperate ip address for the virtual machine. 
______________________________________________________________________________________________________________________________________________

OUTPUT: 
The screenshot of the output accross three systems has been attached with the name asn1_comp1.png, asn1_comp2.png and asn1_comp3.png.
The screenshot of the output in the same system while using three different consoles has been attached with the name loopback.png
Please view the same if needed.

We got the following result on the screen in each of the three computers. 

OUTPUT on SURABHI's PC: 

pesit@pesit-To-be-filled-by-O-E-M:~$ python asn1.py -n Surabhi -a fe80::52e5:49ff:fe1b:f139 -p 11111 -d fe80::52e5:49ff:fe1b:f172,fe80::52e5:49ff:fe1b:f182 -r 12222,13333
	-----------------------------------------------------------------------------------------
WELCOME TO 3-PARTY IPv6 CHAT
	-----------------------------------------------------------------------------------------
My Name:  Surabhi
My IPv6 Address:  fe80::52e5:49ff:fe1b:f139
My port number:  11111
IP address of Second Party: fe80::52e5:49ff:fe1b:f172
IP address of Third Party: fe80::52e5:49ff:fe1b:f182
Port of First Party:  12222
Port of Second Party:  13333
	-----------------------------------------------------------------------------------------
	-----------------------------------------------------------------------------------------

Lets Begin chatting, Enter your message or wait for one!!!

HEllo :)
received message: Zaina: HI there
received message: Shreya: How do you do?
Want to exit? type exit
exit
Sorry, type end
end

OUTPUT ON ZAINA'S PC: 
pesit@pesit-To-be-filled-by-O-E-M:~$ python asn1.py -n Zaina -a fe80::52e5:49ff:fe1b:f172 -p 12222 -d fe80::52e5:49ff:fe1b:f182,fe80::52e5:49ff:fe1b:f139 -r 13333,11111
	-----------------------------------------------------------------------------------------
WELCOME TO 3-PARTY IPv6 CHAT
	-----------------------------------------------------------------------------------------
My Name:  Zaina
My IPv6 Address:  fe80::52e5:49ff:fe1b:f172
My port number:  12222
IP address of Second Party: fe80::52e5:49ff:fe1b:f182
IP address of Third Party: fe80::52e5:49ff:fe1b:f139
Port of First Party:  13333
Port of Second Party:  11111
	-----------------------------------------------------------------------------------------
	-----------------------------------------------------------------------------------------

Lets Begin chatting, Enter your message or wait for one!!!

received message: Surabhi: HEllo :)
HI there   	
received message: Shreya: How do you do?
received message: Surabhi: Want to exit? type exit
received message: Surabhi: exit
received message: Surabhi: Sorry, type end
end


OUTPUT ON SHREYA’s PC

pesit@pesit-To-be-filled-by-O-E-M:~$ python asn1.py -n Shreya -a fe80::52e5:49ff:fe1b:f182 -p 13333 -d fe80::52e5:49ff:fe1b:f139,fe80::52e5:49ff:fe1b:f172 -r 11111,12222
	-----------------------------------------------------------------------------------------
WELCOME TO 3-PARTY IPv6 CHAT
	-----------------------------------------------------------------------------------------
My Name:  Shreya
My IPv6 Address:  fe80::52e5:49ff:fe1b:f182
My port number:  13333
IP address of Second Party: fe80::52e5:49ff:fe1b:f139
IP address of Third Party: fe80::52e5:49ff:fe1b:f172
Port of First Party:  11111
Port of Second Party:  12222
	-----------------------------------------------------------------------------------------
	-----------------------------------------------------------------------------------------

Lets Begin chatting, Enter your message or wait for one!!!

received message: Surabhi: HEllo :)
received message: Zaina: HI there
How do you do?
received message: Surabhi: Want to exit? type exit
received message: Surabhi: exit
received message: Surabhi: Sorry, type end
end

________________________________________________________________________________________________________________________________________________


