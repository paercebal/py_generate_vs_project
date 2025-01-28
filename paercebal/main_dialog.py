import tkinter as tk
import uuid
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import paercebal.file_system
import paercebal.file_text
import subprocess


# https://www.pythontutorial.net/tkinter/tkinter-combobox/

class main_dialog():
    def __init__(self, p_user_data):
        self.user_data = p_user_data
        self.root = tk.Tk()
        #self.root.geometry('300x220')
        #self.root.resizable(False, False)
        self.root.title('Generate Visual Studio Module')

        self.style = ttk.Style()
        self.style.configure("TFrame", background='#BBBBBB')
        self.style.configure("TLabel", background='#BBBBBB')
        self.style.configure("TCheckbutton", background='#BBBBBB')
        self.style.configure(".", font=('Helvetica', 12))

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

        current_row = -1

        # ========================================================================================
        #current_row += 1
        #ttk.Label(frm, text="Hello World!").grid(column=0, row=current_row)
        #ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=current_row)

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Module Type:").grid(column=0, row=current_row, sticky="E")
        #self.cb_project_type_current = tk.StringVar()
        #self.cb_project_type = ttk.Combobox(self.frm, textvariable=cb_project_type_current)
        #self.cb_project_type.grid(column=1, row=current_row)
        #self.cb_project_type["values"] = ("Console", "DLL")
        #self.cb_project_type.set("Console")
        #self.cb_project_type["state"] = "readonly"
        self.pw_module_type = ttk.PanedWindow(self.frm, orient='horizontal')
        self.pw_module_type.grid(column=1, row=current_row, sticky="W")
        self.rb_module_type_variable = tk.StringVar()
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='Console EXE', value='ConsoleEXE', style='Toolbutton', variable=self.rb_module_type_variable))
        #self.pw_module_type.add(ttk.Radiobutton(self.frm, text='WinAPI EXE', value='WinApiEXE', style='Toolbutton', variable=self.rb_module_type_variable))
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='SFML EXE', value='SFMLEXE', style='Toolbutton', variable=self.rb_module_type_variable))
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='DLL', value='DLL', style='Toolbutton', variable=self.rb_module_type_variable))
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='GTest EXE', value='GTestEXE', style='Toolbutton', variable=self.rb_module_type_variable))
        self.rb_module_type_variable.set('ConsoleEXE')

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Parent Directory:").grid(column=0, row=current_row, sticky="E")
        self.cb_parent_dir_variable = tk.StringVar()
        self.cb_parent_dir = ttk.Combobox(self.frm, width=40, textvariable=self.cb_parent_dir_variable)
        self.cb_parent_dir.grid(column=1, row=current_row, sticky="W")
        self.cb_parent_dir['values'] = (r'D:\_rbr\dev\cpp')
        self.cb_parent_dir.set(r'D:\_rbr\dev\cpp')

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Root Namespace:").grid(column=0, row=current_row, sticky="E")
        self.txt_root_namespace = tk.Text(self.frm, height=1, width=40)
        self.txt_root_namespace.grid(column=1, row=current_row, sticky="W")
        self.txt_root_namespace.insert("1.0", "paercebal")

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Application Name:").grid(column=0, row=current_row, sticky="E")
        self.txt_app_main_namespace = tk.Text(self.frm, height=1, width=40)
        self.txt_app_main_namespace.grid(column=1, row=current_row, sticky="W")
        self.txt_app_main_namespace.insert("1.0", "my_app")

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Module Name:").grid(column=0, row=current_row, sticky="E")
        self.txt_module_sub_namespace = tk.Text(self.frm, height=1, width=40)
        self.txt_module_sub_namespace.grid(column=1, row=current_row, sticky="W")
        self.txt_module_sub_namespace.insert("1.0", "my_module")

        # ========================================================================================
        current_row += 1
        self.ck_vcpkg_paercebal_variable = tk.BooleanVar()
        self.ck_vcpkg_paercebal = ttk.Checkbutton(self.frm, text='Explicit VCPKG/PAERCEBAL', variable=self.ck_vcpkg_paercebal_variable)
        self.ck_vcpkg_paercebal.grid(column=0, row=current_row, columnspan=2, sticky="E")
        self.ck_vcpkg_paercebal_variable.set(True)

        # ========================================================================================
        current_row += 1
        self.ck_open_explorer_variable = tk.BooleanVar()
        self.ck_open_explorer = ttk.Checkbutton(self.frm, text='Open Explorer', variable=self.ck_open_explorer_variable)
        self.ck_open_explorer.grid(column=0, row=current_row, columnspan=2, sticky="E")
        self.ck_open_explorer_variable.set(True)

        # ========================================================================================
        current_row += 1
        self.ck_open_explorer = ttk.Button(self.frm, text='Create Module', command=lambda: self.on_create_click())
        self.ck_open_explorer.grid(column=0, row=current_row, columnspan=2, sticky="E")
        self.ck_open_explorer_variable.set(True)


        # ========================================================================================
        # ========================================================================================

    def fill_and_check_user_data(self):
        self.user_data.m_module_type = self.rb_module_type_variable.get()
        self.user_data.m_parent_directory = self.cb_parent_dir_variable.get()
        self.user_data.m_root_namespace = self.txt_root_namespace.get("1.0",'end-1c')
        self.user_data.m_application_name = self.txt_app_main_namespace.get("1.0",'end-1c')
        self.user_data.m_module_name = self.txt_module_sub_namespace.get("1.0",'end-1c')
        self.user_data.m_vcpkg_paercebal = self.ck_vcpkg_paercebal_variable.get()
        self.user_data.m_open_explorer = self.ck_open_explorer_variable.get()
        return True

    def on_create_click(self):
        if self.fill_and_check_user_data():
            self.user_data.m_module_guid = uuid.uuid4()
            self.create_directories();
            self.generate_files();
            self.open_explorer();
            messagebox.showinfo(title='Success', message='Visual Studio Module Generated', type=messagebox.OK)

    def create_directories(self):
        paercebal.file_system.create_directory_structure(self.user_data)

    def generate_files(self):
        paercebal.file_text.create_main_header(self.user_data)
        paercebal.file_text.create_main_source(self.user_data)
        paercebal.file_text.create_update_file_sln_as_needed(self.user_data)
        paercebal.file_text.create_file_vcxproj(self.user_data)
        paercebal.file_text.create_file_vcxproj_filters(self.user_data)

    def open_explorer(self):
        if self.user_data.m_open_explorer:
            subprocess.Popen('explorer "' + self.user_data.get_solution_directory() + '"')

    def main_loop(self):
        self.root.mainloop()

