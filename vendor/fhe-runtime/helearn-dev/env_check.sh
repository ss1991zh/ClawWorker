#!/bin/bash

if pip list | grep -q pathlib; then
    echo "*********************************************************************************"
    echo "**The 'conda-repo-cli' package, which is installed by default during the Anaconda**"
    echo "**installation process, is an earlier version that depends on the third-party  **"
    echo "**'pathlib' package. In more recent versions of Python, pathlib has been        **"
    echo "**integrated into the standard library and no longer requires separate         **"
    echo "**installation. When utilizing multiprocessing, an import error related to     **"
    echo "**'numpy' and the 'pathlib' package may arise due to a deprecated statement in **"
    echo "**the third-party 'pathlib' implementation, leading to incorrect program       **"
    echo "**execution.                                                                  **"
    echo "**The installation script will remove any locally installed pathlib packages.  **"
    echo "**It is recommended that you execute:                                          **"
    echo "**                                                                             **"
    echo "**'conda install conda-repo-cli'                                               **"
    echo "**                                                                             **"
    echo "**to update your 'conda-repo-cli' package; this new version will eliminate     **"
    echo "**reliance on the third-party 'pathlib'.                                       **"
    echo "*********************************************************************************"
    pip uninstall -y pathlib
fi

# pip install -e helearn