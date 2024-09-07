import ctypes
import time
import threading
lastR=""
lastL=""


PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Definir algumas constantes necessárias para a função SendInput
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
MAPVK_VK_TO_VSC = 0


pulo = 0x41 #a
dash = 0x42 #b
cima = 0X4B #c
baixo = 0x44 #d
anda_dir = 0x45 #e
anda_esq = 0x46 #f
diag_sup_esq = 0x47
diag_sup_dir = 0x48
diag_inf_esq = 0x49
diag_inf_dir = 0x4A
agarra = 0x4C
passa = 0x25

def press_key(hexKeyCode):
    try:
        if not isinstance(hexKeyCode, int):
            raise TypeError(f"hexKeyCode must be an integerz\n{hexKeyCode}")
        
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            hexKeyCode,
            ctypes.windll.user32.MapVirtualKeyA(hexKeyCode, MAPVK_VK_TO_VSC),
            0,
            0,
            ctypes.pointer(extra)
        )
        
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    except TypeError as e:
        print(f"Error in press_key: {e}")
    except ctypes.ArgumentError as e:
        print(f"Error in press_key: {e}")


def release_key(hexKeyCode):
    
    try:
        if not isinstance(hexKeyCode, int):
            raise TypeError(f"hexKeyCode must be an integer\n{hexKeyCode}")
        
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(
            hexKeyCode,
            ctypes.windll.user32.MapVirtualKeyA(hexKeyCode, MAPVK_VK_TO_VSC),
            2, # KEYEVENTF_KEYUP
            0,
            ctypes.pointer(extra)
        )
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    except TypeError as e:
        print(f"Error in release_key: {e} {hexKeyCode}")
    except ctypes.ArgumentError as e:
        print(f"Error in release_key: {e} {hexKeyCode}")

def press_and_release_key(comando, ultimoComando):
    if comando!=ultimoComando and ultimoComando == 0x25:
        press_key(comando)
    elif comando != ultimoComando and comando == dash:
        release_key(ultimoComando)
        press_key(comando)
        release_key(comando)
    else:
        release_key(ultimoComando)
        press_key(comando)
def checa_comandos_keys(comando,ultimoComando):
    if type(comando) == int:
        press_and_release_key(comando, ultimoComando)
        
       


class Mao():
    def __init__(self, dedos, pontos_mao, lado):
        self.dedos = dedos
        self.pontos_mao = pontos_mao
        self.lado = lado
    
    def verificaPolegar(self):
        if self.pontos_mao[4][1]> self.pontos_mao[0][1]:
            return baixo
        else:
            return cima
    
    def comando(self):
        match self.dedos:
            case [False, False, False, False, False]:
                return pulo
            case [False, True, True, False, False]:
                return agarra
            case [True, True, True, True, True]:
                return dash
            case [False, True, False, False, False]:
                if self.lado=="Esq":
                    return anda_esq
                elif self.lado == "Dir":    
                    return anda_dir
            case [True, False, False, False, False]:
                return self.verificaPolegar()
            case [True, True, False, False, False]:
                if self.lado=="Esq":
                    return diag_sup_esq
                else:    
                    return diag_sup_dir
            case [True, False, False, False, True]:
                if self.lado=="Esq":
                    return diag_inf_esq
                else:    
                    return diag_inf_dir
            case _:
                None
            
            
    def __str__(self) -> str:
        return f"{self.lado}: {self.dedos}"

def checa_comandos(mao1,mao2,ultimoComando1, ultimoComando2):
    
    esq=""
    dir=""
    if mao1 is not None and hasattr(mao1, 'comando'):
        esq = mao1.comando()

    if mao2 is not None and hasattr(mao2, 'comando'):
        dir = mao2.comando()
    if mao1 == ultimoComando1 and mao2 ==ultimoComando2:
        return
    comando = []
    comando.append(esq)
    comando.append(dir)
    if ultimoComando1== 0x25 and ultimoComando2== 0x25:
        comandEsq = threading.Thread(target=press_and_release_key,  args=(esq,ultimoComando1,))
        comandDir = threading.Thread(target=press_and_release_key,  args=(dir,ultimoComando2,))
        comandDir.start()
        comandEsq.start()
        comandDir.join()
        comandEsq.join()
    elif len(comando)==2:
        comandEsq = threading.Thread(target=checa_comandos_keys,  args=(esq,ultimoComando1,))
        comandDir = threading.Thread(target=checa_comandos_keys,  args=(dir,ultimoComando2,))
        comandDir.start()
        comandEsq.start()
    elif len(comando)==1 and esq != "":
        comandEsq = threading.Thread(target=checa_comandos_keys,  args=(esq,))
        comandEsq.start()
    elif len(comando)==1 and dir != "":
        comandDir = threading.Thread(target=checa_comandos_keys,  args=(dir,))
        comandDir.start()
    