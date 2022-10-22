#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 5555

int main() {
  int c_fd, py_fd;
  struct sockaddr_in c_addr, py_addr;
  socklen_t addr_size;
  char buffer[1024];

  // socket
  c_fd = socket(AF_INET, SOCK_STREAM, 0);
  c_addr.sin_family = AF_INET;
  c_addr.sin_port = htons(PORT);
  c_addr.sin_addr.s_addr = inet_addr("192.168.43.109");

  bind(c_fd, (struct sockaddr *)&c_addr, sizeof(c_addr));
  listen(c_fd, 5);
  printf("[LISTENING] Port Number: %d\n", PORT);

  while (1) {
    py_fd = accept(c_fd, (struct sockaddr *)&py_addr, &addr_size);
    //printf("[CONNECTED] New Connection\n");
    printf("\nEnter your message: \n");
    fgets(buffer, 1024, stdin);
    fflush(stdin);
    send(py_fd, buffer, strlen(buffer), 0);
    memset(buffer, '\0', sizeof(buffer));//renew buffer by \0
    recv(py_fd, buffer, 1024, 0);
    printf("[PYTHON] says: %s\n", buffer);
    char end_message1[5] = "quit";
    char end_message2[5] = "Quit";
    char end_message3[5] = "QUIT";
    if (strcmp(buffer, end_message1) == 0 || strcmp(buffer, end_message2) == 0 || strcmp(buffer, end_message3) == 0){
    close(py_fd);
    printf("[DISCONNECTED] Connection closed\n");
    close(c_fd);
    }
  }

  return 0;
}
