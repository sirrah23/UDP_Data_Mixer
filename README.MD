# UDP Data Mixer

This project is a little experiment with UDP.

There are two parts, the client and the server.

## Project Source
This project idea was obtained from & is described
[here](http://michael.dipperstein.com/mixer/mixer.html).

## Installation

Run `pip install -r requirements.txt`

## Server

You can start the server by running:

`python src/proxy <ip> <port>`

The proxy server starts up and listens for connections.
When clients connect they can send over matrices of data
to the server. 

Every X seconds the server mixes all of the data together
using a specified algorithm and stores it as a frame of data.

## Client

You can start a client by running:

`python src/client <# rows> <# columns> <server-ip> <server-port>`

The client is a front-end that shows the user a nxm matrix. It 
connects to the the proxy server and then every two seconds it 
generates/sends random binary matrices to the server for mixing.

The user can interact with the server by pressing the following keys:

* D to drop a packet
* S to skip a packet
* R to reverse sequence numbers for packets
