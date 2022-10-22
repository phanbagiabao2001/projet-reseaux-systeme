import random
import wrapper
import time
import argparse
import atexit

def exit_handler():
    wrapper.close_peer()

def callbackTest(x,y) :
    print('x : {}, y : {}'.format(x,y))

if __name__ == "__main__":
    atexit.register(exit_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_port',type=int,help='local port')
    parser.add_argument('--remote_port',type=int,help='remote port')
    parser.add_argument('--remote_ip',type=str,help='remote ip')
    args = parser.parse_args()

    if wrapper.init_peer(args.local_port,args.remote_port,args.remote_ip) == False :
        exit()
    wrapper.register_callback(wrapper.callbackType()(callbackTest))
    while(True) :
        time.sleep(0.5)
        coor = [random.randrange(100, 1000, 1),random.randrange(100, 1000, 1)]
        print("send : " + str(coor))
        wrapper.send_peer(coor[0],coor[1])
