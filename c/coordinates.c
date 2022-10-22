#include "coordinates.h"

int8_t * serialize_data(coordinates_t * coor) {
    int8_t * data = (int8_t *)malloc(sizeof(coordinates_t) + 2);
    data[0] = 0xFF;
    data[sizeof(coordinates_t) + 1] = 0xAA;
    memcpy(data + 1,coor,sizeof(coordinates_t));
    return data;
}
coordinates_t * deserialize_data(int8_t * data,size_t len) {
    if (len != (sizeof(coordinates_t) + 2))
        return NULL;
    coordinates_t * ret = (coordinates_t *)malloc(sizeof(coordinates_t));
    memcpy(ret,data + 1,sizeof(coordinates_t));
    return ret;
}