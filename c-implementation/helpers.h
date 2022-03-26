#ifndef HELPERS_H
#define HELPERS_H

#include <tins/tins.h>
#include <json.hpp>
#include "main.h"
#include <regex>
#include <thread>

using json = nlohmann::json;

int getCurrentTime();

mac getStationMAC(Tins::Dot11Data *frame);

bool isMacFake(mac address);

bool isMacValid(mac address);

json postJSON(string url, json j);

json getJSON(string url);

void channel_switcher(string interface);

void set_monitor_mode(string interface);

bool is_monitor_mode(string interface);

size_t curlWriteCallback(void *contents, size_t size, size_t nmemb, std::string *s);

#endif