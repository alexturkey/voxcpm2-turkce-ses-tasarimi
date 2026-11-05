"""Vulkan kartının iş kümesi sınırına göre güvenli AudioVAE GPU dilim boyu (saniye).

Motorun ggml Vulkan kodu büyük bir hesabı parçalara bölmüyor: tek gönderimdeki iş kümesi sayısı kartın
maxComputeWorkGroupCount[0] sınırını aşarsa motor GGML_ASSERT ile durur. Intel HD 630'da bu sınır 65536,
NVIDIA GTX 1050 Ti'de 2147483647 (vulkaninfo, 2026-11-05). Varsayılan 10 sn dilim Intel'de ~10 sn'den uzun seste
aşıyordu (30 sn tasarım çöktü, 9 sn okuma geçti). Sınırı düşük kartta dilim küçülür; NVIDIA ve AMD'de 10 sn kalır.

Safe AudioVAE GPU chunk length from the Vulkan device's maxComputeWorkGroupCount[0]: low-limit GPUs (e.g. Intel
integrated, 65536) get a shorter chunk, high-limit GPUs (NVIDIA, AMD) keep 10 s. Reads the limit with ctypes,
no extra package; any failure keeps the default.
"""
import ctypes
import functools
import os
import re
import sys

VARSAYILAN_SN = 10.0   # NVIDIA, AMD ve CUDA: değişmez / unchanged default
DUSUK_SN = 5.0         # Intel HD 630'da 30 sn tasarımla doğrulandı / verified on Intel HD 630
DUSUK_SINIR = 1 << 20  # bu sınırın altındaki kart "düşük" sayılır / below this the device counts as low-limit

_TUR_GOMULU, _TUR_AYRIK, _TUR_CPU = 1, 2, 4
_STYPE_PROPS2, _STYPE_ID = 1000059001, 1000071004
_LIMITS = 296                        # VkPhysicalDeviceProperties.limits başlangıcı (8 bayt hizalı)
_PAYLASIMLI = _LIMITS + 216          # limits.maxComputeSharedMemorySize
_IS_KUMESI = _LIMITS + 220           # limits.maxComputeWorkGroupCount[0]


class _AppInfo(ctypes.Structure):
    _fields_ = [("sType", ctypes.c_int), ("pNext", ctypes.c_void_p), ("pApplicationName", ctypes.c_char_p),
                ("applicationVersion", ctypes.c_uint32), ("pEngineName", ctypes.c_char_p),
                ("engineVersion", ctypes.c_uint32), ("apiVersion", ctypes.c_uint32)]


class _InstanceInfo(ctypes.Structure):
    _fields_ = [("sType", ctypes.c_int), ("pNext", ctypes.c_void_p), ("flags", ctypes.c_uint32),
                ("pApplicationInfo", ctypes.POINTER(_AppInfo)), ("enabledLayerCount", ctypes.c_uint32),
                ("ppEnabledLayerNames", ctypes.c_void_p), ("enabledExtensionCount", ctypes.c_uint32),
                ("ppEnabledExtensionNames", ctypes.c_void_p)]


class _IdProps(ctypes.Structure):
    _fields_ = [("sType", ctypes.c_int), ("pNext", ctypes.c_void_p), ("deviceUUID", ctypes.c_ubyte * 16),
                ("driverUUID", ctypes.c_ubyte * 16), ("deviceLUID", ctypes.c_ubyte * 8),
                ("deviceNodeMask", ctypes.c_uint32), ("deviceLUIDValid", ctypes.c_uint32)]


class _Props2(ctypes.Structure):
    _fields_ = [("sType", ctypes.c_int), ("pNext", ctypes.c_void_p), ("properties", ctypes.c_ubyte * 1024)]


def _kitaplik():
    if sys.platform == "win32":
        return ctypes.WinDLL("vulkan-1")
    if sys.platform.startswith("linux"):
        return ctypes.CDLL("libvulkan.so.1")
    raise OSError("bu platformda Vulkan sınır okuması yok / no Vulkan limit query on this platform")


