from multiprocessing import Process, Queue

from sympy import RealNumber
rx = Queue()
def getRXQueue() :
    return rx

tx = Queue()

def getTXQueue() :
    return tx

rb = Queue()

def getRBQueue():
    return rb

rn = Queue()
# rn
# def getRNQueue():
#     return rn