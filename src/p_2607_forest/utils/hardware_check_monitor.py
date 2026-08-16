# display_checker.py
import ctypes
from ctypes import wintypes

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]

def check_all_monitors_scaling() -> bool:
    """
    연결된 모든 모니터의 DPI 배율을 확인합니다.
    - 모든 모니터가 100%인 경우: True 반환
    - 100%가 아닌 모니터가 있는 경우: 경고 팝업 후 False 반환
    """
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()

    monitors = []

    MONITORENUMPROC = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HMONITOR,
        wintypes.HDC,
        ctypes.POINTER(RECT),
        wintypes.LPARAM,
    )

    def enum_callback(hmonitor, hdc, lprect, lparam):
        dpi_x = wintypes.UINT()
        dpi_y = wintypes.UINT()
        result = ctypes.windll.shcore.GetDpiForMonitor(
            hmonitor, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y)
        )
        scale = round((dpi_x.value / 96.0) * 100) if result == 0 else 100
        monitors.append(scale)
        return True

    callback = MONITORENUMPROC(enum_callback)
    ctypes.windll.user32.EnumDisplayMonitors(0, 0, callback, 0)

    # 100%가 아닌 모니터가 하나라도 있는지 검사
    if any(scale != 100 for scale in monitors):
        monitor_status = "\n".join(
            [f"- 모니터 {i + 1}: {scale}%" for i, scale in enumerate(monitors)]
        )
        message = (
            "배율 100% 가 아닌 모니터가 감지되었습니다.\n\n"
            f"[배율 현황]\n{monitor_status}\n\n"
            "모든 모니터의 배율을 100% 로 설정해 주세요."
        )
        ctypes.windll.user32.MessageBoxW(0, message, "⚠️ 디스플레이 배율 경고", 0x30)
        return False

    return True

if __name__ == "__main__":
    if check_all_monitors_scaling():
        print("모든 모니터의 배율이 100%입니다.")
    else:
        print("100%가 아닌 모니터가 존재합니다.")