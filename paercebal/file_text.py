import os
from pathlib import Path
import re
import shutil
import uuid


def create_define(p_name):
    define_name = ''
    is_previous_char_none = True
    is_previous_char_underscore = False
    is_previous_char_upper = False

    for i in range(len(p_name)):
        c = p_name[i]

        if c == '_':
            define_name += '_x_'
            is_previous_char_upper = False
            is_previous_char_underscore = True
        elif c.upper() == c:
            if is_previous_char_none:
                pass
            elif not is_previous_char_upper:
                if not is_previous_char_underscore:
                    define_name += '_'
            define_name += c
            is_previous_char_upper = True
            is_previous_char_underscore = False
        else:
            define_name += c.upper()
            is_previous_char_upper = False
            is_previous_char_underscore = False

        is_previous_char_none = False

    return define_name

def create_main_header(p_user_data):
    src = p_user_data.get_main_module_file_model_name(True)
    dst_header_include_guard = p_user_data.get_main_module_file_header_guard()
    dst = p_user_data.get_main_module_file_name(True)
    macro_prefix = p_user_data.get_main_module_macro_prefix()
    module_cpp_namespace = p_user_data.get_module_cpp_namespace()

    shutil.copy(src, dst)

    with open(dst, 'r') as file:
        data = file.read()

    data = re.sub('RBRBRBR_MAIN_FILE_HEADER_GUARD_RBRBRBR', dst_header_include_guard, data)
    data = re.sub('RBRBRBR_MODULE_MACRO_PREFIX_RBRBRBR', macro_prefix, data)
    data = re.sub('RBRBRBR_MODULE_CPP_NAMESPACE_RBRBRBR', module_cpp_namespace, data)
    data = data.replace('RBRBRBR_MAIN_FILE_PUBLIC_INCLUDE_DIRECTORY_RBRBRBR', '..\\' + p_user_data.get_relative_public_directory_for_includes())
    data = data.replace('RBRBRBR_MAIN_FILE_PUBLIC_COMENT_LIB_RBRBRBR', p_user_data.get_relative_module_pure_name())

    with open(dst, "w") as file:
        file.write(data)

def create_main_source(p_user_data):
    src = p_user_data.get_main_module_file_model_name(False)
    dst_header_include = p_user_data.get_main_module_file_include()
    dst = p_user_data.get_main_module_file_name(False)
    macro_prefix = p_user_data.get_main_module_macro_prefix()
    module_cpp_namespace = p_user_data.get_module_cpp_namespace()

    shutil.copy(src, dst)

    with open(dst, 'r') as file:
        data = file.read()

    data = data.replace('RBRBRBR_MODULE_MACRO_PREFIX_RBRBRBR', macro_prefix)
    data = data.replace('RBRBRBR_MODULE_CPP_NAMESPACE_RBRBRBR', module_cpp_namespace)

    if p_user_data.is_module_a("ConsoleEXE"):
        data = data.replace('RBRBRBR_MAIN_FILE_HEADER_INCLUDE_RBRBRBR', dst_header_include)
        data = data.replace('RBRBRBR_MAIN_FILE_SFML_INCLUDE_RBRBRBR', '')
        data = data.replace('RBRBRBR_MAIN_FILE_GTEST_INCLUDE_RBRBRBR', '')
        data = data.replace('RBRBRBR_WINMAIN_REDIRECTOR_TO_MAIN_RBRBRBR', '')
        data = data.replace('RBRBRBR_MAIN_FUNCTION_BODY_RBRBRBR', p_user_data.get_console_main_content())
    elif p_user_data.is_module_a("SFMLEXE"):
        data = data.replace('RBRBRBR_MAIN_FILE_HEADER_INCLUDE_RBRBRBR', dst_header_include)
        data = data.replace('RBRBRBR_MAIN_FILE_SFML_INCLUDE_RBRBRBR', '#include <SFML/Graphics.hpp>')
        data = data.replace('RBRBRBR_MAIN_FILE_GTEST_INCLUDE_RBRBRBR', '')
        data = data.replace('RBRBRBR_WINMAIN_REDIRECTOR_TO_MAIN_RBRBRBR', p_user_data.get_winmain_redirector_to_main())
        data = data.replace('RBRBRBR_MAIN_FUNCTION_BODY_RBRBRBR', p_user_data.get_sfml3_main_content())
    elif p_user_data.is_module_a("GTestEXE"):
        data = data.replace('RBRBRBR_MAIN_FILE_HEADER_INCLUDE_RBRBRBR', dst_header_include)
        data = data.replace('RBRBRBR_MAIN_FILE_SFML_INCLUDE_RBRBRBR', '')
        data = data.replace('RBRBRBR_MAIN_FILE_GTEST_INCLUDE_RBRBRBR', '#include <gtest/gtest.h>')
        data = data.replace('RBRBRBR_WINMAIN_REDIRECTOR_TO_MAIN_RBRBRBR', '')
        data = data.replace('RBRBRBR_MAIN_FUNCTION_BODY_RBRBRBR', p_user_data.get_gtest_main_content())
    elif p_user_data.is_module_a("DLL"):
        data = data.replace('RBRBRBR_MAIN_FILE_HEADER_INCLUDE_RBRBRBR', dst_header_include)

    with open(dst, "w") as file:
        file.write(data)


