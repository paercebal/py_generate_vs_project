import os
import tkinter as tk
import uuid
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import paercebal.configuration
import paercebal.file_system
import paercebal.file_text
import subprocess


# https://www.pythontutorial.net/tkinter/tkinter-combobox/


def get_textbox(p_textbox):
    return p_textbox.get("1.0",'end-1c')

def set_textbox(p_textbox, p_text):
    p_textbox.delete(1.0, "end-1c")
    p_textbox.insert("end-1c", p_text)


class main_dialog:
    def __init__(self, p_user_data):
        self.user_data = p_user_data
        self.root = tk.Tk()
        #self.root.geometry('300x220')
        #self.root.resizable(False, False)
        self.root.title('Generate Visual Studio Project')

        self.style = ttk.Style()
        self.style.configure("TFrame", background='#BBBBBB')
        self.style.configure("TLabel", background='#BBBBBB')
        self.style.configure("TCheckbutton", background='#BBBBBB')
        self.style.configure("TPanedWindow", background='#BBBBBB')
        self.style.configure(".", font=('Helvetica', 12))

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

        current_row = -1

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Module Type:").grid(column=0, row=current_row, sticky="E")
        self.pw_module_type = ttk.PanedWindow(self.frm, orient='horizontal')
        self.pw_module_type.grid(column=1, row=current_row, columnspan=2, sticky="W")
        self.rb_module_type_variable = tk.StringVar()
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='Console EXE', value='ConsoleEXE', style='Toolbutton', variable=self.rb_module_type_variable))
        self.pw_module_type.add(ttk.Separator(self.frm, orient='vertical'))
        #self.pw_module_type.add(ttk.Radiobutton(self.frm, text='WinAPI EXE', value='WinApiEXE', style='Toolbutton', variable=self.rb_module_type_variable))
        #self.pw_module_type.add(ttk.Separator(self.frm, orient='vertical'))
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='SFML EXE', value='SFMLEXE', style='Toolbutton', variable=self.rb_module_type_variable))
        self.pw_module_type.add(ttk.Separator(self.frm, orient='vertical'))
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='DLL', value='DLL', style='Toolbutton', variable=self.rb_module_type_variable))
        self.pw_module_type.add(ttk.Separator(self.frm, orient='vertical'))
        self.pw_module_type.add(ttk.Radiobutton(self.frm, text='GTest EXE', value='GTestEXE', style='Toolbutton', variable=self.rb_module_type_variable))

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Parent Directory:").grid(column=0, row=current_row, sticky="E")
        self.cb_parent_dir_variable = tk.StringVar()
        self.cb_parent_dir = ttk.Combobox(self.frm, width=40, textvariable=self.cb_parent_dir_variable)
        self.cb_parent_dir.grid(column=1, row=current_row, columnspan=2, sticky="W")
        self.cb_parent_dir['values'] = list(r'D:\_rbr\dev\cpp')

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Solution Behaviour:").grid(column=0, row=current_row, sticky="E")
        self.pw_solution_behaviour = ttk.PanedWindow(self.frm, orient='horizontal')
        self.pw_solution_behaviour.grid(column=1, row=current_row, columnspan=2, sticky="W")
        self.rb_solution_behaviour_variable = tk.BooleanVar()
        self.pw_solution_behaviour.add(ttk.Radiobutton(self.frm, text='Default', value=False, style='Toolbutton', variable=self.rb_solution_behaviour_variable))
        self.pw_solution_behaviour.add(ttk.Separator(self.frm, orient='vertical'))
        self.pw_solution_behaviour.add(ttk.Radiobutton(self.frm, text='Inject', value=True, style='Toolbutton', variable=self.rb_solution_behaviour_variable))

        def on_behaviour_change(*args):
            if self.rb_solution_behaviour_variable.get():
                self.txt_root_namespace_injected.configure(state=tk.NORMAL, bg='white')
                self.txt_app_main_namespace_injected.configure(state=tk.NORMAL, bg='white')
                self.txt_module_sub_namespace_injected.configure(state=tk.NORMAL, bg='white')
            else:
                self.txt_root_namespace_injected.configure(state=tk.DISABLED, bg='grey60')
                self.txt_app_main_namespace_injected.configure(state=tk.DISABLED, bg='grey60')
                self.txt_module_sub_namespace_injected.configure(state=tk.DISABLED, bg='grey60')

        self.rb_solution_behaviour_variable.trace_add('write', on_behaviour_change)

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text=" ").grid(column=0, row=current_row, sticky="E")
        ttk.Label(self.frm, text="Project:").grid(column=1, row=current_row)
        ttk.Label(self.frm, text="Injected into:").grid(column=2, row=current_row)

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Root Namespace:").grid(column=0, row=current_row, sticky="E")
        self.txt_root_namespace = tk.Text(self.frm, height=1, width=20)
        self.txt_root_namespace.grid(column=1, row=current_row, columnspan=1, sticky="W")
        self.txt_root_namespace_injected = tk.Text(self.frm, height=1, width=20)
        self.txt_root_namespace_injected.grid(column=2, row=current_row, columnspan=1, sticky="W")

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Application Name:").grid(column=0, row=current_row, sticky="E")
        self.txt_app_main_namespace = tk.Text(self.frm, height=1, width=20)
        self.txt_app_main_namespace.grid(column=1, row=current_row, columnspan=1, sticky="W")
        self.txt_app_main_namespace_injected = tk.Text(self.frm, height=1, width=20)
        self.txt_app_main_namespace_injected.grid(column=2, row=current_row, columnspan=1, sticky="W")

        # ========================================================================================
        current_row += 1
        ttk.Label(self.frm, text="Module Name:").grid(column=0, row=current_row, sticky="E")
        self.txt_module_sub_namespace = tk.Text(self.frm, height=1, width=20)
        self.txt_module_sub_namespace.grid(column=1, row=current_row, columnspan=1, sticky="W")
        self.txt_module_sub_namespace_injected = tk.Text(self.frm, height=1, width=20)
        self.txt_module_sub_namespace_injected.grid(column=2, row=current_row, columnspan=1, sticky="W")

        # ========================================================================================
        current_row += 1
        self.ck_vcpkg_paercebal_variable = tk.BooleanVar()
        self.ck_vcpkg_paercebal = ttk.Checkbutton(self.frm, text='Explicit VCPKG/PAERCEBAL', variable=self.ck_vcpkg_paercebal_variable)
        self.ck_vcpkg_paercebal.grid(column=0, row=current_row, columnspan=3, sticky="E")

        # ========================================================================================
        current_row += 1
        self.ck_open_explorer_variable = tk.BooleanVar()
        self.ck_open_explorer = ttk.Checkbutton(self.frm, text='Open Explorer on finish', variable=self.ck_open_explorer_variable)
        self.ck_open_explorer.grid(column=0, row=current_row, columnspan=3, sticky="E")

        # ========================================================================================
        current_row += 1
        self.ck_message_box_on_finish_variable = tk.BooleanVar()
        self.ck_message_box_on_finish = ttk.Checkbutton(self.frm, text='MessageBox on finish', variable=self.ck_message_box_on_finish_variable)
        self.ck_message_box_on_finish.grid(column=0, row=current_row, columnspan=3, sticky="E")

        # ========================================================================================
        current_row += 1
        self.ck_save_configuration = ttk.Button(self.frm, text='Save Config', command=lambda: self.save_configuration_from_dialog())
        self.ck_save_configuration.grid(column=0, row=current_row, columnspan=3, sticky="E")

        # ========================================================================================
        current_row += 1
        self.ck_create_module = ttk.Button(self.frm, text='Create Module', command=lambda: self.on_create_click())
        self.ck_create_module.grid(column=0, row=current_row, columnspan=3, sticky="E")

        # ========================================================================================
        # ========================================================================================
        self.rb_module_type_variable.set('ConsoleEXE')
        self.cb_parent_dir.set(r'D:\_rbr\dev\cpp')
        self.rb_solution_behaviour_variable.set(False)
        self.ck_vcpkg_paercebal_variable.set(True)
        self.ck_open_explorer_variable.set(True)
        self.ck_message_box_on_finish_variable.set(True)
        set_textbox(self.txt_root_namespace, "ROOT_NAMESPACE")
        set_textbox(self.txt_app_main_namespace, "my_app")
        set_textbox(self.txt_module_sub_namespace, "my_module")
        set_textbox(self.txt_root_namespace_injected, "ROOT_NAMESPACE_INJ")
        set_textbox(self.txt_app_main_namespace_injected, "my_app_inj")
        set_textbox(self.txt_module_sub_namespace_injected, "my_module_inj")

        # ========================================================================================
        # ========================================================================================
        self.load_configuration_into_dialog()


    # ========================================================================================
    # ========================================================================================

    def load_configuration_into_dialog(self):
        data = paercebal.configuration.load_configuration(os.path.join(os.getcwd(), r'py_generate_vs_project.json'))

        if 'parent_directories' in data:
            dirs = data['parent_directories']
            self.cb_parent_dir['values'] = dirs

        if 'root_namespace' in data:
            set_textbox(self.txt_root_namespace, str(data['root_namespace']))

        if 'application_name' in data:
            set_textbox(self.txt_app_main_namespace, str(data['application_name']))

        if 'module_name' in data:
            set_textbox(self.txt_module_sub_namespace, str(data['module_name']))

        if 'root_namespace_injected' in data:
            set_textbox(self.txt_root_namespace_injected, str(data['root_namespace_injected']))

        if 'application_name_injected' in data:
            set_textbox(self.txt_app_main_namespace_injected, str(data['application_name_injected']))

        if 'module_name_injected' in data:
            set_textbox(self.txt_module_sub_namespace_injected, str(data['module_name_injected']))

        if 'explicit_vcpkg_paercebal' in data:
            self.ck_vcpkg_paercebal_variable.set(data['explicit_vcpkg_paercebal'])

        if 'open_explorer_on_finish' in data:
            self.ck_open_explorer_variable.set(data['open_explorer_on_finish'])

        if 'message_box_on_finish' in data:
            self.ck_message_box_on_finish_variable.set(data['message_box_on_finish'])

        pass

    def save_configuration_from_dialog(self):
        data = paercebal.configuration.load_configuration(os.path.join(os.getcwd(), r'py_generate_vs_project.json'))

        if 'parent_directories' not in data:
            data['parent_directories'] = self.cb_parent_dir['values']
        else:
            data['parent_directories'].extend(self.cb_parent_dir['values'])

        data['parent_directories'].insert(0, self.cb_parent_dir_variable.get())
        data['parent_directories'] = list(dict.fromkeys(data['parent_directories']))
        data['parent_directories'][0:10]
        self.cb_parent_dir['values'] = data['parent_directories']
        paercebal.configuration.save_configuration(os.path.join(os.getcwd(), r'py_generate_vs_project.json'), data)
        pass


    # ========================================================================================
    # ========================================================================================

    def fill_and_check_user_data(self):
        self.user_data.m_module_type = self.rb_module_type_variable.get()
        self.user_data.m_parent_directory = self.cb_parent_dir_variable.get()
        self.user_data.m_root_namespace = get_textbox(self.txt_root_namespace)
        self.user_data.m_application_name = get_textbox(self.txt_app_main_namespace)
        self.user_data.m_module_name = get_textbox(self.txt_module_sub_namespace)
        self.user_data.m_injected = self.rb_solution_behaviour_variable.get()
        self.user_data.m_root_namespace_injected = get_textbox(self.txt_root_namespace_injected)
        self.user_data.m_application_name_injected = get_textbox(self.txt_app_main_namespace_injected)
        self.user_data.m_module_name_injected = get_textbox(self.txt_module_sub_namespace_injected)
        self.user_data.m_vcpkg_paercebal = self.ck_vcpkg_paercebal_variable.get()
        self.user_data.m_open_explorer = self.ck_open_explorer_variable.get()
        self.user_data.m_message_box_on_finish = self.ck_message_box_on_finish_variable.get()
        return True

    def on_create_click(self):
        if self.fill_and_check_user_data():
            self.user_data.m_module_guid = uuid.uuid4()
            self.create_directories()
            self.generate_files()
            self.open_explorer()
            self.open_message_box()

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

    def open_message_box(self):
        if self.user_data.m_message_box_on_finish:
            messagebox.showinfo(title='Success', message='Visual Studio Project Generated', type=messagebox.OK)

    def main_loop(self):
        self.root.mainloop()

