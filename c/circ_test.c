#include "circ_buf.h"
int main()
{
    circ_buf_t circ = {
        .init = init_circ_buf,
        .del = del_circ_buf,
        .write_bytes = write_bytes_to_circ_buf,
        .write_byte = write_byte_to_circ_buf,
        .read_bytes = read_bytes_from_circ_buf,
        .read_byte = read_byte_form_circ_buf,
        .lock = lock_circ_buf,
        .unlock = unlock_circ_buf,
    };
    circ.init(&circ,256);
    char a[50] = {'a'};
    int8_t res = 0;
    circ.lock(&circ);
    circ.write_bytes(&circ,a,sizeof(a));
    circ.unlock(&circ);
    circ.lock(&circ);
    printf("%d",circ.read_byte(&circ,&res));
    circ.unlock(&circ);

}