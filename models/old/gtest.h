#ifndef GTEST_H_AE554D8E_2DB7_4759_B0AD_C397807D7AB5
#define GTEST_H_AE554D8E_2DB7_4759_B0AD_C397807D7AB5

#include <iostream>
#include <sstream>
#include <string>
#include <map>
#include <vector>
#include <utility>
#include <cstring>
#include <cstdlib>
#include <cctype>

#include <conmanip/conmanip.hpp>


namespace testing
{

class Test
{
public:
   Test() {}
   ~Test() {}

   virtual void ExecuteTestBody() = 0;
   virtual void SetUp() {}
   virtual void TearDown() {}

   void ExecuteTest()
   {
      this->SetUp();
      this->ExecuteTestBody();
      this->TearDown();
   }

private:
   Test(const Test &) {}
   Test & operator = (const Test &) { return *this; }

};

}

namespace gtest
{
;

#ifdef _MSC_VER
#define GTEST_DEBUG_BREAK __debugbreak()
#else
#define GTEST_DEBUG_BREAK std::abort()
#endif

#ifdef _MSC_VER
#else

inline int _stricmp(const char * a, const char * b)
{
   while(*a && *b && (std::tolower(*a) == std::tolower(*b)))
   {
      ++a; ++b;
   }

   return std::tolower(*a) - std::tolower(*b) ;
}

inline int _wcsicmp(const wchar_t * a, const wchar_t * b)
{
   while(*a && *b && (std::tolower(*a) == std::tolower(*b)))
   {
      ++a; ++b;
   }

   return std::tolower(*a) - std::tolower(*b);
}



#endif





class AssertData
{
public :

   typedef void (TestFunction)() ;
   typedef std::vector< std::pair<TestFunction *, std::string> > TestFunctionVector;
   typedef std::vector< std::pair<testing::Test *, std::string> > TestClassVector;

   typedef std::map<std::string, TestFunction *> NameFunctionMap;
   typedef std::map<std::string, NameFunctionMap> FullNameFunctionMap;

   typedef std::map<std::string, testing::Test *> NameClassMap;
   typedef std::map<std::string, NameClassMap> FullNameClassMap;

   AssertData()
      : m_testCount(0)
      , m_errorCount(0)
      , m_testGroupCount(0)
      , m_testGroupErrorCount(0)
      , m_isErrorRaised(false)
   {
   }

   void registerTestFunction(TestFunction * p_function, const std::string & p_functionName)
   {
      this->m_testFunction.push_back(std::make_pair(p_function, p_functionName));
   }

   void registerTestFunction(TestFunction * p_function, const std::string & p_prefix, const std::string & p_suffix)
   {
      this->m_mapFunction[p_prefix][p_suffix] = p_function;
      //FullNameFunctionMap m_mapFunction;
      //FullNameClassMap m_mapClass;
   }

   template <typename T>
   void registerTestClass(const std::string & p_className)
   {
      this->m_testClass.push_back(std::make_pair(static_cast<testing::Test *>(new T()), p_className));
   }

   template <typename T>
   void registerTestClass(const std::string & p_prefix, const std::string & p_suffix)
   {
      this->m_mapClass[p_prefix][p_suffix] = new T();
   }

   size_t getCountTestCase() const
   {
      return this->m_mapFunction.size() + this->m_mapClass.size();
   }

   size_t getCountTestFull() const
   {
      size_t total = 0 ;

      for(FullNameFunctionMap::const_iterator itFull = this->m_mapFunction.begin(), itFullEnd = this->m_mapFunction.end(); itFull != itFullEnd; ++itFull)
      {
         total += itFull->second.size();
      }

      for(FullNameClassMap::const_iterator itFull = this->m_mapClass.begin(), itFullEnd = this->m_mapClass.end(); itFull != itFullEnd; ++itFull)
      {
         total += itFull->second.size();
      }

      return total;
   }

