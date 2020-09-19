import socket
import sys
import datetime
import struct
import select


class DT_response(object):
    def __init__(self, request_type, languageCode):
        #date and time
        self.now = datetime.datetime.now()
        self.year = self.now.year
        self.month = self.now.month
        self.day = self.now.day
        self.hour = self.now.hour
        self.minute = self.now.minute
        self.english = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        self.maori = {1: "Kohit¯atea", 2: "Hui-tanguru", 3: "Pout¯u-te-rangi", 4: "Paenga-wh¯awh¯a", 5: "Haratua", 6: "Pipiri", 7: "H¯ongongoi", 8: "Here-turi-k¯ok¯a", 9: "Mahuru", 10: "Whiringa-¯a-nuku", 11: "Whiringa-¯a-rangi", 12: "Hakihea"}
        self.german = {1: "Januar", 2: "Februar", 3: "M¨arz", 4: "April", 5: "Mai", 6: "Juni", 7: "Juli", 8: "August", 9: "September", 10: "Oktober", 11: "November", 12: "Dezember"}
        
        #packet components
        self.magicNo = 0x497E
        self.packetType = 0x0002
        self.request_type = request_type
        self.languageCode = languageCode
        self.response_packet = bytearray()
        
        
    def payload_string(self):
        if self.request_type == 0x0001: #date
            if self.languageCode == 0x0001:
                self.payload = "Today's date is %s %d, %d" % (self.english[self.month], self.day, self.year)
                print(self.payload)#test
            elif self.languageCode == 0x0002:
                self.payload = "Ko te ra o tenei ra ko %s %d, %d" % (self.maori[self.month], self.day, self.year)
                print(self.payload)#test
            elif self.languageCode == 0x0003:
                self.payload = "Heute ist der %s %d, %d" % (self.german[self.month], self.day, self.year)
                print(self.payload)#test
        elif self.request_type == 0x0002: #time
            if self.languageCode == 0x0001:
                self.payload = "The current time is %d:%d" % (self.hour, self.minute)
                print(self.payload)#test
            elif self.languageCode == 0x0002:
                self.payload = "Ko te wa o tenei wa %d:%d" % (self.hour, self.minute)
                print(self.payload)#test
            elif self.languageCode == 0x0003:
                self.payload = "Die Uhrzeit ist %d:%d" % (self.hour, self.minute)
                print(self.payload)#test
        return self.payload
    
    def payload_length_check(self):
        self.length = len(self.payload.encode())
        print(self.length)
        if self.length >= 255:
            print("ERROR: length too long")
            return False
        print("valid length")
        return True
    
    def packet_encode(self):
        self.payload_string()
        self.payload_byte = self.payload.encode('utf-8')
        if self.payload_length_check():
            self.response_packet_header = struct.pack(">hhhhbbbbb",self.magicNo, self.packetType, self.languageCode, self.year, self.month, self.day, self.hour, self.minute, self.length)
            self.response_packet = self.response_packet_header + self.payload_byte
            result = self.response_packet
            print(self.response_packet)
        return result




def request_packet_check(data):
    magicNo, packetType, request_type = struct.unpack("<hhh", data)
    packet_length = struct.calcsize(">hhh")
    if packet_length == 6:
        if (magicNo == 0x497E) and (packetType == 0x0001) and (request_type == 0x0001 or request_type == 0x0002):
            validity_check = True
    else:
        validity_check = False
    return validity_check

def decode(data):
    if request_packet_check(data):
        magicNo, packetType, request_type = struct.unpack("<hhh", data)
    return request_type

def main():
    UDP_ip = "127.0.0.1"
    
    #english packet
    UDP_port_eng = int(sys.argv[1])
    sock_eng = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_eng.bind((UDP_ip, UDP_port_eng))
    
    #maori
    UDP_port_mao = int(sys.argv[2])
    sock_mao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_mao.bind((UDP_ip, UDP_port_mao))
    
    #german
    UDP_port_ger = int(sys.argv[3])
    sock_ger = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_ger.bind((UDP_ip, UDP_port_ger))
    
    while True:
        client, _, _ = select.select([sock_eng, sock_mao, sock_ger], [], [], None)
        for s in client:
            if s:
                data, addr = s.recvfrom(1024)
                if s == sock_eng:
                    print ("eng", data)
                    print(len(data))
                    languageType = 0x0001
                    
                elif s == sock_mao:
                    print ("mao", data)
                    languageType = 0x0002
                
                elif s == sock_ger:
                    print ("ger", data)
                    languageType = 0x0003
        
        #setting and passing request_type and language_type to DT_response class
        requestType = decode(data)
        p = DT_response(requestType, languageType)
        p.packet_encode()
main()