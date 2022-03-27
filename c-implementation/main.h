#ifndef MAIN_H
#define MAIN_H

#include <tins/tins.h>

#include <bitset>
#include <string>
#include <vector>
#include <mutex>
#include <atomic>
#include <unordered_set>

using namespace std;
using namespace Tins;

extern bool debugMode;

typedef HWAddress<6> mac;

struct ProbeRequest {
    string stationMac;
    string intent;
    string time;
    int frequency;
    int power;
};

struct UploadJSONData {
    string deviceID;
    std::vector<ProbeRequest> probeRequests;
};


struct MacMetadata {
    int detectionCount;
    double averageSignalStrenght;
    string signature;
    vector<int> typeCount;
};


class PacketManager {
   private:
    map<mac, MacMetadata>* detectedMacs;
    unordered_set<mac>* personalMacs;
    bool disableBackendUpload = false;
    int currentWindowStartTime;
    mutex uploadingMutex;
    bool showPackets;
    string deviceID;
    int secondsPerWindow;

    void uploadToBackend();

    void uploader();

    void syncPersonalMacs();

    void countDevice(mac macAddress, double signalStrength, int type);

    void countPossibleDevice(mac macAddress, double signalStrength);

    void registerManagement(Dot11ManagementFrame *managementFrame, double signalStrength);

    void registerControl(Dot11Control *controlFrame, double signalStrength);

    void registerData(Dot11Data *dataFrame, double signalStrength);

   public:
    PacketManager(bool uploadBackend, string deviceID, bool showPackets, int secondsPerWindow);

    void registerFrame(Packet frame);

};

#endif