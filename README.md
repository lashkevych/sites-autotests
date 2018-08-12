1. Load and install [python 3](https://www.python.org/downloads/windows/), including
 - adding Python to the PATH 
 - install pip

2. Install virtualenv

```
> pip install virtualenv
```

3. Load and install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/#section=windows)

4. Clone [GitHub Repo](https://github.com/lashkevych/sites-autotests) (`Clone or Download` Button -> `Open in Desktop`), 
for example into `C:\Users\HP\Documents\GitHub\sites-autotests\`

5. Create virtual env 
in folder `C:\Users\HP\Documents\GitHub\sites-autotests\` execute the following command

```
> virtualenv.exe _env
```

6. Launch cmd and activate virtual env in it (to add to begining of the `PATH` ENV VARIABLE path to the scripts folder of virtual env)

```
> C:\Users\HP\Documents\GitHub\sites-autotests\_env\Scripts\activate.bat
```
    
7. Install requirements into the virtual env (in the same cmd where we activated virtual env) 

```
pip install -r requirements.txt 
```

// you should be in root project dir (where `reqiurements.txt` is located)

8. Open Project in PyCharm  

9. Download Selenium driver for Chrome and put in Project root

10. Install Pytest plugin for PyCharm (`File->Settings->Plugins`) 

11. Create `config.py` file based on `config.py.template`


#Testing by using IE and Edge

1. Check [driver reference](https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver#required-configuration)
for the initial configuration that should) be done for IE.

2. Specify in PyCharm configuration file for PyTest(instead of default - `pytest.ini`) `-с c:/path_to_non_default_ini_file/pytest-ie.ini`
![Specify configuration file for PyTest](img/Specify_configuration_file_for_PyTest.png)

3. Add all site (all resellers and all qa-env) to trusted sites for IE ("Свойства броузера/Безопасность/Надежные сайты"):
![Trusted sites configuration](img/IE_trusted_sites.png)
 
 #Fully Automatic Test in IE
1. In order to use fully automated tests with IE follow instructions on [MITM configuration](https://github.com/lightbody/browsermob-proxy/blob/master/mitm/README.md).
A short (and insecure) way: add browserproxy certificate `ca-certificate-rsa.cer` to windows as a trusted Certificate Authority
 as described in [this doc](https://support.comodo.com/index.php?/comodo/Knowledgebase/Article/View/636/17/) 
 
2. Set manual proxy in IE Internet Configuration to localhost:8081

3. Make sure there are no java.exe processes hanging around after the previous test run. Sometimes browserproxy does not stop correctly by unknown reason.
If you do not stop them you will see a entry in test log near the beginning mentioning port like 8082 or 8083 but it should be 8081. 