def create_update_file_sln_as_needed(p_user_data):
    pds = p_user_data.get_all_project_data()
    src = p_user_data.get_sln_model_name()

    for k, v in pds.items():
        dst = p_user_data.get_base_project_file_solution_name(k)
        my_file = Path(dst)


        # create dst file if it does not already exist
        if not my_file.is_file():
            shutil.copy(src, dst)

            with open(dst, 'r') as file:
                data = file.read()

            data = re.sub('RBRBR_SOLUTION_VISUAL_STUDIO_TITLE_RBRBR', v.m_sln_title, data)
            data = re.sub('RBRBR_SOLUTION_VISUAL_STUDIO_VERSION_RBRBR', v.m_sln_version, data)
            data = re.sub('RBRBR_SOLUTION_VISUAL_STUDIO_GLOBAL_SECTION_POST_SOLUTION_RBRBR', v.m_sln_global_section_post_solution, data)

            with open(dst, "w") as file:
                file.write(data)


        # here, we know dst file already exists, and only needs update
        project_line = p_user_data.get_sln_project_line()

        project_configuration_line_marker_re = r'GlobalSection\(ProjectConfigurationPlatforms\) = postSolution'
        project_configuration_line_marker = r'GlobalSection(ProjectConfigurationPlatforms) = postSolution'
        project_configuration_line = ''
        project_configuration_line += '\n\t\t' + str(p_user_data.m_module_guid) + '.ReleaseDev|x64.ActiveCfg = ReleaseDev|x64'
        project_configuration_line += '\n\t\t' + str(p_user_data.m_module_guid) + '.ReleaseDev|x64.Build.0 = ReleaseDev|x64'
        project_configuration_line += '\n\t\t' + str(p_user_data.m_module_guid) + '.Debug|x64.ActiveCfg = Debug|x64'
        project_configuration_line += '\n\t\t' + str(p_user_data.m_module_guid) + '.Debug|x64.Build.0 = Debug|x64'
        project_configuration_line += '\n\t\t' + str(p_user_data.m_module_guid) + '.Release|x64.ActiveCfg = Release|x64'
        project_configuration_line += '\n\t\t' + str(p_user_data.m_module_guid) + '.Release|x64.Build.0 = Release|x64'

        with open(dst, 'r') as file:
            data = file.read()

        m = re.search(r'Project\(\"([0-9a-fA-F\-]+)\"\)', data)
        if m:
            found = m.group(1)
            p_user_data.update_solution_guid(uuid.UUID(found))

        data = re.sub(r'^Global$', project_line + '\nGlobal', data, flags=re.MULTILINE)
        data = re.sub(project_configuration_line_marker_re, project_configuration_line_marker + project_configuration_line, data, flags=re.MULTILINE)

        with open(dst, "w") as file:
            file.write(data)


def create_file_vcxproj(p_user_data):
    pds = p_user_data.get_all_project_data()
    src = p_user_data.get_vcproj_model_name()
    src_header = p_user_data.get_main_module_file_name_for_vcproj(True)
    src_file = p_user_data.get_main_module_file_name_for_vcproj(False)

    files_declared_in_vcxproj = ''
    files_declared_in_vcxproj += '  <ItemGroup>\n'
    files_declared_in_vcxproj += '    <ClCompile Include="..\\' + src_file + '" />\n'
    files_declared_in_vcxproj += '  </ItemGroup>\n'
    files_declared_in_vcxproj += '  <ItemGroup>\n'
    files_declared_in_vcxproj += '    <ClInclude Include="..\\' + src_header + '" />\n'
    files_declared_in_vcxproj += '  </ItemGroup>'

    for k, v in pds.items():
        dst = p_user_data.get_full_project_file_project_name(k, 'vcxproj')
        my_file = Path(dst)

        shutil.copy(src, dst)

        with open(dst, 'r') as file:
            data = file.read()

        data = re.sub('RBRBR_PROJECT_TOOLS_VERSION_RBRBR', v.m_vcproj_project_tools_version, data)
        data = data.replace('RBRBR_FILES_DECLARED_IN_VCXPROJ_RBRBR', files_declared_in_vcxproj)
        data = data.replace('RBRBR_PROJECT_GUID_RBRBR', str(p_user_data.m_module_guid))
        data = data.replace('RBRBR_ROOT_NAMESPACE_NAME_RBRBR', p_user_data.get_vcxproj_root_namespace())
        data = data.replace('RBRBR_WINDOWS_TARGET_PLATFORM_VERSION_RBRBR', v.m_vcproj_windows_target_platform_version)
        data = data.replace('RBRBR_PROJECT_PLATFORM_FOLDER_NAME_RBRBR', v.m_solution_directory)
        data = data.replace('RBRBR_SUBSYSTEM_PREPROCESSOR_DEFINITION_RBRBR', p_user_data.get_subsystem_preprocessor_definition())
        data = data.replace('RBRBR_LANGUAGE_STANDARD_RBRBR', v.m_language_standard)
        data = data.replace('RBRBR_SUBSYSTEM_VALUE_RBRBR', p_user_data.get_subsystem_value())
        data = data.replace('RBRBR_VCPKG_PAERCEBAL_RBRBR', p_user_data.get_vcpkg_paercebal())
        data = data.replace('RBRBR_PROJECT_PLATFORM_TOOLSET_RBRBR', v.m_vcproj_project_platform_toolset)
        data = data.replace('RBRBR_SDL_CHECK_RBRBR', v.m_sdl_check)
        data = data.replace('RBRBR_CONFORMANCE_MODE_RBRBR', v.m_conformance_mode)
        data = data.replace('RBRBR_CONFIGURATION_TYPE_VALUE_RBRBR', p_user_data.get_configuration_type_value())
        data = data.replace('RBRBR_ADDITIONAL_INCLUDE_DIRECTORIES_RBRBR', '..\\' + p_user_data.get_additional_include_directories())

        with open(dst, "w") as file:
            file.write(data)



