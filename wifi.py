import time
import pywifi
from pywifi import const

def connect_to_wifi(ssid, password=None):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(1)
    scan_results = iface.scan_results()

    for result in scan_results:
        if result.ssid == ssid:
            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK if password else const.AKM_TYPE_NONE)
            if password:
                profile.cipher = const.CIPHER_TYPE_CCMP
                profile.key = password

            tmp_profile = iface.add_network_profile(profile)
            iface.connect(tmp_profile)
            time.sleep(5)
            
            if iface.status() == const.IFACE_CONNECTED:
                print(f"와이파이 '{ssid}'에 연결되었습니다.")
                return True
            else:
                print("와이파이 연결에 실패했습니다.")
                return False

    print(f"와이파이 '{ssid}'를 찾을 수 없습니다.")
    return False
