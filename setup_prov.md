# Language-Level Provenance Setup

## Background Setup:
Disclaimer: Everything I will detail in this setup is from a clean machine. 

Tried on the following systems:
OS: Ubuntu 18.04, Fedora 29/31, and MacOS Mojave (10.14.8) 

## Installing:
noWorkflow: version 1.11.2
RDataTracker: requires R version 3.6.1

## Setup Instructions:
1. install python and python3 (```sudo apt install <package>```)
2. install pip (not pip3) (```sudo apt install python-pip```)
3. install pyenv
4. in whichever directory you want to work in, set the local python version to 3.5.6.
   a) ```pyenv install 3.5.6```
   b) ```pyenv local 3.5.6```
-----------------------------------------------------------------------------------------


### noWorkflow Installation:
Install noWorkflow via pip (```pip install noworkflow[all]```)
   - pip install noworkflow[all] to install noWorkflow, PyPosAST, SQLAlchemy, 
      python-future, flask, IPython, Jupyter and PySWIP.
   - Only requirements for running noWorkflow are PyPosAST, SQLAlchemy, and python-future. 
      The other libraries are only used for provenance analysis. Can simply run 
      "pip install noworkflow" if only want noWorkflow, PyPosAST, SQLAlchemy, and python-future.


### RDataTracker Installation:
Install via git.
1. Setup an R console session (call "R" in the command line). Check version. 
   Ubuntu 18.04 comes with R version <3.6 so to install latest R do the following:
   a) install necessary packages to add a new repository over HTTPS:
       ```sudo apt install apt-transport-https software-properties-common```
   b) enable the CRAN repo:
       ```sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9```
   c) add the CRAN GPG key to system:
       ```sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'```
   d) update packages list and install R package:
       ```sudo apt update```
       ```sudo apt install r-base```
2. install devtools (```install.packages("devtools")```)
   a) because many of the R packages were installed on a previous R version 
       you may need to install dependent packages.
   b) call library(devtools) to import
3. install ggplot2 (```install.packages("ggplot2")```)
4. install rdtLite via git
    ```install_github("End-to-end-provenance/rdtLite")```
5. ```call library(rdtLite)``` to import

Now you can use rdtLite via command-line (prov.init) or in the shell (prov.run). You can set the location of the saved prov.json as a formal parameter of either function. 
More information can be found here: https://github.com/End-to-end-provenance/rdtLite
-----------------------------------------------------------------------------------------

# System-Level Provenance and End2End Functionality

The following can be accessed through the docker container or virtual machine. Both of which you can find on my github repo: https://github.com/narunraman/EndtoEndProvenance

## CamFlow installation:
You should be able to install CamFlow from source via the instructions on http://camflow.org.

For a clean install on Fedora 29 you may need to install some or all of the following: pygpgme, gcc, gcc-c++, patch, ruby, uncrustify, flex, bison, ncurses-devel, elfutils-libelf-devel, openssl-devel (via sudo yum install <package-name> or with Fedora >=22 sudo dnf install <package-name>).
Below are the packages required on the camflow website.

```
sudo dnf groupinstall 'Development Tools'
sudo dnf install ncurses-devel cmake clang gcc-c++ wget git openssl-devel zlib patch mosquitto bison flex ruby
```

## Prov-CPL installation:
Follow the installation process from https://github.com/ProvTools/prov-cpl
If you are getting a postgres user authentification error, you may need to do the following:
1. open the pg_hba.conf file (it should be in /etc/postgres/<version-num>/main)
	local	all 		postgres		peer
   to
	local	all		postgres		trust
2. Restart the psql server:
	```$ sudo service postgresql restart```
3. Login to psql and set password:
	```$ psql -U postgres```
	```db> ALTER USER postgres with password 'your-password';```
4. Now change the pg_hba.conf file to:
	local	all		postgres		trust
   to
	local	all		postgres		md5
5. Now restart psql server and you should be good to go.
