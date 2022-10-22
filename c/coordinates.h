#ifndef _WRAPPER_H_
#define _WRAPPER_H_
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct coordinates coordinates_t;

struct __attribute__((packed)) coordinates {
    float x;
    float y;
    float z;
    float t;
    float h;
};

int8_t * serialize_data(coordinates_t * coor);
coordinates_t * deserialize_data(int8_t * data,size_t len);

#endif