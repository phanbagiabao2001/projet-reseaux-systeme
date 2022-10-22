#ifndef _UDP_PEER_H_
#define _UDP_PEER_H_

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <pthread.h>
#include "circ_buf.h"
#include "coordinates.h"

typedef struct udp_peer udp_peer_t;

#define MAXLINE 1024 

struct udp_peer {
    int sockfd;
    struct sockaddr_in servaddr, remoteaddr;
    circ_buf_t tx;
    circ_buf_t rx;

    bool (*init)(udp_peer_t * peer, int local_port, int remote_port, char * remote_ip);
    ssize_t (*send)(udp_peer_t * peer,void * data, size_t len);
    ssize_t (*recv)(udp_peer_t * peer,void * data, size_t len);
    void (*close)(udp_peer_t * peer);

    void (*callback)(void * data, size_t len);
};

bool init_udp_peer(udp_peer_t * peer, int local_port, int remote_port, char * remote_ip);
void close_udp_peer(udp_peer_t * peer);
ssize_t send_block(udp_peer_t * peer,void * data, size_t len);
ssize_t recv_block(udp_peer_t * peer,void * data, size_t len);
void * recv_block_loop(void * arg);
void * process_block_loop(void * arg);

#endif
