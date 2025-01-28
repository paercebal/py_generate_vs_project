RBRBRBR_MAIN_FILE_HEADER_INCLUDE_RBRBRBR

#ifndef _WIN32

#include <Windows.h>

BOOL WINAPI DllMain(
   HINSTANCE hinstDLL,  // handle to DLL module
   DWORD fdwReason,     // reason for calling function
   LPVOID lpvReserved)  // reserved
{
   // Perform actions based on the reason for calling.
   switch(fdwReason) 
   {
      case DLL_PROCESS_ATTACH:
         // Initialize once for each new process.
         // Return FALSE to fail DLL load.
         break;

      case DLL_THREAD_ATTACH:
         // Do thread-specific initialization.
         break;

      case DLL_THREAD_DETACH:
         // Do thread-specific cleanup.
         break;

      case DLL_PROCESS_DETACH:

         if(lpvReserved != nullptr)
         {
            break; // do not do cleanup if process termination scenario
         }

         // Perform any necessary cleanup.
         break;
   }
   
   return TRUE;  // Successful DLL_PROCESS_ATTACH.
}

#endif // _WIN32


namespace RBRBRBR_MODULE_CPP_NAMESPACE_RBRBRBR {

RBRBRBR_MODULE_MACRO_PREFIX_RBRBRBR_x_API int get_value(int p_value)
{
   return p_value * 2;
}

} // namespace RBRBRBR_MODULE_CPP_NAMESPACE_RBRBRBR




