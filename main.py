from audioop import add
from scapy.all import Dot11, Dot11ProbeReq, Dot11Beacon, sniff
import traceback
from data_manager import DataManager
from mac_vendor_lookup import MacLookup, VendorNotFoundError


# Get the mac address of the wireless mobile device
# that we are interested in targeting
def get_station_mac_from_pkt(pkt):

    # If the address 4 has meaning, then the packet is from a wireless bridge
    # This means that no mobile wireless device is involved
    #print("Meaning " + str(pkt[Dot11].address_meaning(4)))
    if pkt[Dot11].address_meaning(4) != None:
        return None


    addr_matrix = [
        {
            "meaning": pkt[Dot11].address_meaning(1),
            "addr": pkt.addr1
        },
        {
            "meaning": pkt[Dot11].address_meaning(2),
            "addr": pkt.addr2
        },
        {
            "meaning": pkt[Dot11].address_meaning(3),
            "addr": pkt.addr3
        }
    ]

    # Detect the BSSID
    bssid = None
    for addr in addr_matrix:
        if "BSSID" in addr["meaning"]:
            bssid = addr["addr"]

    # Get addr where TA=SA
    # This means that the Transmission Address = Source Address
    for addr in addr_matrix:
        if "TA=SA" in addr["meaning"]:
            return addr["addr"]

    # Is the previous one was not the case, then RA=DA is the one
    # Where Receiving Address = Destination Address
    for addr in addr_matrix:
        if "RA=DA" in addr["meaning"] and addr["addr"] != bssid:
            return addr["addr"]

    
    return None



# Get the mac address of the bssid (ap mac address)
def get_bssid_from_pkt(pkt):

    addr_matrix = [
        {
            "meaning": pkt[Dot11].address_meaning(1),
            "addr": pkt.addr1
        },
        {
            "meaning": pkt[Dot11].address_meaning(2),
            "addr": pkt.addr2
        },
        {
            "meaning": pkt[Dot11].address_meaning(3),
            "addr": pkt.addr3
        },
        {
            "meaning": pkt[Dot11].address_meaning(4),
            "addr": pkt.addr4
        }
    ]

    for addr in addr_matrix:
        if "BSSID" in addr["meaning"]:
            return addr["addr"]

    

def packet_handler(pkt):
    if pkt.haslayer(Dot11):

        # Management frames
        if pkt.type == 0:
        
            # Probe requests
            if pkt.subtype == 4:

                print("Probe request with MAC {pkt.addr2} and ssid {ssid}".format(
                    show=pkt.show(dump=True), pkt=pkt, ssid=pkt.info.decode()))

                DataManager().register_probe_request_frame(
                    station_mac=pkt.addr2, intent=pkt.info.decode(), power=pkt.dBm_AntSignal)

            # Probe request responses
            elif pkt.subtype == 5:
                pass
            
            # Beacons
            elif pkt.subtype == 8:
                print("Beacon with power " + str(pkt.dBm_AntSignal))
                DataManager().register_beacon_frame(bssid=pkt.addr3, ssid=pkt.info.decode())

            
            DataManager().register_management_frame(addr1=pkt.addr1,
                                                    addr2=pkt.addr2,
                                                    addr3=pkt.addr3,
                                                    addr4=pkt.addr4,
                                                    subtype=pkt.subtype,
                                                    power=pkt.dBm_AntSignal)
            

        # Control frames
        elif pkt.type == 1:

            bssid = pkt.addr1
            station_mac = pkt.addr1
            power = pkt.dBm_AntSignal

            DataManager().register_control_frame(
                bssid=bssid,
                station_mac=station_mac,
                power=power,
                subtype=str(pkt.subtype)
            )
            
            print("Control frame subtype " + str(pkt.subtype))


        # Data frames
        elif pkt.type == 2:

            bssid = get_bssid_from_pkt(pkt)
            station_mac = get_station_mac_from_pkt(pkt)
            power = pkt.dBm_AntSignal

            print("Data frame with power {pkt.dBm_AntSignal}".format(
                pkt=pkt))
            
            DataManager().register_data_frame(
                bssid=bssid,
                station_mac=station_mac,
                power=power,
                subtype=pkt.subtype
            )



def start_sniffer():
    try:
        sniff(iface="wlan1", prn=packet_handler, store=0)
    except Exception as e:
        print("--------")
        traceback.print_exc()
        start_sniffer()


if __name__ == "__main__":
    start_sniffer()
