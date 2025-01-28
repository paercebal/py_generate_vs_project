#include <RBRBRBR_NAMESPACE_NAME_RBRBRBR.RBRBRBR_MODULE_NAME_RBRBRBR/main.hpp>
#include <iostream>
RBRBRBR_GTEST_INCLUDE_RBRBRBR

RBRBRBR_GTEST_GLOBAL_DATA_RBRBRBR

int main(int argc, char * argv[])
{
   RBRBRBR_GTEST_LAUNCH_ALL_TEST_FUNCTION_RBRBRBR

   //return RBRBRBR_NAMESPACE_NAME_RBRBRBR::RBRBRBR_MODULE_NAME_RBRBRBR::pause(0) ;
}

namespace RBRBRBR_NAMESPACE_NAME_RBRBRBR {
namespace RBRBRBR_MODULE_NAME_RBRBRBR {

int pause(int p_value)
{
   std::cout << "\nPress RETURN to continue..." << std::endl ;
   std::cin.ignore() ;
   return p_value ;
}

} // namespace RBRBRBR_MODULE_NAME_RBRBRBR
} // namespace RBRBRBR_NAMESPACE_NAME_RBRBRBR

