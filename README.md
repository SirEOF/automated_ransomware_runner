# Automated ransomware runner

Runs a sequence of commands, which can be defined in the `run.json`, in a virtual box. Afterwards it compresses the files and folders in the output folder.
The operations in the `run.json` are setup to copy the ransomware executable on the internal drive, starting the executable, waiting for some time and then copying the encrypted files to the output folder.
The purpose of this runner is to generate a set of files encrypted by ransomware by automatically running ransomware executables in a save environment.

## Virtual box setup for optimally running ransomware

* Fully updated Windows 10
* Disabled Windows Defender
* Disabled UAC

## Setup

Use the constants in the script do define:
* Virtual box machine name
* Virtual box user name
* Virtual box password
* Zip Input folder (Virtual box output folder)
* Zip Output folder