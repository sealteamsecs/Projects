#include <stdio.h>
#include <windows.h>

// Definition of the function prototype expected from the DLL
typedef DWORD (APIENTRY *pGetFileVersionInfoSize)(LPCSTR lptstrFilename, LPDWORD lpdwHandle);

int main() {
    HINSTANCE hDll;
    pGetFileVersionInfoSize GetFileVersionInfoSizeFunc;
    DWORD dwHandle;
    DWORD dwLen;

    // Load the DLL named "version.dll"
    hDll = LoadLibrary("version.dll");
    if (hDll == NULL) {
        printf("Failed to load version.dll\n");
        return 1;
    }

    // Get the address of the function "GetFileVersionInfoSize" from the DLL
    GetFileVersionInfoSizeFunc = (pGetFileVersionInfoSize) GetProcAddress(hDll, "GetFileVersionInfoSizeA");
    if (GetFileVersionInfoSizeFunc == NULL) {
        printf("Function GetFileVersionInfoSize not found in version.dll\n");
        FreeLibrary(hDll);
        return 1;
    }

    // Call the function
    dwLen = GetFileVersionInfoSizeFunc("C:\\Windows\\System32\\kernel32.dll", &dwHandle);
    if (dwLen == 0) {
        printf("Failed to get version info size.\n");
    } else {
        printf("Version info size for kernel32.dll: %u bytes\n", dwLen);
    }

    // Free the loaded DLL
    FreeLibrary(hDll);
    return 0;
}
