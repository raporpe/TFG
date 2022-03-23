#ifndef MAIN_H
#define MAIN_H

#include <tins/tins.h>

#include <bitset>
#include <string>
#include <vector>

using namespace std;
using namespace Tins;

const int WINDOW_SIZE = 15;
const int FRAME_TIME = 60;
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

struct RecordObject {
    bitset<WINDOW_SIZE> record;
    int signalStrength;
};



class PacketManager {
   private:
    vector<Dot11ProbeResponse> probeResponses;
    vector<Dot11ProbeRequest> probeRequests;
    int currentSecond = 0;
    map<mac, RecordObject> store;
    bool uploadBackend = false;
    string deviceID;

    void uploadToBackend();

    void checkTimeIncrease();

    void addAndTickMac(mac macAddress, int signalStrength);

    void tickMac(mac macAddress, int signalStrength);

    int getActiveDevices();

   public:
    PacketManager(bool uploadBackend, string deviceID);

    void registerProbeRequest(Dot11ProbeRequest *frame, int signalStrength);

    void registerProbeResponse(Dot11ProbeResponse *frame, int signalStrength);

    void registerControl(Dot11Control *frame, int signalStrength);

    void registerData(Dot11Data *frame, int signalStrength);

};

#endif