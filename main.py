from scapy.all import Dot11, Dot11Elt, sniff
import traceback
from data_manager import DataManager
import time
# Get the mac address of the wireless mobile device
# that we are interested in targeting

FILTER = "not wlan type ctl"


def get_station_mac_from_pkt(pkt):

    to_DS, from_DS = get_DS(pkt)

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

    to_DS, from_DS = get_DS(pkt)

    if not to_DS and not from_DS:
        return pkt.addr3
    elif not to_DS and from_DS:
        return pkt.addr2
    elif to_DS and not from_DS:
        return pkt.addr1
    elif to_DS and from_DS:
        return None


def get_DS(pkt):
    DS = pkt.FCfield & 0x3
    return DS & 0x1 != 0, DS & 0x2 != 0


def packet_handler(pkt):
    if pkt.haslayer(Dot11):

        # Management frames
        if pkt.type == 0:

            # Probe requests
            if pkt.subtype == 4:

                print("Probe request with MAC {pkt.addr2} and ssid {ssid}".format(
                    pkt=pkt, ssid=pkt.info.decode()))

                DataManager().register_probe_request_frame(
                    station_mac=pkt.addr2,
                    intent=pkt.info.decode(),
                    frequency=pkt.ChannelFrequency,
                    power=pkt.dBm_AntSignal
                )

            # Probe request responses
            elif pkt.subtype == 5:
                print("Probe response with MAC {pkt.addr2} and ssid {ssid}".format(
                    pkt=pkt, ssid=pkt.info.decode()))

                DataManager().register_probe_response_frame(
                    bssid=pkt.addr3,
                    ssid=pkt.info.decode(),
                    station_mac=pkt.addr1,
                    frequency=pkt.ChannelFrequency,
                    power=pkt.dBm_AntSignal
                )

            # Beacons
            elif pkt.subtype == 8:
                print("Beacon with power " + str(pkt.dBm_AntSignal))
                DataManager().register_beacon_frame(bssid=pkt.addr3, ssid=pkt.info.decode())

            DataManager().register_management_frame(addr1=pkt.addr1,
                                                    addr2=pkt.addr2,
                                                    addr3=pkt.addr3,
                                                    addr4=pkt.addr4,
                                                    subtype=pkt.subtype,
                                                    frequency=pkt.ChannelFrequency,
                                                    power=pkt.dBm_AntSignal,
                                                    )

        # Control frames
        elif pkt.type == 1:

            DataManager().register_control_frame(
                addr1=pkt.addr1,
                addr2=pkt.addr2,
                addr3=pkt.addr3,
                addr4=pkt.addr4,
                subtype=str(pkt.subtype),
                frequency=pkt.ChannelFrequency,
                power=pkt.dBm_AntSignal,
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
                subtype=pkt.subtype,
                frequency=pkt.ChannelFrequency,
                power=power,
            )


def start_sniffer():
    try:
        sniff(iface="wlan1", prn=packet_handler, store=0, filter=FILTER)
    except Exception as e:
        print("--------")
        traceback.print_exc()
        time.sleep(1)
        start_sniffer()


if __name__ == "__main__":
    start_sniffer()
