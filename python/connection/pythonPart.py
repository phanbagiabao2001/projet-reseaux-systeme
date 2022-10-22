import socket

IP = "192.168.43.109"
PORT = 5555
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    while(1):
        #TCP Socket 
        py = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        py.connect(ADDR)
        #Recv data
        data = py.recv(SIZE).decode(FORMAT)
        if data == "quit":
            py.close()
        print(f"[C] says: {data}")
        #Send data
        print("Enter your message: ");
        s = input()
        py.send(s.encode(FORMAT))
        #Close connection
        py.close()

if __name__ == "__main__":
    main()
