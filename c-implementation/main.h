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

const int RECORD_SIZE = 15;
const int WINDOW_TIME = 60;
const float ACTIVITY_PERCENTAGE = 0.6;
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
    int averageSignalStrenght;
    string signature;
    vector<int> typeCount;
};


class PacketManager {
   private:
    map<mac, MacMetadata>* detectedMacs;
    unordered_set<mac>* personalDeviceMacs;
    bool disableBackendUpload = false;
    int currentStateStartTime;
    mutex uploadingMutex;
    bool showPackets;
    string deviceID;

    void uploadToBackend();

    void uploader();

    void countDevice(mac macAddress, int signalStrength, int type);

    void countPossibleDevice(mac macAddress, int signalStrength);

    void registerManagement(Dot11ManagementFrame *managementFrame, int signalStrength);

    void registerControl(Dot11Control *controlFrame, int signalStrength);

    void registerData(Dot11Data *dataFrame, int signalStrength);

   public:
    PacketManager(bool uploadBackend, string deviceID, bool showPackets);

    void registerFrame(Packet frame);

};

#endif