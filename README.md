P2P Local File Transfer
Author: Dandan Rabinovitz
Initial Commit: July 12, 2026

A peer-to-peer (P2P) file transfer application designed for direct, serverless data migration between hosts over a Local Area Network (LAN).

By establishing a direct socket connection between the sender and receiver, this project eliminates the need for intermediate cloud architecture or external servers, ensuring high-speed local data transfer and data privacy.

Features
Direct peer-to-peer connection over LAN.

Zero Configuration: Connects using standard local IPv4 addresses without manual port forwarding.

Automatic Storage: Incoming payloads are automatically written to the server's working directory.

Architecture & Workflow
The system utilizes a client-server model to establish the peer connection:

The Receiver (Host) initializes a listener socket via the server binary.

The Sender (Client) initiates a handshake by targeting the host's local IP address.

The Payload streams directly between the machines, bypassing the public internet.

Usage
Prerequisites
Both machines must be connected to the same local subnet (same Wi-Fi or Ethernet network).

Step 1: Receiving Files (Server)
Place fs-server.exe into your desired download directory.

Launch fs-server.exe.

Click Start Server to begin listening for incoming connections.

Note your local IP address (e.g., 192.168.1.50).

Step 2: Sending Files (Client)
Launch fs-client on the sending machine.

Input the receiver's local IP address when prompted.

Select the file you intend to transfer.

The transmission will begin immediately, and the file will appear in the server's directory upon completion.
