import os
from shutil import rmtree


REMOVE_BUILD = True
REMOVE_SPEC = True


scripts = ("server.py", "client.py")


for script in scripts:
    try: 
        print(f'Generating executable for {script}...')
        os.system(f'python -m PyInstaller {script} --onefile --distpath /apps')

        if REMOVE_SPEC:
            print(f'Removing {script[:-3]}.spec file...')
            os.remove(f'{script[:-3]}.spec')

        if REMOVE_BUILD:
            print('Removing build directory...')
            rmtree('build')

    except Exception as e:
        print(f'Error generating executable for {script}: {e}')

    else:
        print(f'Executable file generated: apps/{script[:-3]}.exe')
