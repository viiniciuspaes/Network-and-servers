# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 14:32:04 2018
@author: Glauco
"""

# import subnetcalc as sb
from PTA import subnetcalc as sb
import sys

"""
    Each entry in this table indicates the network address, 
    the network mask, and the forwarding interface.
"""
table = {
            ('41.0.1.0','24'): 3,
            ('41.0.1.192','26'): 2,
            ('20.100.0.0','19'): 1,
            ('0.0.0.0','0'): 4
        }

"""
    Each entry in the list below is the destination address
    of a given packet.
"""
packets = ['20.100.32.1','41.0.1.200']

def forwarding(ip,tbl):
    """
        Receives the destination ip address and chooses the route
        based on the longest prefix match againt the routing table.
        Inputs:
            ip: ip address (string)
            tbl: routing table (dict whose the value is the forwarding interface and the key is a tuple with network address and netmask)
        
        Returns: the forwarding interface
    """

    """
        Please change here
    """
    list_of_adress = []
    base_ip = ip.split(".")[0:-2:]
    last_dig = int(ip.split(".")[-1])
    for adress, forward in tbl.items():
        if base_ip == adress[0].split(".")[0:-2:]:
            list_of_adress.append([adress[0], int(adress[0].split(".")[-1]),forward])

    if list_of_adress.__len__() == 1:
        return list_of_adress[0][2]
    else:
        for index in range(len(list_of_adress)):
            new_value = abs(list_of_adress[index][1] - last_dig)
            list_of_adress[index][1] = new_value

    list_of_adress.sort(key=lambda x: x[1])

    return list_of_adress[0][2]


if __name__ == "__main__":
    if len(sys.argv) == 3:
        tblfile = sys.argv[1]
        ip = sys.argv[2]
        try:
            tbl = dict()
            tblpointer = file(tblfile)
            for line in tblpointer:
                fields = line.split(",")
                tbl[(fields[0],fields[1])] = int(fields[2].strip("\n"))
        except:
            print("Problem")
        intf = forwarding(ip,table);
        print("The packet with dest addr",ip,"will be forwarded to interface", intf)
    else:
        for ip in packets:
            intf = forwarding(ip,table);
            print("The packet with dest addr",ip,"will be forwarded to interface", intf)