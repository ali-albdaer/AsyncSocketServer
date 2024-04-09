"""Generate executable files for the server and client scripts using pyinstaller"""

import os
from shutil import rmtree


scripts = ("server.py", "client.py")

for script in scripts:
    try: 
        print(f'Generating executable for {script}...')
        os.system(f'python -m PyInstaller {script} --onefile --distpath ../apps')
        
        print("Removing build files...")
        os.remove(f'{script[:-3]}.spec')
        rmtree('build')
    except Exception as e:
        print(f'Error generating executable for {script}: {e}')

    else:
        print(f'Executable file generated: apps/{script[:-3]}.exe')
