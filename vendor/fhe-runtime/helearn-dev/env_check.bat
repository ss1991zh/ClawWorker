@echo off
pip list | findstr pathlib
if %errorlevel% equ 0 (
    echo   *********************************************************************************
    echo **The 'conda-repo-cli' package, which is installed by default during the Anaconda  **
    echo **installation process, is an earlier version that depends on the third-party      **
    echo **'pathlib' package. In more recent versions of Python, pathlib has been integrated**
    echo **into the standard library and no longer requires separate installation.          **
    echo **When utilizing multiprocessing, an import error related to 'numpy' and the       **
    echo **'pathlib' package may arise due to a deprecated statement in the third-party     **
    echo **'pathlib' implementation, leading to incorrect program execution.                **
    echo **The installation script will remove any locally installed pathlib packages.      **
    echo **It is recommended that you execute:                                              **
    echo **                                                                                 **
    echo **'conda install conda-repo-cli'                                                   **
    echo **                                                                                 **
    echo **to update your 'conda-repo-cli' package; this new version will eliminate         **
    echo **reliance on the third-party 'pathlib'.                                           **
    echo   *********************************************************************************
    pip uninstall -y pathlib
)
@REM pip install -e helearn

echo on