   void printFullTestBegin(conmanip::console_out_context & p_ctxout)
   {
      using namespace conmanip;

      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[==============================]" << std::endl;
      std::cout << "[=            GTEST           =]" << std::endl;
      std::cout << "[==============================]" << std::endl;
      p_ctxout.restore();
      std::cout << std::endl;

      std::cout << std::endl;
      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[==========]";
      p_ctxout.restore();
      std::cout << " " << this->getCountTestFull() << " test(s) from " << this->getCountTestCase() << " test cases to be run." << std::endl;
      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[----------]";
      p_ctxout.restore();
      std::cout << std::endl;
      std::cout << std::endl;
   }

   void printFullTestEnd(conmanip::console_out_context & p_ctxout)
   {
      using namespace conmanip;

      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[----------]";
      p_ctxout.restore();
      std::cout << std::endl;
      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[==========]";
      p_ctxout.restore();
      std::cout << " " << this->getCountTestFull() << " test(s) from " << this->getCountTestCase() << " test cases ran. (done)" << std::endl;
      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[  PASSED  ]";
      p_ctxout.restore();
      std::cout << " " << (this->getTestGroupCount() - this->getTestGroupErrorCount()) << " test(s)" << std::endl ;

      if(this->getTestGroupErrorCount() > 0)
      {
         std::cout << settextcolor(console_text_colors::light_red);
         std::cout << "[  FAILED  ]";
         p_ctxout.restore();
         std::cout << " " << this->getTestGroupErrorCount() << " test(s), listed below:" << std::endl;

         for(size_t i = 0, iMax = this->m_testGroupFailed.size(); i < iMax; ++i)
         {
            std::cout << settextcolor(console_text_colors::light_red);
            std::cout << "[  FAILED  ]";
            p_ctxout.restore();
            std::cout << " " << this->m_testGroupFailed[i] << std::endl;
         }

         std::cout << std::endl;
         std::cout << "Conclusion: " << this->m_testCount << " assertions(s), with " << this->m_errorCount << " failed" << std::endl;
         std::cout << std::endl ;
         std::cout << " " << this->getTestGroupErrorCount() << " FAILED TESTS" << std::endl;
         std::cout << std::endl;
      }
      else
      {
         std::cout << std::endl;
         std::cout << "Conclusion: " << this->m_testCount << " assertions(s), with " << this->m_errorCount << " assertions(s) failed" << std::endl;
         std::cout << std::endl;
      }
   }

   void printTestCaseBegin(conmanip::console_out_context & p_ctxout, const std::string & p_prefix, size_t testCount)
   {
      using namespace conmanip;

      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[----------]";
      p_ctxout.restore();
      std::cout << " " << testCount << " test(s) from " << p_prefix << std::endl;
   }

   void printTestCaseEnd(conmanip::console_out_context & p_ctxout, const std::string & p_prefix, size_t testCount)
   {
      using namespace conmanip;

      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[----------]";
      p_ctxout.restore();
      std::cout << " " << testCount << " test(s) from " << p_prefix << " (done)" << std::endl;
      std::cout << std::endl;
   }

   void printTestBegin(conmanip::console_out_context & p_ctxout, const std::string & p_prefix, const std::string & p_suffix)
   {
      using namespace conmanip;

      std::cout << settextcolor(console_text_colors::light_green);
      std::cout << "[ RUN      ]";
      p_ctxout.restore();
      std::cout << " " << p_prefix << "." << p_suffix << std::endl;
   }

   void printTestEnd(conmanip::console_out_context & p_ctxout, const std::string & p_prefix, const std::string & p_suffix)
   {
      using namespace conmanip;

      std::string name = p_prefix + "." + p_suffix;

      if(this->isErrorRaised())
      {
         std::cout << settextcolor(console_text_colors::light_red);
         std::cout << "[  FAILED  ]";
         p_ctxout.restore();
         m_testGroupFailed.push_back(name);
      }
      else
      {
         std::cout << settextcolor(console_text_colors::light_green);
         std::cout << "[       OK ]";
         p_ctxout.restore();
      }

      std::cout << " " << name << " (done)" << std::endl;
   }

   void launchAllTestFunction()
   {
      using namespace conmanip;

      console_out_context ctxout;

      launchAllTestFunction(ctxout);
   }

