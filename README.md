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