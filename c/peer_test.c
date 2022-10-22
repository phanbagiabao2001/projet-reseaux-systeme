#include "udp_peer.h"
#include "coordinates"
#include <signal.h>

bool bExit = false;
void exit_handler(int sig) {
    bExit = true;
}

void myCallback(void * data, size_t len) {
    coordinates_t * coor = (coordinates_t *)data;
    fprintf(stderr,"recv x : %f\n",coor->x);
}

int main(int argc, char *argv[]) {
    if(argc != 4) {
		perror("Missing Arg");
		exit(EXIT_FAILURE);
	}
    signal(SIGINT, exit_handler);
    udp_peer_t peer = {
        .init = init_udp_peer,
        .send = send_block,
        .recv = recv_block,
        .callback = myCallback,
    };
    peer.init(&peer,atoi(argv[1]),atoi(argv[2]),argv[3]);



    while (!bExit)
    {
        usleep(1000000);
        coordinates_t coor  = {
            .x = rand(),
            .y = rand(),
            .z = rand(),
            .time = rand(),
        };
        int8_t * pack = serialize_data(&coor);
        peer.tx.lock(&peer.tx);
        peer.tx.write_bytes(&peer.tx,pack,sizeof(coordinates_t) + 2);
        peer.tx.unlock(&peer.tx);
        fprintf(stderr,"send x : %f\n",coor.x);
        free(pack);
    }
    return 0;
}