@functools.lru_cache(maxsize=1)
def _ham_aygitlar() -> tuple:
    """Vulkan'ın ham sırasıyla bütün fiziksel aygıtlar (süreç başına bir kez sorgulanır).
    All physical devices in raw Vulkan order, queried once per process."""
    vk = _kitaplik()
    try:
        vk.vkCreateInstance.argtypes = [ctypes.POINTER(_InstanceInfo), ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]
        vk.vkEnumeratePhysicalDevices.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_void_p]
        vk.vkGetPhysicalDeviceProperties2.argtypes = [ctypes.c_void_p, ctypes.POINTER(_Props2)]
        vk.vkGetPhysicalDeviceProperties2.restype = None
        vk.vkDestroyInstance.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        vk.vkDestroyInstance.restype = None
    except AttributeError as hata:  # Vulkan 1.1 öncesi yükleyici / pre-1.1 loader
        raise OSError(f"Vulkan işlevi yok / missing Vulkan function: {hata}") from hata
    uygulama = _AppInfo(0, None, b"ses_tasarim", 1, b"ses_tasarim", 1, (1 << 22) | (2 << 12))  # Vulkan 1.2
    bilgi = _InstanceInfo(1, None, 0, ctypes.pointer(uygulama), 0, None, 0, None)
    ornek = ctypes.c_void_p()
    if vk.vkCreateInstance(ctypes.byref(bilgi), None, ctypes.byref(ornek)) != 0:
        raise OSError("vkCreateInstance başarısız / failed")
    try:
        sayi = ctypes.c_uint32(0)
        if vk.vkEnumeratePhysicalDevices(ornek, ctypes.byref(sayi), None) != 0:
            raise OSError("vkEnumeratePhysicalDevices başarısız / failed")
        tutamaklar = (ctypes.c_void_p * sayi.value)()
        if vk.vkEnumeratePhysicalDevices(ornek, ctypes.byref(sayi), tutamaklar) not in (0, 5):  # 5 = VK_INCOMPLETE
            raise OSError("vkEnumeratePhysicalDevices başarısız / failed")
        hepsi = []
        for tutamak in tutamaklar[:sayi.value]:
            kimlik = _IdProps(_STYPE_ID, None)
            ozellik = _Props2(_STYPE_PROPS2, ctypes.cast(ctypes.pointer(kimlik), ctypes.c_void_p))
            vk.vkGetPhysicalDeviceProperties2(tutamak, ctypes.byref(ozellik))
            ham = bytes(ozellik.properties)
            hepsi.append({
                "ad": ham[20:276].split(b"\0", 1)[0].decode("utf-8", "replace"),
                "tur": int.from_bytes(ham[16:20], "little"),
                "is_kumesi": int.from_bytes(ham[_IS_KUMESI:_IS_KUMESI + 4], "little"),
                "paylasimli_bellek": int.from_bytes(ham[_PAYLASIMLI:_PAYLASIMLI + 4], "little"),
                "_uuid": bytes(kimlik.deviceUUID),
                "_luid": bytes(kimlik.deviceLUID) if kimlik.deviceLUIDValid else None,
            })
    finally:
        vk.vkDestroyInstance(ornek, None)
    return tuple(hepsi)


def sirala(hepsi, gorunur=None) -> list:
    """ggml-vulkan'ın motor numarası sırası. GGML_VK_VISIBLE_DEVICES verilmişse ggml ham sıradaki o numaraları
    aynen kullanır. Verilmemişse: yalnız ayrık ve gömülü kartlar, aynı kartın ikinci kaydı (UUID/LUID) atlanır; hiç
    yoksa CPU olmayan ilk aygıt. Burada olmayanlar (nadir): ggml'in özellik denetimi (is_supported, yalnız çok eski
    kartları eler) ve aynı kartın iki sürücü kaydında sürücü önceliği.
    Order of ggml-vulkan device numbers (honours GGML_VK_VISIBLE_DEVICES like ggml does)."""
    hepsi = list(hepsi)
    if gorunur:
        return [_dis(hepsi[int(n)]) for n in gorunur.replace(",", " ").split() if 0 <= int(n) < len(hepsi)]
    secili = []
    for aygit in hepsi:
        if aygit["tur"] not in (_TUR_GOMULU, _TUR_AYRIK):
            continue
        if any(a["_uuid"] == aygit["_uuid"] or (aygit["_luid"] and a["_luid"] == aygit["_luid"]) for a in secili):
            continue
        secili.append(aygit)
    if not secili:
        secili = [a for a in hepsi if a["tur"] != _TUR_CPU][:1]
    return [_dis(a) for a in secili]


def _dis(aygit: dict) -> dict:
    return {k: v for k, v in aygit.items() if not k.startswith("_")}


def aygitlar() -> list:
    """Motorun numaraladığı sırada kartlar: [{ad, tur, is_kumesi, paylasimli_bellek}].
    Devices in the order the engine numbers them."""
    return sirala(_ham_aygitlar(), os.environ.get("GGML_VK_VISIBLE_DEVICES"))


def _numara(cihaz) -> int:
    numara = int(cihaz) if cihaz not in (None, "") else 0
    if numara < 0:
        raise ValueError(f"cihaz negatif olamaz / device must be >= 0: {cihaz}")
    return numara


def dilim_sn(settings: dict, liste=None) -> tuple:
    """(dilim saniyesi, seçilen kartın adı ya da None). Vulkan dışında ya da sınır okunamazsa 10 sn.
    Returns (chunk seconds, chosen device name or None); anything but a readable low-limit Vulkan device keeps 10 s."""
    if settings.get("backend", "cuda") != "vulkan":
        return VARSAYILAN_SN, None
    try:
        liste = aygitlar() if liste is None else liste
        aygit = liste[_numara(settings.get("cihaz"))]
    except Exception:  # noqa: BLE001 - sürücü yok, kitaplık yok, numara dışı: varsayılan kalır
        return VARSAYILAN_SN, None
    sinir = aygit.get("is_kumesi") or 0
    return (DUSUK_SN if 0 < sinir < DUSUK_SINIR else VARSAYILAN_SN), aygit.get("ad")


def motor_adi(stdout_metni: str, cihaz):
    """Motorun kendi listesinden seçili kartın adı ('ggml_vulkan: 1 = NVIDIA ... (NVIDIA) | ...'); bulunamazsa None.
    Name of the chosen device as the engine itself printed it, or None."""
    try:
        numara = _numara(cihaz)
    except ValueError:
        return None
    for satir in stdout_metni.splitlines():
        eslesme = re.match(r"ggml_vulkan: (\d+) = (.+?) \([^()]*\) \|", satir)
        if eslesme and int(eslesme.group(1)) == numara:
            return eslesme.group(2).strip()
    return None