   void launchAllTestFunction(conmanip::console_out_context & p_ctxout)
   {
      using namespace conmanip;

      size_t count = 0 ;

      this->printFullTestBegin(p_ctxout);

      for(FullNameFunctionMap::iterator itFull = this->m_mapFunction.begin(), itFullEnd = this->m_mapFunction.end(); itFull != itFullEnd; ++itFull)
      {
         const std::string & prefix = itFull->first;

         this->printTestCaseBegin(p_ctxout, prefix, itFull->second.size());

         for(NameFunctionMap::iterator it = itFull->second.begin(), itEnd = itFull->second.end(); it != itEnd; ++it)
         {
            const std::string & suffix = it->first;
            TestFunction * testFunction = it->second;
            this->printTestBegin(p_ctxout, prefix, suffix) ;
            this->resetErrorRaised();
            (*testFunction)();
            this->printTestEnd(p_ctxout, prefix, suffix);
            ++count;
         }

         this->printTestCaseEnd(p_ctxout, prefix, itFull->second.size());
      }

      for(FullNameClassMap::iterator itFull = this->m_mapClass.begin(), itFullEnd = this->m_mapClass.end(); itFull != itFullEnd; ++itFull)
      {
         const std::string & prefix = itFull->first;

         this->printTestCaseBegin(p_ctxout, prefix, itFull->second.size());

         for(NameClassMap::iterator it = itFull->second.begin(), itEnd = itFull->second.end(); it != itEnd; ++it)
         {
            const std::string & suffix = it->first;
            testing::Test * testClass = it->second;
            this->printTestBegin(p_ctxout, prefix, suffix);
            this->resetErrorRaised();
            (*testClass).ExecuteTest();
            this->printTestEnd(p_ctxout, prefix, suffix);
            ++count;
         }

         this->printTestCaseEnd(p_ctxout, prefix, itFull->second.size());
      }

      this->printFullTestEnd(p_ctxout);
   }

   size_t getTestCount() { return this->m_testCount; }
   size_t getErrorCount() { return this->m_errorCount; }

   size_t getTestGroupCount() { return this->m_testGroupCount; }
   size_t getTestGroupErrorCount() { return this->m_testGroupErrorCount; }

   void doSucceed(bool p_isFatal, const char * p_function, const int p_line)
   {
      incrementTestCount() ;
   }

   void doFail(bool p_isFatal, const char * p_function, const int p_line)
   {
      incrementTestCount() ;

      incrementErrorCount() ;
      std::cout << "Error in " << p_function << ", line " << p_line << " :\n" ;

      if(p_isFatal)
      {
         GTEST_DEBUG_BREAK;
      }
   }

   template<typename T_Operand>
   void doAssertTrue(bool p_isFatal, const char * p_operandName, const T_Operand & p_operand, const char * p_function, const int p_line)
   {
      incrementTestCount() ;

      if(p_operand)
      {
      }
      else
      {
         incrementErrorCount() ;
         std::cout << "Error in " << p_function << ", line " << p_line << " :\n" ;
         std::cout << "   => (" << p_operandName << " is not true" << std::endl ;
         std::cout << "      - " << p_operandName << " : [" << p_operand << "]" << std::endl ;

         if(p_isFatal)
         {
            GTEST_DEBUG_BREAK;
         }
      }
   }

   template<typename T_Operand>
   void doAssertFalse(bool p_isFatal, const char * p_operandName, const T_Operand & p_operand, const char * p_function, const int p_line)
   {
      incrementTestCount() ;

      if(!p_operand)
      {
      }
      else
      {
         incrementErrorCount() ;
         std::cout << "Error in " << p_function << ", line " << p_line << " :\n" ;
         std::cout << "   => (" << p_operandName << " is not false" << std::endl ;
         std::cout << "      - " << p_operandName << " : [" << p_operand << "]" << std::endl ;

         if(p_isFatal)
         {
            GTEST_DEBUG_BREAK;
         }
      }
   }

