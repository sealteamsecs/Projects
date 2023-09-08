/* Replace "dll.h" with the name of your header */
#include "dll.h"
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
DLLIMPORT void HelloWorld()
{
	printf("This is a 'malicious' DLL.");
	system("c:\\windows\\system32\\calc");

}


