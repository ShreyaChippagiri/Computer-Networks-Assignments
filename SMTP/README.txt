ASSIGNMENT2-8

Problem statement:

Modify the A2-7 to send only one email in a connection but modify it to send attachments encoded as
base64.

(A2-7: develop a simple mail client that sends email to any recipient. Your client will need to connect
to a mail server, dialogue with the mail server using the SMTP protocol, and send an email message to
the mail server. Python provides a module, called smtplib, which has built in methods to send mail using
SMTP protocol. However, we will not be using this module in this assignment, because it hide the details
of SMTP and socket programming.

Note: Do not use smtplib or any other similar module. Client should be able to send multiple emails in a
single connection. Use the skeleton code from "Socket3_SMTP.pdf”)

A) Command Line Arguments:

In order to run the email client, 
1. Specify the command line arguments in the following way,

	$ python filename.py <IPaddress/servername><space><serverport>
	
	OR

	$ python filename.py <gmail-smtp-in.l.google.com><space><port number> 

(The servername is stored in sys.argv[1] and the server port is stored in sys.argv[2])

For example,

	i) if I want to connect to a system whose IP address is 127.0.0.1 and I want to use port 25 (all
	   TCP connections use port 25) I would type the following commands in the terminal,

	   $ python asn2.py 127.0.0.1 25

       ii) if I want to connect to the google mail server and I want to use port 25 (all
	   TCP connections use port 25) I would type the following commands in the terminal,

	   $ python asn2.py gmail-smtp-in.l.google.com 25

2. For "HELO:" command type your name and press enter. 

3. For "MAIL FROM:" command type <useridofsender@gmail.com> and press enter (<> is a must).

4. For "RCPT TO:" command type <useridofreceiver@gmail.com> and press enter (<> is a must).

5. Fllow the instructions that appear on the terminal.

6. To end your message type a period. 

7. For attachments, type in the entire path and press enter and then a period to end the message.


Modules and Packages Used:

1. sys
   The sys module provides access to some variables used or maintained by the interpreter and to
   functions that interact strongly with the interpreter.
   sys.argv is a list of command line arguments passed to the python script.

2. email package
   the email package is a library for managing email messages, including MIME and other message
   documents

   email.mime.base - This is the base class for all the MIME-specific subclasses of message.

   email.encoders - This is used to obtain a list of encoders

   email.MIMEMultipart - This is a base class for MIMEspecifications and adds Content-Type header
                       and MIME-Version header.

   email.MIMEText - This is a class for creating text type MIME documents.

   email.MIMEImage - This is a class for creating image type MIME documents.

3. socket
   This module gives access to the BSD socket interface. It provides the basic methods
   for creating a networking socket.


B) HOW THE PROGRAM WORKS:

The program begins by accepting the servername and the serverport number through the
command line arguments.
The servername is stored in sys.argv[1] and the server port is stored in sys.argv[2].

for example,
$ python asn2.py 127.0.0.1 25

The next step is to establish the TCP connection with the Server.
In order to do this, a client socket is created (clientSocket = socket(AF_INET, SOCK_STREAM)) The
parameters that are passed are AF_INET(indicates that the underlying network is using IPv4)and
SOCK_STREAM(this is the type of connection between the two end points, which is TCP).

The function, clientSocket.connect(servername,serverport)initiates the TCP connection. The
parameters are the address of the server side of the connection.

The method, clientSocket.recv(2048) receives the TCP message or the server response. 2048 indicates
the buffer size (in bytes). Then the program prints the response on the terminal.

The server responds via response codes. In case the server fails to respond while establishing the TCP
connection, error messages are printed on the terminal and the client is closed. The following code
prints the error message.

if recv[:3] != '220':
print '220 reply not received from server.'
exit(0)

Other server response codes include,
1. 250 - Requested action taken and completed.
2. 354 - Start message input and end with <CRLF>.<CRLF>. This indicates that the server is ready to
accept the message.
3. 221 - Service closing

After the TCP connection is established, the client responds with the HELO command, the MAIL FROM
command and the RCPT TO commands when the user can type in the respective details.
The raw_input() method was used to take in the user input.

Next, the DATA command is issued where the user is given an option to send either plain text or an
attachment(either an image or a text file).

How the attachments work:

A message object consists of headers and payloads. The payload is either a sting or a list of message
objects for MIME container documents (eg. Multipart) and the headers are field names and values.

msg=MIMEMultipart() indicates that the message's payload is a part of an aggregate of MIME message
objects.

The path of the document is taken in from the user.

In case of a text file, msg.set_payload(file(gh).read()) ensures that the payload is a string.

email.encoders.encode_base64(msg) encodes the payload to base64 form and sets the Content-
Transfer-Encoding header in to base64. This renders the content of the text file non-human readable.

a.append(msg.as_string()) Returns the entire message as a string and appends it to a[](a list that store
the input data).

msg.attach(MIMEImage(file(gh).read())) adds the given payload to the current payload which can have
nothing in it or if it contains a list of message objects.
the attach() constructor is used in places where the attachment is not just a string. We used attach()
because the client allows the user to attach images.

By typing a period the user can end the message and by pressing enter the user is allowed to send
another message.

By typing QUIT, the user can exit the email client. Before exiting the email client, the server responds
with one of its response codes (221).
