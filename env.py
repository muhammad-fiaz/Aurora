import subprocess
import platform
import torch

from modules.logger import logly

# Function to check if a package is installed
def is_package_installed(package_name):
    process = subprocess.Popen(['pip', 'show', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode == 0

# Function to prepare the environment
def prepare_environment():
    # List of packages to install
    packages_to_install = []

    # Check if packages are not installed or have different versions
    packages = ['torch', 'torchvision', 'torchaudio']
    for package_name in packages:
        if not is_package_installed(package_name):
            packages_to_install.append(package_name)
        else:
            installed_version = subprocess.check_output(['pip', 'show', package_name]).decode('utf-8').split('\n')[1].split(': ')[1]
            # Uncomment the lines below if you want to check the exact version
            #if installed_version != package_versions[package_name]:
            #    packages_to_install.append(package_name)

    # Install packages based on platform and GPU availability
    if packages_to_install:
        if platform.system() == 'Linux':
            if torch.cuda.is_available():
                subprocess.run(['pip', 'install'] + packages_to_install + ['--index-url', 'https://download.pytorch.org/whl/cu118'])
            else:
                subprocess.run(['pip', 'install'] + packages_to_install + ['--index-url', 'https://download.pytorch.org/whl/cpu'])
        elif platform.system() == 'Windows':
            if torch.cuda.is_available():
                subprocess.run(['pip', 'install'] + packages_to_install + ['--index-url', 'https://download.pytorch.org/whl/cu121'])
            else:
                subprocess.run(['pip', 'install'] + packages_to_install)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['pip', 'install'] + packages_to_install)
        else:
            logly.warn("Unsupported operating system.")
        logly.info("Pytorch installed successfully.")
    else:
        logly.info("Pytorch packages are up-to-date.")
    # Install additional packages from requirements.txt
    logly.info("Checking for additional packages...")
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    logly.info("Additional packages installed successfully.")



