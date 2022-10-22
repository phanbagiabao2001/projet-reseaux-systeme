#ifndef _WRAPPER_H_
#define _WRAPEER_H_
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "coordinates.h"

bool init_peer(int local_port, int remote_port, char * remote_ip);
void send_coor(float x, float y, float z, float t,float h);
void register_callback(void (*callback)(float x, float y, float z, float t,float h));
void close_peer();

#endif