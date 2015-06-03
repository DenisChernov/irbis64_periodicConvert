from cryptography.hazmat.bindings.commoncrypto.cf import INCLUDES
from xlwt import Workbook

__author__ = 'demiin'


import socket
import xlrd
import xlwt
import re

tableSource = '/mnt/hard/Dropbox/invent.xls'
tableDestination = "/mnt/hard/Dropbox/invent_reparsed_10.xls"
reg = re.compile("__60#([а-яА-Я\\s0-9,-;\.]*)__200#([\(\)\"а-яА-Я\\s0-9,-;\.a-zA-Z\[\]\!\?]*)__200f#([\(\)\[\]а-яА-Я\\s0-9,-;\.]*)__215#([\[\]а-яА-Я\\s0-9,-;\.a-zA-Z]*)__10#([\[\]а-яА-Я\\s0-9,-;\.]*)#")
row = 1
fWrite = xlwt.Workbook()
ww = fWrite.add_sheet("Sheet")
#ww.write(0, 0, "#")
#ww.write(0, 1, "Инвентарный номер")
#ww.write(0, 2, "Место хранения")
#ww.write(0, 3, "Заглавие")
#ww.write(0, 4, "Раздел")



fRead = xlrd.open_workbook(tableSource, formatting_info=True)
ws = fRead.sheet_by_index(1)

bases = ['OLDEK', 'RETRO']
SERVER = "192.168.9.20"
#log = open("/tmp/unlock_irbis64_records", "w")
#log.write(str(datetime.datetime.now()) + "\n")


counter = 1
while (row < ws.nrows):
### First step - connect   ####################
    msg_connect = "\nA\nC\nA\n31771\n" + str(counter) + "\n" + "9f9@7Nuq\nirbisoft\n\n\n\n" + "irbisoft\n9f9@7Nuq"
    msg_connect = str(len(msg_connect) - 1) + msg_connect
    sock = socket.socket()
    sock.connect((SERVER, 6666))
    sock.send(msg_connect.encode('utf-8'))
    data = sock.recv(64000)
    sock.close()
    #print("connected")
#log.write("connected to: " + SERVER + "\n")

### Steps - get book   ###########

    for bd in range(0, len(bases)):
        counter += 2
        msg_listBlocked = "\nK\nC\nK\n31771\n" \
                          + str(counter) + "\n" + "9f9@7Nuq\nirbisoft\n\n\n\n" + bases[bd] + \
                          "\n\"IN=" + str(int(ws.row_values(row)[0])) \
                          + "\"\n1\n1\nmpl,'&&&&&','__60#',v60,'__200#',v200^a,'__200f#',v200^f,'__215#',v215^a,'__10#',v10^d,'#'"
        msg_listBlocked = str(len(msg_listBlocked) - 1) + msg_listBlocked
        sock = socket.socket()
        sock.connect((SERVER, 6666))
        sock.send(msg_listBlocked.encode('utf-8'))
        data = ""
        buf = sock.recv(10240)
        data += buf.decode('utf-8')
        sock.close()
        #print("base: " + bases[bd])
        #print(data)

        res = reg.search(data)
        if res:
            ww.write(row + 2, 0, row)
            ww.write(row + 2, 1, str(int(ws.row_values(row)[0])))
            ww.write(row + 2, 2, "ф 14")
            s1 = res.group(3) + " " + res.group(2) + " - " + res.group(4)
         #   print(s1)
            ww.write(row + 2, 3, s1)
            ww.write(row + 2, 4, res.group(1))
            ww.write(row + 2, 5, res.group(5))
            print(str(int(ws.row_values(row)[0])) + " - done")
            break
        else:
            ww.write(row + 2, 0, row)
            ww.write(row + 2, 1, str(int(ws.row_values(row)[0])))
            ww.write(row + 2, 2, "ф 14")
            ww.write(row + 2, 3, "")
            ww.write(row + 2, 4, "")
            print(str(int(ws.row_values(row)[0])) + " - done")
            break

#    log.write("get blocked from: " + bases[bd] + "\n")

### Last step - disconnect   ################
    msg_disconnect = "\nB\nA\nB\n31771\n" + str(counter) + "\n" + "9f9@7Nuq\nirbisoft\n\n\n\n" + "irbisoft\n9f9@7Nuq"
    msg_disconnect = str(len(msg_disconnect) - 1) + msg_disconnect
    sock = socket.socket()
    sock.connect((SERVER, 6666))
    sock.send(msg_disconnect.encode('utf-8'))
    data = sock.recv(64000)
    sock.close()
    #print ("disconnect")
    row += 1

#log.write("disconnect" + "\n")
#log.close()

fWrite.save(tableDestination)
print ("total: " + str(row))