import socket
import sys
import struct

class DT_request(object):
    def __init__(self, magicNo, packetType, requestType):
        self.magicNo = magicNo
        self.packetType = packetType
        self.requestType = requestType        
        self.request_packet = bytearray()
    
    
    def validity_check(self):        
        if self.magicNo == 0x497E:
            if self.packetType == 0x0001:
                if self.requestType == 0x0001 or self.requestType == 0x0002:
                    self.input_valid = True
                else:
                    self.input_valid = False
            else:
                self.input_valid = False
        else:
            self.input_valid = False
        
        return self.input_valid
    
    
    def encode(self):
        if self.input_valid == True:
            self.request_packet = struct.pack("<hhh", self.magicNo, self.packetType, self.requestType)
            #self.request_packet.extend(self.magicNo.to_bytes(2, byteorder = 'big'))
            #self.request_packet.extend(self.packetType.to_bytes(2, byteorder = 'big'))
            #self.request_packet.extend(self.requestType.to_bytes(2, byteorder = 'big'))
            result = self.request_packet
        else:
            result = "Check the input."
        
        return result
        

def main():
    
    input_request_type = sys.argv[1]
    UDP_ip = sys.argv[2]
    UDP_port = int(sys.argv[3])
    
    if input_request_type == "date":
        request_type = 0x0001
    elif input_request_type == "time":
        request_type = 0x0002
    
    message = DT_request(0x497E, 0x0001, request_type)
    message.validity_check()
    message.encode()
    
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientsock.sendto(message.request_packet, (UDP_ip, UDP_port))
    
    
    
main()
