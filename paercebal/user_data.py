import os
import re
import uuid
import paercebal.project_data


class user_data:

    def __init__(self):
        self.m_models_directory = ""
        self.m_root_namespace = ""
        self.m_application_name = ""
        self.m_module_name = ""
        self.m_parent_directory = ""
        self.m_module_type = ""
        self.m_solution_guid = uuid.uuid4()
        self.m_module_guid = uuid.uuid4()
        self.m_vcpkg_paercebal = True
        self.m_open_explorer = True
        self.m_message_box_on_finish = True
        self.m_project_datas = paercebal.project_data.get_all_project_data()

    def update_solution_guid(self, p_uuid):
        self.m_solution_guid = p_uuid

    def get_parent_directory(self):
        return self.m_parent_directory

    def get_solution_directory(self):
        if len(self.m_root_namespace) > 0:
            return os.path.join(self.m_parent_directory, self.m_root_namespace + '.' + self.m_application_name)
        else:
            return os.path.join(self.m_parent_directory, self.m_application_name)

    def get_relative_module_pure_name(self):
        if len(self.m_root_namespace) > 0:
            return self.m_root_namespace + '.' + self.m_application_name + '.' + self.m_module_name
        else:
            return self.m_application_name + '.' + self.m_module_name

    def get_relative_module_directory(self):
        return self.get_relative_module_pure_name()

    def get_module_directory(self):
        return os.path.join(self.get_solution_directory(), self.get_relative_module_directory())

    def get_all_project_data(self):
        return self.m_project_datas

    def get_project_files_directory(self, p_key):
        return os.path.join(self.get_solution_directory(), p_key)

    def get_vs2017_directory(self):
        return self.get_project_files_directory('_vs2017')

    def get_vs2019_directory(self):
        return self.get_project_files_directory('_vs2019')

    def get_vs2022_directory(self):
        return self.get_project_files_directory('_vs2022')

    def get_gcc_directory(self):
        return self.get_project_files_directory('_gcc_cpp')

    def get_gcc11_directory(self):
        return self.get_project_files_directory('_gcc_cpp11')

    def get_gcc14_directory(self):
        return self.get_project_files_directory('_gcc_cpp14')

    def get_base_cpp_include(self):
        if len(self.m_root_namespace) > 0:
            return self.m_root_namespace + '/' + self.m_application_name + '/' + self.m_module_name
        else:
            return self.m_application_name + '/' + self.m_module_name

    def get_base_project_file_solution_name(self, p_KEY):
        if len(self.m_root_namespace) > 0:
            return os.path.join(self.get_solution_directory(), p_KEY, self.m_root_namespace + '.' + self.m_application_name + '.sln')
        else:
            return os.path.join(self.get_solution_directory(), p_KEY, self.m_application_name + '.sln')

    def get_project_file_project_name(self):
        if len(self.m_root_namespace) > 0:
            return self.m_root_namespace + '.' + self.m_application_name + '.' + self.m_module_name
        else:
            return self.m_application_name + '.' + self.m_module_name

    def get_vcxproj_root_namespace(self):
        if len(self.m_root_namespace) > 0:
            return self.m_root_namespace + '_' + self.m_application_name + '_' + self.m_module_name
        else:
            return self.m_application_name + '_' + self.m_module_name

    def get_project_file_project_name_with_suffix(self, p_file_suffix):
        if len(self.m_root_namespace) > 0:
            return self.m_root_namespace + '.' + self.m_application_name + '.' + self.m_module_name + '.' + p_file_suffix
        else:
            return self.m_application_name + '.' + self.m_module_name + '.' + p_file_suffix

    def get_full_project_file_project_name(self, p_KEY, p_file_suffix):
        if len(self.m_root_namespace) > 0:
            return os.path.join(self.get_solution_directory(), p_KEY, self.m_root_namespace + '.' + self.m_application_name + '.' + self.m_module_name + '.' + p_file_suffix)
        else:
            return os.path.join(self.get_solution_directory(), p_KEY, self.m_application_name + '.' + self.m_module_name + '.' + p_file_suffix)

    def get_base_SOURCE_directory(self, p_SOURCE):
        if len(self.m_root_namespace) > 0:
            return os.path.join(self.get_module_directory(), p_SOURCE, self.m_root_namespace, self.m_application_name, self.m_module_name)
        else:
            return os.path.join(self.get_module_directory(), p_SOURCE, self.m_application_name, self.m_module_name)

    def get_base_private_directory(self):
        return self.get_base_SOURCE_directory("private")

    def get_base_public_directory(self):
        return self.get_base_SOURCE_directory("public")

    def get_relative_SOURCE_directory(self, p_SOURCE):
        if len(self.m_root_namespace) > 0:
            return os.path.join(self.get_relative_module_directory(), p_SOURCE, self.m_root_namespace, self.m_application_name, self.m_module_name)
        else:
            return os.path.join(self.get_relative_module_directory(), p_SOURCE, self.m_application_name, self.m_module_name)

    def get_relative_private_directory(self):
        return self.get_relative_SOURCE_directory("private")

    def get_relative_public_directory(self):
        return self.get_relative_SOURCE_directory("public")

    def get_relative_SOURCE_directory_for_includes(self, p_SOURCE):
        if len(self.m_root_namespace) > 0:
            return os.path.join(self.get_relative_module_directory(), p_SOURCE, self.m_root_namespace, self.m_application_name, self.m_module_name)
        else:
            return os.path.join(self.get_relative_module_directory(), p_SOURCE, self.m_application_name, self.m_module_name)

    def get_relative_private_directory_for_includes(self):
        return os.path.join(self.get_relative_module_directory(), 'private')

    def get_relative_public_directory_for_includes(self):
        return os.path.join(self.get_relative_module_directory(), 'public')

    def is_module_a(self, p_module_type):
        return self.m_module_type == p_module_type

    def is_module_library(self):
        return self.m_module_type == 'DLL'

    def get_subsystem_preprocessor_definition(self):
        if self.m_module_type == 'ConsoleEXE':
            return '_CONSOLE'
        if self.m_module_type == 'GTestEXE':
            return '_CONSOLE'
        if self.m_module_type == 'WinApiEXE':
            return '_WINDOWS'
        if self.m_module_type == 'SFMLEXE':
            return '_WINDOWS'
        if self.m_module_type == 'DLL':
            macro_prefix = self.get_main_module_macro_prefix()

            return '_WINDOWS;_USRDLL;' + macro_prefix + '_x_EXPORTS'
        return '_CONSOLE'

    def get_subsystem_value(self):
        if self.m_module_type == 'ConsoleEXE':
            return 'Console'
        if self.m_module_type == 'GTestEXE':
            return 'Console'
        if self.m_module_type == 'WinApiEXE':
            return 'Windows'
        if self.m_module_type == 'SFMLEXE':
            return 'Windows'
        if self.m_module_type == 'DLL':
            return 'Windows'
        return 'Console'

    def get_configuration_type_value(self):
        if self.m_module_type == 'ConsoleEXE':
            return 'Application'
        if self.m_module_type == 'GTestEXE':
            return 'Application'
        if self.m_module_type == 'WinApiEXE':
            return 'Application'
        if self.m_module_type == 'SFMLEXE':
            return 'Application'
        if self.m_module_type == 'DLL':
            return 'DynamicLibrary'
        return 'Application'

    def has_public_headers(self):
        return self.is_module_library()

    def get_main_module_file_model_name(self, p_is_header):
        if self.is_module_library():
            filename = 'module'
        else:
            filename = 'main'

        if p_is_header:
            extension = 'hpp'
        else:
            extension = 'cpp'

        return os.path.join(self.m_models_directory, filename + '.' + extension)

    def get_main_module_file_name(self, p_is_header):
        if self.is_module_library():
            filename = 'module'
        else:
            filename = 'main'

        if p_is_header:
            extension = 'hpp'
        else:
            extension = 'cpp'

        if p_is_header and self.has_public_headers():
            return os.path.join(self.get_base_public_directory(), filename + '.' + extension)
        else:
            return os.path.join(self.get_base_private_directory(), filename + '.' + extension)

    def get_main_module_file_name_for_vcproj(self, p_is_header):
        if self.is_module_library():
            filename = 'module'
        else:
            filename = 'main'

        if p_is_header:
            extension = 'hpp'
        else:
            extension = 'cpp'

        if p_is_header and self.has_public_headers():
            return os.path.join(self.get_relative_public_directory(), filename + '.' + extension)
        else:
            return os.path.join(self.get_relative_private_directory(), filename + '.' + extension)


    def get_main_module_file_include_content(self):
        if self.is_module_library():
            filename = 'module'
        else:
            filename = 'main'

        extension = 'hpp'

        return self.get_base_cpp_include() + '/' + filename + '.' + extension

    def get_main_module_file_include(self):
        return '#include <' + self.get_main_module_file_include_content() + '>'

    def get_main_module_file_header_guard(self):
        hg = self.get_main_module_file_include_content().upper()
        hg = re.sub(r'\/', r'_x_', hg)
        hg = re.sub(r'\.', r'_x_', hg)
        return hg

    def get_main_module_macro_prefix(self):
        mp = self.get_base_cpp_include().upper()
        mp = re.sub(r'\/', r'_x_', mp)
        return mp

    def get_module_cpp_namespace(self):
        if len(self.m_root_namespace) > 0:
            return self.m_root_namespace + '::' + self.m_application_name + '::' + self.m_module_name
        else:
            return self.m_application_name + '::' + self.m_module_name

    def get_sln_model_name(self):
        return os.path.join(self.m_models_directory, 'vs2010.sln')

    def get_vcproj_model_name(self):
        return os.path.join(self.m_models_directory, 'vs2010.vcxproj')

    def get_vcproj_filter_model_name(self):
        return os.path.join(self.m_models_directory, 'vs2010.vcxproj.filters')

    def get_sln_project_line(self):
        s = 'Project("' + str(self.m_solution_guid) + '")'
        s += ' = "' + self.get_project_file_project_name() + '"'
        s += ', "' + self.get_project_file_project_name_with_suffix('vcxproj') + '"'
        s += ', "' + str(self.m_module_guid) + '"'
        return s

    def get_vcpkg_paercebal(self):
        if self.m_vcpkg_paercebal:
            return r'<Import Project="$(PAERCEBAL_VCPKG_DIR)\scripts\buildsystems\msbuild\vcpkg.targets" />'
        else:
            return ''

    def get_additional_include_directories(self):
        s = ''
        if self.has_public_headers():
            s += self.get_relative_public_directory_for_includes() + ';'
        s += self.get_relative_private_directory_for_includes()
        return s

    def get_winmain_redirector_to_main(self):
        s = ''
        s += '#if defined(_WIN32)\n\n'
        s += '#include <windows.h>\n\n'
        s += 'extern int main(int argc, char* argv[]);\n\n'
        s += 'int WINAPI WinMain(HINSTANCE, HINSTANCE, LPSTR, INT)\n'
        s += '{\n'
        s += '   return main(__argc, __argv);\n'
        s += '}\n\n'
        s += '#endif // _WIN32\n'
        return s

    def get_gtest_main_content(self):
        s = ''
        s += '   ::testing::InitGoogleTest(&p_argc, p_argv);\n'
        s += '   return RUN_ALL_TESTS();'
        return s

    def get_console_main_content(self):
        s = ''
        s += '   std::cout << "Hello World";'
        return s

    def get_sfml2_main_content(self):
        s = ''
        s += '   sf::Window window;\n'
        s += '   window.create(sf::VideoMode(800, 600), "My SFML2 window");\n'
        s += '   window.setVerticalSyncEnabled(true); // call it once, after creating the window\n'
        s += '   window.setFramerateLimit(60); // call it once, after creating the window\n'
        s += '\n'
        s += '   while (window.isOpen())\n'
        s += '   {\n'
        s += '      // check all the window\'s events that were triggered since the last iteration of the loop\n'
        s += '      sf::Event event;\n'
        s += '\n'
        s += '      while (window.pollEvent(event))\n'
        s += '      {\n'
        s += '         // "close requested" event: we close the window\n'
        s += '         if (event.type == sf::Event::Closed)\n'
        s += '         {\n'
        s += '            window.close();\n'
        s += '         }\n'
        s += '      }\n'
        s += '   }\n'
        s += '\n'
        s += '   return 0;'
        return s


