# DLLSearchOrderHijack
Example of a DLL Search Order Hijack



Windows searches for DLLs in the following order:
1. HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs
2. Application Directory
3. C:\Windows\System32
4. C:\Windows\System
5. C:\Windows
6. Current Directory
7. PATH variables directory


To test DLL Search Order Hijacking, place the "LegitDLL" in a folder further down in the search order. Then copy the "MaliciousDLL" and place it further up, then simply run the executable.
Try moving the 2 DLLs into different locations (from the list of options above) and see if the program runs differently.