   template<typename T_Left, typename T_Right>
   void doAssert(bool p_isFatal, const char * p_leftName, const char * p_operator, const char * p_rightName, const T_Left & p_left, const T_Right & p_right, const char * p_function, const int p_line)
   {
      std::cout << "Error in " << p_function << ", line " << p_line << " :\n" ;
      std::cout << "   => (" << p_leftName << " " << p_operator << " " << p_rightName << ") is not true" << std::endl ;
      std::cout << "      - " << p_leftName << " : [" << p_left << "]" << std::endl ;
      std::cout << "      - " << p_rightName << " : [" << p_right << "]" << std::endl ;

      if(p_isFatal)
      {
         GTEST_DEBUG_BREAK;
      }
   }

   template<typename T_Left, typename T_Right>
   void doAssertEqual(bool p_isFatal, const char * p_leftName, const char * p_rightName, const T_Left & p_left, const T_Right & p_right, const char * p_function, const int p_line)
   {
      incrementTestCount() ;

      if(p_left == p_right)
      {
      }
      else
      {
         incrementErrorCount() ;
         doAssert(p_isFatal, p_leftName, "==", p_rightName, p_left, p_right, p_function, p_line) ;
      }
   }

   template<typename T_Left, typename T_Right>
   void doAssertNotEqual(bool p_isFatal, const char * p_leftName, const char * p_rightName, const T_Left & p_left, const T_Right & p_right, const char * p_function, const int p_line)
   {
      incrementTestCount() ;

      if(p_left != p_right)
      {
      }
      else
      {
         incrementErrorCount() ;
         doAssert(p_isFatal, p_leftName, "!=", p_rightName, p_left, p_right, p_function, p_line) ;
      }
   }

   template<typename T_Left, typename T_Right>
   void doAssertLesser(bool p_isFatal, const char * p_leftName, const char * p_rightName, const T_Left & p_left, const T_Right & p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left < p_right)
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "<", p_rightName, p_left, p_right, p_function, p_line);
      }
   }

   template<typename T_Left, typename T_Right>
   void doAssertLesserOrEqual(bool p_isFatal, const char * p_leftName, const char * p_rightName, const T_Left & p_left, const T_Right & p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left <= p_right)
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "<=", p_rightName, p_left, p_right, p_function, p_line);
      }
   }

   template<typename T_Left, typename T_Right>
   void doAssertGreater(bool p_isFatal, const char * p_leftName, const char * p_rightName, const T_Left & p_left, const T_Right & p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left > p_right)
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, ">", p_rightName, p_left, p_right, p_function, p_line);
      }
   }

   template<typename T_Left, typename T_Right>
   void doAssertGreaterOrEqual(bool p_isFatal, const char * p_leftName, const char * p_rightName, const T_Left & p_left, const T_Right & p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left >= p_right)
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, ">=", p_rightName, p_left, p_right, p_function, p_line);
      }
   }

   void doAssertEqualCString(bool p_isFatal, const char * p_leftName, const char * p_rightName, const char * p_left, const char * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left == p_right)
      {
      }
      else if ((p_left) && (p_right) && (strcmp(p_left, p_right) == 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstr}==", p_rightName, p_left, p_right, p_function, p_line);
      }
   }

   void doAssertNotEqualCString(bool p_isFatal, const char * p_leftName, const char * p_rightName, const char * p_left, const char * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left != p_right)
      {
      }
      else if ((! p_left) || (! p_right) || (strcmp(p_left, p_right) != 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstr}!=", p_rightName, p_left, p_right, p_function, p_line);
      }
   }
   /*
   void doAssertEqualCString(bool p_isFatal, const char * p_leftName, const char * p_rightName, const wchar_t * p_left, const wchar_t * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left == p_right)
      {
      }
      else if ((p_left) && (p_right) && (wcscmp(p_left, p_right) == 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstr}==", p_rightName, p_left, p_right, p_function, p_line);
      }
   }
   
   void doAssertNotEqualCString(bool p_isFatal, const char * p_leftName, const char * p_rightName, const wchar_t * p_left, const wchar_t * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left != p_right)
      {
      }
      else if ((!p_left) || (!p_right) || (wcscmp(p_left, p_right) != 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstr}!=", p_rightName, p_left, p_right, p_function, p_line);
      }
   }
   */
   void doAssertEqualCStringCase(bool p_isFatal, const char * p_leftName, const char * p_rightName, const char * p_left, const char * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left == p_right)
      {
      }
      else if ((p_left) && (p_right) && (_stricmp(p_left, p_right) == 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstri}==", p_rightName, p_left, p_right, p_function, p_line);
      }
   }

   void doAssertNotEqualCStringCase(bool p_isFatal, const char * p_leftName, const char * p_rightName, const char * p_left, const char * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left != p_right)
      {
      }
      else if ((!p_left) || (!p_right) || (_stricmp(p_left, p_right) != 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstri}!=", p_rightName, p_left, p_right, p_function, p_line);
      }
   }
   /*
   void doAssertEqualCStringCase(bool p_isFatal, const char * p_leftName, const char * p_rightName, const wchar_t * p_left, const wchar_t * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left == p_right)
      {
      }
      else if ((p_left) && (p_right) && (_wcsicmp(p_left, p_right) == 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstri}==", p_rightName, p_left, p_right, p_function, p_line);
      }
   }

   void doAssertNotEqualCStringCase(bool p_isFatal, const char * p_leftName, const char * p_rightName, const wchar_t * p_left, const wchar_t * p_right, const char * p_function, const int p_line)
   {
      incrementTestCount();

      if (p_left != p_right)
      {
      }
      else if ((!p_left) || (!p_right) || (_wcsicmp(p_left, p_right) != 0))
      {
      }
      else
      {
         incrementErrorCount();
         doAssert(p_isFatal, p_leftName, "{cstri}!=", p_rightName, p_left, p_right, p_function, p_line);
      }
   }
   */

