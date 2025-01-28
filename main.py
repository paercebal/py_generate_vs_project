import os
import sys
import paercebal.file_text
import paercebal.main_dialog
import paercebal.user_data

#print("Hello World")
#paercebal.my_file.my_function()

def test_define(p_text):
    print(p_text + ' : ' + paercebal.file_text.create_define(p_text))


def main() -> int:
    if True:
        ud = paercebal.user_data.user_data()
        ud.m_models_directory = os.path.join(os.getcwd(), "models")
        md = paercebal.main_dialog.main_dialog(ud)
        md.main_loop()
    else:
        print()
        test_define('AbcDef')
        test_define('AbcDEfg')
        test_define('Abc_Def')
        test_define('Abc_DEfg')
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit

