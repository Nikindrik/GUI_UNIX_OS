import subprocess
import os

def install_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    subprocess.check_call(['pip', 'install', '-r', requirements_path])

install_requirements()