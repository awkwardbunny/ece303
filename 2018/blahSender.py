from sender import BogoSender
import logging
import socket

import channelsimulator
import utils
import array
import struct

class BlahSender(BogoSender):
    TEST_DATA = bytearray('A'*33)  # some bytes representing ASCII characters: 'D', 'A', 'T', 'A'

    def __init__(self):
        super(BlahSender, self).__init__()

    def encapsulate(self, data, seq):
        return struct.pack('BB',seq,00000000) + data;

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        while True:
            try:
                window_size = 1024
                frame_size = 10

                last_acked = 0
                last_sent = 0

                padding = frame_size - (len(data)%frame_size)
                data += '\0'*padding
                max_frame = len(data)/frame_size

                #array.array('i',(0 for i in range(0,len(data))));
                while(last_acked < max_frame):
                    while(last_sent < max_frame):
                        beg = last_sent * frame_size
                        end = (last_sent+1) * frame_size
                        print str(beg)+'::'+str(end)
                        tosend = self.encapsulate(data[beg:end], beg)
                        self.simulator.put_to_socket(tosend)
                        last_sent = last_sent+1

                    while(last_acked < last_sent):
                        ack = self.simulator.get_from_socket()
                        if(ack == 'ACK'+str(last_acked+1)):
                                last_acked = last_acked+1

                self.simulator.put_to_socket(data)  # send data
                ack = self.simulator.get_from_socket()  # receive ACK
                self.logger.info("Got ACK from socket: {}".format(
                    ack.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                break
            except socket.timeout:
                pass

if __name__ == "__main__":
    sndr = BlahSender()
    sndr.send(BlahSender.TEST_DATA)
