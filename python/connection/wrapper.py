import ctypes

udp_peer_lib = ctypes.CDLL("../c/libudp_peer.so")

def init_peer(local_port, remote_port, remote_ip) :
    udp_peer_lib.init_peer.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_char_p]
    udp_peer_lib.init_peer.restype = ctypes.c_bool
    return udp_peer_lib.init_peer(local_port,remote_port,str(remote_ip).encode('utf-8'))

def send_peer(x,y,z,t,h) :
    udp_peer_lib.send_coor.argtypes = [ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float]
    udp_peer_lib.send_coor(x,y,z,t,h)

def callbackType() :
    return ctypes.CFUNCTYPE(None,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float)

def register_callback(func) :
    udp_peer_lib.register_callback.argtypes = [callbackType()]
    udp_peer_lib.register_callback(func)

def close_peer() :
    return udp_peer_lib.close_peer()