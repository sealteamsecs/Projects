#include <stdio.h>
#include <windows.h>

typedef char * (HelloFunction)(char*);
typedef void (*HelloWorldFunction)();

int main(int argc, char *argv[])
{
	HINSTANCE hinstDLL;
	hinstDLL = LoadLibrary("SearchOrderDLL.dll"); //Look for SearchOrderDLL.dll
	
	if(hinstDLL != 0)
	{

		HelloWorldFunction helloworld;
		helloworld = (HelloWorldFunction) GetProcAddress(hinstDLL,"HelloWorld");		
		helloworld(); //Call the HelloWorld function
		FreeLibrary(hinstDLL);
		
	}
	else
		printf("Not able to find DLL: Err #%d", GetLastError());
	getchar();
	return 0;
	
}