def create_file_vcxproj_filters(p_user_data):
    pds = p_user_data.get_all_project_data()
    src = p_user_data.get_vcproj_filter_model_name()
    src_header = p_user_data.get_main_module_file_name_for_vcproj(True)
    src_file = p_user_data.get_main_module_file_name_for_vcproj(False)

    for k, v in pds.items():
        dst = p_user_data.get_full_project_file_project_name(k, 'vcxproj.filters')
        my_file = Path(dst)

        shutil.copy(src, dst)

        unique_identifier_private = str(uuid.uuid4())
        unique_identifier_public = str(uuid.uuid4())

        filter_name_public = p_user_data.get_project_file_project_name() + ' (public)'
        filter_name_private = p_user_data.get_project_file_project_name() + ' (private)'
        unique_identifier_public = str(uuid.uuid4())
        unique_identifier_private = str(uuid.uuid4())

        src_file_filter_name = filter_name_private

        if p_user_data.is_module_library():
            src_header_filter_name = filter_name_public
        else:
            src_header_filter_name = filter_name_private

        files_declared_in_vcxproj = ''
        files_declared_in_vcxproj += '  <ItemGroup>\n'
        files_declared_in_vcxproj += '    <Filter Include="' + filter_name_private + '">\n'
        files_declared_in_vcxproj += '      <UniqueIdentifier>' + unique_identifier_private + '</UniqueIdentifier>\n'
        files_declared_in_vcxproj += '    </Filter>\n'
        files_declared_in_vcxproj += '  </ItemGroup>\n'

        if p_user_data.is_module_library():
            files_declared_in_vcxproj += '  <ItemGroup>\n'
            files_declared_in_vcxproj += '    <Filter Include="' + filter_name_public + '">\n'
            files_declared_in_vcxproj += '      <UniqueIdentifier>' + unique_identifier_public + '</UniqueIdentifier>\n'
            files_declared_in_vcxproj += '    </Filter>\n'
            files_declared_in_vcxproj += '  </ItemGroup>\n'

        files_declared_in_vcxproj += '  <ItemGroup>\n'
        files_declared_in_vcxproj += '    <ClCompile Include="..\\' + src_file + '">\n'
        files_declared_in_vcxproj += '      <Filter>' + src_file_filter_name + '</Filter>\n'
        files_declared_in_vcxproj += '    </ClCompile>\n'
        files_declared_in_vcxproj += '  </ItemGroup>\n'
        files_declared_in_vcxproj += '  <ItemGroup>\n'
        files_declared_in_vcxproj += '    <ClInclude Include="..\\' + src_header + '">\n'
        files_declared_in_vcxproj += '      <Filter>' + src_header_filter_name + '</Filter>\n'
        files_declared_in_vcxproj += '    </ClInclude>\n'
        files_declared_in_vcxproj += '  </ItemGroup>'

        with open(dst, 'r') as file:
            data = file.read()

            data = data.replace('RBRBR_PROJECT_TOOLS_VERSION_RBRBR', v.m_vcproj_project_tools_version)
            data = data.replace('RBRBRBR_VCXPROJ_FILTERS_CONTENT_RBRBRBR', files_declared_in_vcxproj)

        with open(dst, "w") as file:
            file.write(data)

def create_gitignore_as_needed(p_user_data):
    src = os.path.join(p_user_data.get_models_directory(), "gitignore.txt")
    dst = os.path.join(p_user_data.get_solution_directory(), ".gitignore")
    my_file = Path(dst)
    # create dst file if it does not already exist
    if not my_file.is_file():
        shutil.copy(src, dst)
