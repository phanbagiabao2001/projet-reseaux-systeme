#include "udp_peer.h"
#include "coordinates.h"

bool init_udp_peer(udp_peer_t * peer, int local_port, int remote_port, char * remote_ip) {
    static bool inited = false;
    if (inited) {
        return true;
    }
    inited = true;

    memset(&peer->servaddr, 0, sizeof(peer->servaddr)); 
    memset(&peer->remoteaddr, 0, sizeof(peer->remoteaddr)); 

   // Creating socket file descriptor 
    if ((peer->sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        return false; 
    } 
        

    socklen_t reuse = 1;
    if (setsockopt(peer->sockfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("setsockopt(SO_REUSEADDR) failed");
        return false;
    }
    if (setsockopt(peer->sockfd, SOL_SOCKET, SO_REUSEPORT, &reuse, sizeof(reuse)) < 0) {
        perror("setsockopt(SO_REUSEPORT) failed");
        return false;
    }
    struct timeval timeout;      
    timeout.tv_sec = 2;
    timeout.tv_usec = 0;
    if (setsockopt(peer->sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout,sizeof(timeout)) < 0) {
        perror("setsockopt failed\n");
        return false;
    }

    if (setsockopt(peer->sockfd, SOL_SOCKET, SO_SNDTIMEO, &timeout,sizeof(timeout)) < 0) {
        perror("setsockopt failed\n");
        return false;
    }

    // Filling local information 
    peer->servaddr.sin_family    = AF_INET; // IPv4 
    peer->servaddr.sin_addr.s_addr = INADDR_ANY; 
    peer->servaddr.sin_port = htons(local_port); 

    // Filling remote information 
    peer->remoteaddr.sin_family    = AF_INET; // IPv4 
    peer->remoteaddr.sin_addr.s_addr = inet_addr(remote_ip); 
    peer->remoteaddr.sin_port = htons(remote_port); 

    // Bind the socket with the server address 
    if ( bind(peer->sockfd, (const struct sockaddr *)&peer->servaddr, sizeof(peer->servaddr)) < 0 ) { 
        perror("bind failed"); 
        return false;
    } 

    //init buf
    peer->rx.init = init_circ_buf;
    peer->rx.del = del_circ_buf;
    peer->rx.write_bytes = write_bytes_to_circ_buf;
    peer->rx.write_byte = write_byte_to_circ_buf;
    peer->rx.read_bytes = read_bytes_from_circ_buf;
    peer->rx.read_byte = read_byte_form_circ_buf;
    peer->rx.size = circ_buf_num_items;
    peer->rx.lock = lock_circ_buf;
    peer->rx.unlock = unlock_circ_buf;
    if (!peer->rx.init(&peer->rx,256)) {
        perror("init rx buf fail");
        return false;
    }

    peer->tx.init = init_circ_buf;
    peer->tx.del = del_circ_buf;
    peer->tx.write_bytes = write_bytes_to_circ_buf;
    peer->tx.write_byte = write_byte_to_circ_buf;
    peer->tx.read_bytes = read_bytes_from_circ_buf;
    peer->tx.read_byte = read_byte_form_circ_buf;
    peer->tx.size = circ_buf_num_items;
    peer->tx.lock = lock_circ_buf;
    peer->tx.unlock = unlock_circ_buf;
    if (!peer->tx.init(&peer->tx,256)) {
        perror("init rx buf fail");
        return false;
    }

    //init thread RX
    pthread_attr_t attrib;
    pthread_attr_init(&attrib);
    pthread_attr_setdetachstate(&attrib, PTHREAD_CREATE_DETACHED);

    pthread_t thread_RX;
    int ret = pthread_create(&thread_RX, &attrib, recv_block_loop, peer);
    if (0 != ret) {
        perror("create thread fail");
    }
    pthread_setname_np(thread_RX, "RXDataThread");

    //init thread TX
    pthread_t thread_P;
    ret = pthread_create(&thread_P, &attrib, process_block_loop, peer);
    if (0 != ret) {
        perror("create thread fail");
    }
    pthread_setname_np(thread_P, "ProcessDataThread");

    return true;
}
ssize_t send_block(udp_peer_t * peer,void * data, size_t len) {

    return (sendto(peer->sockfd, (int8_t *)data , len, 0, (const struct sockaddr *) &peer->remoteaddr, sizeof(peer->remoteaddr))); 
}
ssize_t recv_block(udp_peer_t * peer,void * data, size_t len) {
    struct sockaddr_in cliaddr;
    socklen_t lenCli = sizeof(cliaddr);  //len is value/result 
    memset(&cliaddr, 0, sizeof(cliaddr)); 
    return (recvfrom(peer->sockfd, data, len,  0, ( struct sockaddr *) &cliaddr, &lenCli)); 
}

extern bool bExit;

void * recv_block_loop(void * arg) {
    udp_peer_t * peer = (udp_peer_t *)arg;
    while(!bExit) {
        int8_t buffer[MAXLINE]; 
        ssize_t len = peer->recv(peer,buffer,MAXLINE);

        if (len > 0) {
            peer->rx.lock(&peer->rx);
            peer->rx.write_bytes(&peer->rx,buffer,len);
            peer->rx.unlock(&peer->rx);
        }
    }
    pthread_detach(pthread_self());
    pthread_exit(NULL);
    return NULL;
}
void * process_block_loop(void * arg) {
    udp_peer_t * peer = (udp_peer_t *)arg;
    bool pre_pack = false,full_pack = false;
    int8_t buffer[sizeof(coordinates_t) + 2] ; 

    while(!bExit) {
        bool active = false;
        //RX
        {
            peer->rx.lock(&peer->rx);
            if (!pre_pack) { 
                if(peer->rx.read_byte(&peer->rx,&buffer[0])) {
                    if ((uint8_t)buffer[0] == 0xff) {
                        pre_pack = true;
                    }
                }
            }
            if (pre_pack) {
                size_t aviable_size = peer->rx.size(&peer->rx);
                if (aviable_size >= sizeof(coordinates_t) + 1) {
                    peer->rx.read_bytes(&peer->rx,buffer + 1,sizeof(coordinates_t) + 1);
                    full_pack = true;
                    pre_pack = false;
                } else {
                    full_pack = false;
                }
            }
            peer->rx.unlock(&peer->rx);

            if (full_pack) {
                if ((uint8_t)(buffer[sizeof(coordinates_t) + 1]) == 0xAA) {
                    coordinates_t * coor = deserialize_data(buffer,sizeof(coordinates_t) + 2);
                    if (coor) {
                        peer->callback(coor,sizeof(coordinates_t));
                        free(coor);
                    }
                }
                full_pack = false;
            }
        }
        //TX
        {
            int8_t buffer[MAXLINE]; 
            peer->tx.lock(&peer->tx);
            size_t len = peer->tx.read_bytes(&peer->tx,buffer,MAXLINE);
            peer->tx.unlock(&peer->tx);
            if (len > 0) {
                active = true;
                peer->send(peer,buffer,len);
            }
        }
        if (!active)
            usleep(100000);
    }
    pthread_detach(pthread_self());
    pthread_exit(NULL);

    del_circ_buf(&peer->tx);
    del_circ_buf(&peer->rx);

    return NULL;
}

void close_udp_peer(udp_peer_t * peer) {
    close(peer->sockfd);
}
