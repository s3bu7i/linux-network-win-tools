
# Advanced TCP Chat Server and Client

This project is an advanced implementation of a TCP chat server and client in Python. The chat server allows multiple clients to connect and communicate with each other. Clients can send public messages, private messages, and use special commands such as listing connected users and quitting the chat.

## Features

- **Multiple Clients**: The server supports multiple client connections at once.
- **User Nicknames**: Clients must choose a unique nickname when joining the chat.
- **Public Messaging**: Messages sent by a client are broadcasted to all connected clients.
- **Private Messaging**: Clients can send private messages to specific users.
- **Command Handling**: Clients can use commands like `/list` to see online users and `/quit` to leave the chat.
- **Graceful Disconnection**: When a user disconnects, other clients are notified, and the server handles it gracefully.

## Requirements

- Python 3.x

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tcp-chat-app.git
cd tcp-chat-app
```

### 2. Install Requirements

There are no external dependencies required for this project beyond Python's standard library.

### 3. Running the Server

To start the chat server, run the following command in a terminal:

```bash
python server.py
```

The server will start listening for incoming client connections on `localhost:12345`.

### 4. Running the Client

To connect a client to the chat server, open another terminal and run:

```bash
python client.py
```

The client will prompt you to enter a nickname. Once connected, you can start chatting with other users connected to the same server.

### 5. Commands

Once connected, the following commands are available to the clients:

- `/list`: Lists all connected users.
- `/msg <nickname> <message>`: Sends a private message to a specific user.
- `/quit`: Disconnects from the chat server.