private :

   void incrementTestCount() { ++this->m_testCount ; }
   void incrementErrorCount()
   {
      ++this->m_errorCount ;
      if(this->m_isErrorRaised == false)
      {
         this->m_isErrorRaised = true ;
         this->m_testGroupErrorCount += 1 ;
      }
   }
   void resetErrorRaised()
   {
      this->m_isErrorRaised = false;
      this->m_testGroupCount += 1 ;
   }
   bool isErrorRaised() { return this->m_isErrorRaised ; }

   std::vector<std::string> m_testGroupFailed;
   size_t m_testCount ;
   size_t m_errorCount ;
   size_t m_testGroupCount;
   size_t m_testGroupErrorCount;
   bool m_isErrorRaised ;
   TestFunctionVector m_testFunction;
   TestClassVector m_testClass;

   FullNameFunctionMap m_mapFunction;
   FullNameClassMap m_mapClass;
} ;

AssertData & getAssertData() ;

struct TestFunctionRegistrator
{
   TestFunctionRegistrator(gtest::AssertData::TestFunction * p_function, const char * p_prefix, const char * p_suffix)
   {
      std::string functionName(p_prefix) ;
      functionName += "." ;
      functionName += p_suffix ;
      gtest::getAssertData().registerTestFunction(p_function, functionName) ;
      gtest::getAssertData().registerTestFunction(p_function, p_prefix, p_suffix);
   }
} ;

template <typename T>
struct TestClassRegistrator
{
   TestClassRegistrator(const char * p_prefix, const char * p_suffix)
   {
      std::string className(p_prefix);
      className += ".";
      className += p_suffix;
      gtest::getAssertData().registerTestClass<T>(className);
      gtest::getAssertData().registerTestClass<T>(p_prefix, p_suffix);
   }
};

inline void launchAllTestFunction()
{
   getAssertData().launchAllTestFunction();
}

inline void launchAllTestFunction(conmanip::console_out_context p_ctxout)
{
   getAssertData().launchAllTestFunction(p_ctxout);
}


} // namespace gtest



#define STRINGIFY_PRIVATE(s) #s
#define STRINGIFY(s) STRINGIFY_PRIVATE(s)

#define GTEST_GLOBAL_DATA() namespace gtest { AssertData & getAssertData() { static AssertData assertData ; return assertData ; } }

