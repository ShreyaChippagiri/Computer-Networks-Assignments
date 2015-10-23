NAME:Shreya Chippagiri
USN:1PI10IS134
TEAM MEMBERS:Surabhi.R-1PI10IS109
             Zaina Hamid-1PI10IS124

PROBLEM STATEMENT:
B1. Implement Link State Advertisements and build network graph using this LSA packets.
With each receipt of link state advertisement, build the graph using link state advertisements.
The command line params could be as follows:
-i <nodeid>
-t <periodic broadcast time period>
-e <edge costs>.
Example: For node 3, program should be invoked as
./ha1 -i 3 -e 2:1,4:1,5:2,6:7
The link state packet contain following information:
i) node id
ii) time of this packet generation (keep time in 4byte unix time)
iii)number of neighbours
iv) for each neighbour
a) neighbour id
b) cost of neighbour
A node when receives such an LSA will forward to all other neighbours provided this has
already not been done for this neighbour. Thus, each node should store this information in the
memory. 

UNDERSTANDING OF THE PROBLEM:
The problem statement requires us to implement Link State Advertisements and ONLY build the network graph using these LSA packets.The problem requires us to be able to communicate with multiple nodes(in this case processes,i.e,multiple terminals).Since we have to both send and receive packets on the socket,select module has to be used.Broadcasting of packets needs to be done periodically by maintaining a timeout.The obtained information should be rightly formatted into a matrix form.This way each node maintains a record of the graph initially ,one that it sends by itself and updates it subsequently.Each node broadcasts information about the node it is connected to ,to each of ITS NEIGHBOURS ONLY.Additionally,each node also has to broadcast the information received from its neighbour to all of its other neighbours excepting the one it received from.Also,if the obtained information is already present,it has to be discarded else updated in the matrix maintained by each of the nodes.

ANALYSIS OF THE CODE:

The code works in the following order:

1.Command line arguments are taken and in case of wrong inputs,an error message with the right format is displayed and the program exits.In case no arguments are specified,the default arguments are taken.The command line arguments are given as ,for example:python CNA2_v31.py -i 1 -t 5 -e 2:10,4:20 -n 4
2.The obtained command line arguments are processed,formatted appropriately using tuples and dictionary to be maintained in a matrix.Each of the host node's information is displayed.
3.A list called neighbors is maintained that contains the id of the neighbour node. The port numbers to which the packets have to be sent is maintained in the serverList.The node id added with 12340 gives the port number.Thus the last digit identifies the node for future convenience.
4.A client socket is created for a UDP connection and bound.
5.A list of senders is maintained that contains the node ids of those neighbours from which we have already received packets.A list of received messages is maintained in messages.Only if a message not already received from a node id is appended to the messages list and the corresponding node id to the senders list.
6.The obtained message in the format:node id;no of its neighbours;time;edge:cost is then formatted in the order 'sender node id,neighbour node,edge cost'and maintained in the matrix.The matrix is printed.
7.A flag m is kept to ensure that each of the nodes send its own data to all of its neighbours only once initially.The packet is sent in the format:node id;no of its neighbours;time;edge:cost.Time t is the time of the packet generation given by:t = time.strftime("%I:%M:%S").
8.The packet each node receives from its actual sender is then forwarded to all of its neighbours other than the actual sender.
9.The client socket is then closed.

