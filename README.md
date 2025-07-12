# Building a Peer-to-Peer File Sharing Network in Python

## The Motivation

This project started as an experiment in **learning TCP sockets, networking, and system-level programming**. Instead of following a tutorial blindly, I chose to **build a fully functional Peer-to-Peer (P2P) network** from scratch — with a practical goal: **sending files between peers without a central server managing transfers**.
The goal wasn't to just share files — it was to **understand how decentralized systems operate**, how low-level protocols behave, and what architectural trade-offs emerge in real-time development.


## Architecture Overview

### High-Level Components

1. **Peers**
   - Each peer can act as both **client and server**.
   - They expose a socket server and accept connections from other peers.
   - They can **send encrypted files** to another peer.

2. **Bootstrap Server**
   - A **central registry** that keeps track of all peers (IP + port).
   - It doesn't manage file transfer but helps new peers discover others.
   - Offers two endpoints:
     - `POST /api/register` — Register a new peer.
     - `GET /api/get_peers` — Return list of known peers.


## Thought Process & Design Decisions

### Phase 1: Establish TCP Connections

- Implemented basic socket server and client logic using `socket`.
- Encapsulated this in a `Peer` class with:
  - `start_server()`: Listens for incoming peer connections.
  - `connect_to_peer()`: Connects to another peer and sends a message.
  
**Goal**: Understand raw TCP, port binding, multi-threaded servers.


### Phase 2: Bootstrap Server

- Added a simple HTTP server using Python’s `http.server`.
- Peers register themselves on startup (`register_as_peer()`).
- Other peers can fetch the list via `get_all_peers()`.

**Goal**: Explore the concept of peer discovery in decentralized networks.


### Phase 3: File Transfer

- Built a protocol on top of TCP:
  - A JSON "header" is sent first (filename, size).
  - File chunks are sent afterward in a loop.
- Introduced chunking to avoid memory issues.

**Goal**: Learn how to transmit metadata and data reliably over sockets.



## What Works

- ✅ TCP connection and communication between peers
- ✅ Peer registry via HTTP-based bootstrap server
- ✅ Chunked file transfer
- ✅ Asynchronous listening and sending


## What Could Be Improved

### 1. Better Connection Management

- Current TCP server runs on a fixed IP (`127.0.0.1`).
- **Improvement**: Enable **external connections** using `0.0.0.0` and NAT traversal techniques.
- Could integrate **UPnP** or STUN for real-world deployment.

### 2. Bootstrap Server Health Check

- Currently stores **all peers blindly**.
- **Improvement**: Periodically **ping peers** and remove dead ones from the DB.

### 3. Use a Better Database

- We use SQLite (`peer_registry.db`), which is file-based.
- **Improvement**: Switch to **PostgreSQL** or **Redis** for concurrent access and in-memory lookups.

### 4. Robust Encryption

- **Improvement**:
  - Use **asymmetric encryption (RSA)** to exchange a unique session key.
  - Or upgrade to TLS sockets for encryption + identity.

### 5. Protocol Design

- Right now, it’s a simple custom protocol.
- **Improvement**:
  - Define a proper protocol schema (like HTTP headers).
  - Allow future extensions (chat messages, streaming).

### 6. Graceful Shutdown & Error Recovery

- Connections may hang or break silently.
- **Improvement**: Add timeouts, retries, logging, and cleanup logic.


## Tech Stack

- Python 3.11+
- SQLite (for bootstrap registry)
- `socket` (TCP communication)
- `http.server` (Bootstrap API)
- `dotenv` (Config management)


## Future Ideas
- Add a minimal GUI (Tkinter or Web-based).
- Integrate content hashing and file integrity verification.
- Enable group broadcasting or peer clustering.
- Add peer authentication and digital signatures.

## Final Words
This project isn’t a production-grade P2P system — but it’s an honest exercise in building something real, learning by doing, and peeling away abstraction layers to understand how the web truly works under the hood.
It's a foundation for future projects in decentralized systems, file sharing, or even building your own BitTorrent-lite client.
