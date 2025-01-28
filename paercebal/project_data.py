import os
import re
import uuid


class project_data:

    def __init__(self):
        self.m_solution_directory = None
        self.m_is_visual_studio = False
        self.m_is_gcc = False
        self.m_sln_title = ""
        self.m_sln_version = ""
        self.m_sln_global_section_post_solution = ""
        self.m_vcproj_project_tools_version = ""
        self.m_vcproj_windows_target_platform_version = ""
        self.m_vcproj_project_platform_toolset = ""
        self.m_language_standard = ""
        self.m_sdl_check = ""
        self.m_conformance_mode = ""



def get_all_project_data():
    d = dict()
    pd = project_data_vs_2017()
    d[pd.m_solution_directory] = pd
    pd = project_data_vs_2019()
    d[pd.m_solution_directory] = pd
    pd = project_data_vs_2022()
    d[pd.m_solution_directory] = pd
    return d


def project_data_vs_2017():

    pd = project_data()
    pd.m_solution_directory = "_vs2017"
    pd.m_is_visual_studio = True
    pd.m_sln_title = "Microsoft Visual Studio Solution File, Format Version 12.00"
    pd.m_sln_version = "Visual Studio 15\nVisualStudioVersion = 15.0.26228.4\nMinimumVisualStudioVersion = 10.0.40219.1"
    pd.m_sln_global_section_post_solution = ""

    pd.m_vcproj_project_tools_version = "15.0"
    pd.m_vcproj_windows_target_platform_version = ""
    pd.m_vcproj_project_platform_toolset = "<PlatformToolset>v141</PlatformToolset>"
    pd.m_language_standard = "<LanguageStandard>stdcpplatest</LanguageStandard>"
    pd.m_sdl_check = ""
    pd.m_conformance_mode = ""

    return pd


def project_data_vs_2019():

    pd = project_data()
    pd.m_solution_directory = "_vs2019"
    pd.m_is_visual_studio = True
    pd.m_sln_title = "Microsoft Visual Studio Solution File, Format Version 12.00"
    pd.m_sln_version = "Visual Studio 16\nVisualStudioVersion = 16.0.29009.5\nMinimumVisualStudioVersion = 10.0.40219.1"
    pd.m_sln_global_section_post_solution = "<WindowsTargetPlatformVersion>10.0</WindowsTargetPlatformVersion>"

    pd.m_vcproj_project_tools_version = "15.0"
    pd.m_vcproj_windows_target_platform_version = ""
    pd.m_vcproj_project_platform_toolset = "<PlatformToolset>v142</PlatformToolset>"
    pd.m_language_standard = "<LanguageStandard>stdcpplatest</LanguageStandard>"
    pd.m_sdl_check = ""
    pd.m_conformance_mode = ""

    return pd


def project_data_vs_2022():

    pd = project_data()
    pd.m_solution_directory = "_vs2022"
    pd.m_is_visual_studio = True
    pd.m_sln_title = "Microsoft Visual Studio Solution File, Format Version 12.00"
    pd.m_sln_version = "Visual Studio Version 17\nVisualStudioVersion = 17.1.32407.343\nMinimumVisualStudioVersion = 10.0.40219.1"
    pd.m_sln_global_section_post_solution = ""

    pd.m_vcproj_project_tools_version = "15.0"
    pd.m_vcproj_windows_target_platform_version = "<VCProjectVersion>16.0</VCProjectVersion>\n<WindowsTargetPlatformVersion>10.0</WindowsTargetPlatformVersion>"
    pd.m_vcproj_project_platform_toolset = "<PlatformToolset>v143</PlatformToolset>"
    pd.m_language_standard = "<LanguageStandard>stdcpplatest</LanguageStandard>"
    pd.m_sdl_check = "<SDLCheck>true</SDLCheck>"
    pd.m_conformance_mode = "<ConformanceMode>true</ConformanceMode>"

    return pd

