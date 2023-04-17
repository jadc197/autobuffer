####################################################################################################
#
# This example demonstrates the use of autobuffer for streaming data with the zeromq PUB/SUB pattern
#
#   To run this example, you need to
#       pip install autobuffer
#       pip install pyzmq
#       pip install numpy
#
####################################################################################################


import autobuffer
import zmq
from threading import Thread
from multiprocessing import Process
import numpy as np
import time

def MyDataSource(outaddress):
    zmqContext = zmq.Context()
    outsocket = zmqContext.socket(zmq.PUB)
    outsocket.bind(outaddress)
    # give the subscriber some time to connect...
    time.sleep(1)
    tic=time.perf_counter()
    while True:
        toc = time.perf_counter()
        if (toc - tic) > 0.000262144: # Send blocks of data at an average rate around 1 GBit/s - slow down if needed...
            #print(toc-tic)
            tic = time.perf_counter()
            data2send = np.arange(4096.0) # Send a block of 4096 x 64 bit floats, for example
            outsocket.send(data2send)

def MyDataSink(inaddress):
    zmqContext = zmq.Context()
    insocket = zmqContext.socket(zmq.SUB)
    insocket.connect(inaddress)
    insocket.subscribe(b'')
    while True:
        incoming=np.frombuffer(insocket.recv())
        print(incoming)


def MyProcessingFunction(data):
    # example processing: calculate the sum of all data points
    result = np.sum(data)
    print(round(len(data)/4096)) # this will print how many data blocks were queued by autobuffer
    return result

def MyProcessingNode(inaddress, outaddress, processing_function):
    # This function might seem redundant but it is just to make it easier for a clean exit of this example script (terminate the process and the threads should go as well)
    processing_node = MyDataProcessor(inaddress, outaddress, processing_function)

class MyDataProcessor:
    def __init__(self, inaddress, outaddress, processing_function):
        # create a zeromq context:
        self.zmqContext = zmq.Context()
        # create an autobuffer instance:
        self.autobuffer = autobuffer.autoBuffer()
        # start the incoming and the processing / outgoing threads
        self.T0 = Thread(target = self.buffer_in, args = (inaddress,))
        self.T1 = Thread(target = self.buffer_out, args = (processing_function, outaddress,))
        self.T0.start()
        self.T1.start()
        
    def buffer_in(self, inaddress):
        insocket = self.zmqContext.socket(zmq.SUB)
        insocket.connect(inaddress)
        insocket.subscribe(b'')
        while True:
            incoming=np.frombuffer(insocket.recv())
            self.autobuffer.enque(incoming)

    def buffer_out(self, processing_function, outaddress):
        outsocket = self.zmqContext.socket(zmq.PUB)
        outsocket.bind(outaddress)
        while True:
            data = self.autobuffer.deque()
            if data:
                outsocket.send(processing_function(np.ravel(data)))

if __name__ == '__main__':
    Plist = []
    # start the sink simulation process - this can be somewhere else on the network
    inaddress = "tcp://localhost:6010"
    P=Process(target = MyDataSink, args = (inaddress,))
    P.start()
    Plist.append(P)
    # start the processing node which makes use of the autoBuffer class
    inaddress = "tcp://localhost:6000"
    outaddress = "tcp://*:6010"
    processing_function = MyProcessingFunction
    P=Process(target = MyProcessingNode, args = (inaddress, outaddress, processing_function,))
    P.start()
    Plist.append(P)
    outaddress = "tcp://*:6000"
    # start the source simulation process - this can be somewhere else on the network
    P=Process(target = MyDataSource, args = (outaddress,))
    P.start()
    Plist.append(P)
    input("Press any key to exit...")
    for P in Plist:
            P.terminate()
            P.join()
