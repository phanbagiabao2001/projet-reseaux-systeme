#include "wrapper.h"
#include "coordinates.h"
#include "udp_peer.h"
#include "circ_buf.h"

static udp_peer_t g_peer;
static void (*g_python_callback)(float x, float y, float z, float t,float h);

bool bExit = false;

static void myCallback(void * data, size_t len) {
    coordinates_t * coor = (coordinates_t *)data;
    //fprintf(stderr,"recvcc x y z t: %f %f %f %lu\n",coor->x,coor->y,coor->z,coor->time);
    //memcpy(&g_peer.peer_postion,coor,sizeof(coordinates_t));
    g_python_callback(coor->x,coor->y,coor->z,coor->t,coor->h);
}

bool init_peer(int local_port, int remote_port, char * remote_ip) {
    g_peer.init = init_udp_peer;
    g_peer.send = send_block;
    g_peer.recv = recv_block;
    g_peer.callback = myCallback;
    g_peer.close = close_udp_peer;

    return g_peer.init(&g_peer,local_port,remote_port,remote_ip);
}
void send_coor(float x, float y, float z, float t, float h) {
    coordinates_t coor = {
        .x = x,
        .y = y,
        .z = z,
        .t = t,
        .h = h,
    };

    int8_t * pack = serialize_data(&coor);
    g_peer.tx.lock(&g_peer.tx);
    g_peer.tx.write_bytes(&g_peer.tx,pack,sizeof(coordinates_t) + 2);
    g_peer.tx.unlock(&g_peer.tx);
    free(pack);
}
void register_callback(void (*callback)(float x, float y, float z, float t, float h)) {
    g_python_callback = callback;
    /* Assign the address of the function "g_python_callback" to the function
     pointer "callback" (may be also written as "callback = &g_python_callback;")*/
}
void close_peer()
{
    bExit = true;
    g_peer.close(&g_peer);
}