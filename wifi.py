import time
import pywifi
from pywifi import const

def connect_to_wifi(ssid, password=None):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    # Save the current connected network
    if iface.status() == const.IFACE_CONNECTED:
        reconnect_ssid = iface.network_profiles()[0].ssid
    else:
        reconnect_ssid = None

    iface.disconnect()
    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK if password else const.AKM_TYPE_NONE)
    if password:
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(5)

    if iface.status() == const.IFACE_CONNECTED:
        print(f"Connected to {ssid}")
    else:
        print("Failed to connect")

    return reconnect_ssid

def disconnect_to_wifi(reconnect_ssid):
    if reconnect_ssid is not None:
        connect_to_wifi(reconnect_ssid)