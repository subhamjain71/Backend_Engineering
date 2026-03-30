1. User types domain → Enter

2. DNS Resolution
   Browser cache → OS cache → recursive resolver → authoritative NS
   Returns: target IP address

3. TCP Handshake (1 RTT)
   Client → SYN (random ISN=X)           → Server
   Server → SYN-ACK (ACK=X+1, ISN=Y)    → Client
   Client → ACK (ACK=Y+1)                → Server

   Server side:
     SYN arrives → kernel adds to SYN queue → sends SYN-ACK
     ACK arrives → kernel moves to accept queue
     Application calls accept() → gets file descriptor → connection ready

4. TLS 1.3 Handshake (1 RTT)
   Client → ClientHello + DH key share + supported ciphers
   Server → ServerHello + DH key share + Certificate + Finished
            (server selects cipher, both sides compute shared secret
             via Diffie-Hellman — key never transmitted over wire)
   Client → Finished
   Both sides now have identical symmetric key
   All further communication encrypted

5. HTTP Request sent over TLS encrypted connection

6. Server receives request
   NIC receives packet → raises hardware interrupt
   Kernel interrupt handler runs
   Packet copied into socket receive buffer (kernel space)
   Kernel marks socket fd as readable

7. Application notified via epoll
   epoll_wait() returns → "fd X has data ready"
   Application calls read(fd)
   Kernel copies data from socket buffer → userspace buffer
   Application processes request

8. Server sends response
   Application writes to fd
   Kernel copies to socket send buffer
   NIC transmits over wire

9. Connection kept alive
   keep-alive: reuse TCP+TLS for subsequent requests
   No handshake cost on next request



DNS cache entry:         ~100 bytes
TCP connection (kernel): ~10-20KB (send + receive buffers)
TLS session:             ~10KB (session state, keys)
File descriptor:         ~64 bytes (fd table entry)
epoll registration:      ~160 bytes per fd
──────────────────────────────────────────────────────
Per connection total:    ~20-40KB
At 50K connections:      ~1-2GB kernel memory