#define TEST(a, b) void a##_##b() ; gtest::TestFunctionRegistrator g_TestFunctionRegistrator_##a##_##b(a##_##b, STRINGIFY(a), STRINGIFY(b)) ; void a##_##b()

#define TEST_F(a, b) class a##_##b : public a { public : void ExecuteTestBody() override ; } ; gtest::TestClassRegistrator<a##_##b> g_TestClassRegistrator_##a##_##b(STRINGIFY(a), STRINGIFY(b)) ; void a##_##b::ExecuteTestBody()


//#define LAUNCH(a, b) do { a##_##b() ; } while(false)

#define ASSERT_TRUE(a)  do { gtest::getAssertData().doAssertTrue(                      true,    STRINGIFY(a), (a), __FUNCTION__, __LINE__) ; } while(false)
#define ASSERT_FALSE(a) do { gtest::getAssertData().doAssertFalse(                     true,    STRINGIFY(a), (a), __FUNCTION__, __LINE__) ; } while(false)

#define EXPECT_TRUE(a)  do { gtest::getAssertData().doAssertTrue(                      false,   STRINGIFY(a), (a), __FUNCTION__, __LINE__) ; } while(false)
#define EXPECT_FALSE(a) do { gtest::getAssertData().doAssertFalse(                     false,   STRINGIFY(a), (a), __FUNCTION__, __LINE__) ; } while(false)

#define ASSERT_EQ(a, b) do { gtest::getAssertData().doAssertEqual(                     true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define ASSERT_NE(a, b) do { gtest::getAssertData().doAssertNotEqual(                  true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define EXPECT_EQ(a, b) do { gtest::getAssertData().doAssertEqual(                     false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define EXPECT_NE(a, b) do { gtest::getAssertData().doAssertNotEqual(                  false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define ASSERT_LT(a, b) do { gtest::getAssertData().doAssertLesser(                    true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define ASSERT_LE(a, b) do { gtest::getAssertData().doAssertLesserOrEqual(             true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define EXPECT_LT(a, b) do { gtest::getAssertData().doAssertLesser(                    false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define EXPECT_LE(a, b) do { gtest::getAssertData().doAssertLesserOrEqual(             false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define ASSERT_GT(a, b) do { gtest::getAssertData().doAssertGreater(                   true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define ASSERT_GE(a, b) do { gtest::getAssertData().doAssertGreaterOrEqual(            true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define EXPECT_GT(a, b) do { gtest::getAssertData().doAssertGreater(                   false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define EXPECT_GE(a, b) do { gtest::getAssertData().doAssertGreaterOrEqual(            false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define ASSERT_STREQ(a, b) do { gtest::getAssertData().doAssertEqualCString(           true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define ASSERT_STRNE(a, b) do { gtest::getAssertData().doAssertNotEqualCString(        true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define EXPECT_STREQ(a, b) do { gtest::getAssertData().doAssertEqualCString(           false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define EXPECT_STRNE(a, b) do { gtest::getAssertData().doAssertNotEqualCString(        false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define ASSERT_STRCASEEQ(a, b) do { gtest::getAssertData().doAssertEqualCStringCase(   true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define ASSERT_STRCASENE(a, b) do { gtest::getAssertData().doAssertNotEqualCStringCase(true,    STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define EXPECT_STRCASEEQ(a, b) do { gtest::getAssertData().doAssertEqualCStringCase(   false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)
#define EXPECT_STRCASENE(a, b) do { gtest::getAssertData().doAssertNotEqualCStringCase(false,   STRINGIFY(a), STRINGIFY(b), (a), (b), __FUNCTION__, __LINE__) ; } while(false)

#define SUCCEED()       do { gtest::getAssertData().doSucceed(                         true,    __FUNCTION__, __LINE__) ; } while(false)
#define FAIL()          do { gtest::getAssertData().doFail(                            true,    __FUNCTION__, __LINE__) ; } while(false)
#define ADD_FAILURE()   do { gtest::getAssertData().doFail(                            false,   __FUNCTION__, __LINE__) ; } while(false)

#endif // GTEST_H_AE554D8E_2DB7_4759_B0AD_C397807D7AB5




