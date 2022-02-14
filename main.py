from audioop import add
from sunau import AUDIO_FILE_ENCODING_LINEAR_24
from scapy.all import Dot11, Dot11ProbeReq, Dot11Beacon, sniff
import traceback
from data_manager import DataManager

# Get the mac address of the wireless mobile device
# that we are interested in targeting
def get_station_mac_from_pkt(pkt):

    DS = pkt.FCfield & 0x3
    to_DS = DS & 0x1 != 0
    from_DS = DS & 0x2 != 0

    if not to_DS and not from_DS:
        return pkt.addr2
    elif not to_DS and from_DS:
        return pkt.addr1
    elif to_DS and not from_DS:
        return pkt.addr2
    elif to_DS and from_DS:
        return None


# Get the mac address of the bssid (ap mac address)
def get_bssid_from_pkt(pkt):

    DS = pkt.FCfield & 0x3
    to_DS = DS & 0x1 != 0
    from_DS = DS & 0x2 != 0

    if not to_DS and not from_DS:
        return pkt.addr3
    elif not to_DS and from_DS:
        return pkt.addr2
    elif to_DS and not from_DS:
        return pkt.addr1
    elif to_DS and from_DS:
        return None

    

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
