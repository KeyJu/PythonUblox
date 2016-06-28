#coding:utf-8
from struct import *

SYS_NONE =   0x00
SYS_GPS  =   0x01
SYS_SBS  =   0x02
SYS_GLO  =   0x04
SYS_GAL  =   0x08
SYS_QZS  =   0x10
SYS_CMP  =   0x20
SYS_ALL  =   0xFF

MINPRNGPS = 1
MAXPRNGPS = 34
NSATGPS   =  (MAXPRNGPS-MINPRNGPS+1)
NSYSGPS   =  1

MINPRNGLO  = 1 
MAXPRNGLO  = 24
NSATGLO = (MAXPRNGLO-MINPRNGLO+1)
NSYSGLO = 1

MINPRNGAL =  1                   
MAXPRNGAL = 27                  
NSATGAL   = (MAXPRNGAL-MINPRNGAL+1)
NSYSGAL   =  1

MINPRNQZS   = 193
MAXPRNQZS   = 195
MINPRNQZS_S = 183
MAXPRNQZS_S = 185
NSATQZS  =   (MAXPRNQZS-MINPRNQZS+1)
NSYSQZS  =   1

MINPRNCMP  = 1 
MAXPRNCMP  = 35
NSATCMP   =  (MAXPRNCMP-MINPRNCMP+1)
NSYSCMP   =  1

values = {
           0: SYS_GPS,
           1: SYS_SBS,
           2: SYS_GAL,
           3: SYS_CMP,
           5: SYS_QZS,
           6: SYS_GLO,
         }

def satno(sys ,prn):
    if prn <= 0:
        return 0
    elif prn < MINPRNGPS or prn >MAXPRNGPS:
        return 0
    else :
        if sys == SYS_GPS :
            return prn-MINPRNGPS+1
        elif sys == SYS_GLO :
            return NSATGPS+prn-MINPRNGLO+1 
        elif sys == SYS_GAL :
            return NSATGPS+NSATGLO+prn-MINPRNGAL+1
        elif sys == SYS_QZS :
            return NSATGPS+NSATGLO+NSATGAL+prn-MINPRNQZS+1 
        elif sys == SYS_CMP :
            return NSATGPS+NSATGLO+NSATGAL+NSATQZS+prn-MINPRNCMP+1
        elif sys == SYS_SBS :
            return NSATGPS+NSATGLO+NSATGAL+NSATQZS+NSATCMP+prn-MINPRNSBS+1  

filename = ['ublox 001.txt','ublox 002.txt']
name = ['Satellite ID','GPS Time','Pseudorange','Carrier Phase','C/N']
i = 1
for fn in filename:
    fr = open(fn,'rb')
    fw = open('ublox%d.txt' % i,  'w')
    print(name[0].rjust(15)+name[1].rjust(18)+name[2].rjust(20)+name[3].rjust(20)+name[4].rjust(10))
    fw.write(name[0].rjust(15)+name[1].rjust(18)+name[2].rjust(20)+name[3].rjust(20)+name[4].rjust(10))
    fw.write("\n") 
    data = fr.read()       
    for p in range(len(data)):
        if data[p:p+4] == b'\xb5b\x02\x15':
            p = p+6
            buffer = []
            p1 = p
            buffer.append("%0.3f" % unpack('!d',data[p1:p1+8][::-1]))
            p1 = p+8
            buffer.append("%d" % unpack('!H',data[p1:p1+2][::-1]))
            p1 = p+10
            buffer.append("%d" % unpack('!b',data[p1:p1+1][::-1]))
            p1 = p+11
            buffer.append("%d" % unpack('!B',data[p1:p1+1][::-1]))
            p1 = p+12
            buffer.append("%x" % data[p1])
            p1 = p+13
            reserved1 = []
            reserved1.append("%d" % unpack('!B',data[p1:p1+1][::-1]))
            reserved1.append("%d" % unpack('!B',data[p1+1:p1+2][::-1]))
            reserved1.append("%d" % unpack('!B',data[p1+2:p1+3][::-1]))
            buffer.append(reserved1)
            p1 = p+16
            p = p+16
            for j in range(int(buffer[3])):                
                buffer.append("%0.3f" % unpack('!d',data[p1:p1+8][::-1])) 
                p1 = p+8
                buffer.append("%0.3f" % unpack('!d',data[p1:p1+8][::-1]))
                p1 = p+16
                buffer.append("%0.3f" % unpack('!f',data[p1:p1+4][::-1]))
                p1 = p+20
                buffer.append("%d" % unpack('!B',data[p1:p1+1][::-1]))
                p1 = p+21
                buffer.append("%d" % unpack('!B',data[p1:p1+1][::-1]))
                p1 = p+22
                buffer.append("%d" % unpack('!B',data[p1:p1+1][::-1]))
                p1 = p+23
                buffer.append("%d" % unpack('!B',data[p1:p1+1][::-1]))
                p1 = p+24
                buffer.append("%d" % unpack('!H',data[p1:p1+2][::-1]))
                p1 = p+26
                buffer.append("%d" %  unpack('!B',data[p1:p1+1][::-1]))
                p1 = p+27
                buffer.append("%x" % data[p1])
                p1 = p+28
                buffer.append("%x" % data[p1])
                p1 = p+29
                buffer.append("%x" % data[p1])
                p1 = p+30
                buffer.append("%x" % data[p1])
                p1 = p+31
                buffer.append("%x" % data[p1])
                p1 = p+32
                p = p1 
                if  int(buffer[9]) in values:
                    if values[int(buffer[9])] == SYS_QZS:
                        buffer[10] = str(int(buffer[10]) + 192 )
                    sat = satno(values[int(buffer[9])],int(buffer[10])) 
                    if sat != 0 :
                        buffer[10] = str(sat)                                      
                        need = []
                        need.append(buffer[10])
                        need.append(buffer[0])
                        need.append(buffer[6])
                        need.append(buffer[7])
                        need.append(buffer[14])
                        print(need[0].rjust(15)+need[1].rjust(18)+need[2].rjust(20)+need[3].rjust(20)+need[4].rjust(10))
                        fw.write(need[0].rjust(15)+need[1].rjust(18)+need[2].rjust(20)+need[3].rjust(20)+need[4].rjust(10))
                        fw.write("\n")
                del buffer[6:] 
    i = i+1
    fr.close()
    fw.close()    
