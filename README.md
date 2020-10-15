# CSCI4502Project

## Setup
Ensure python3 is installed
```bash
python --version
```
If using Mac/Linux, sometimes `python` refers to python 2 and `python3` is required. Use whatever gives you the correct version.

First, create and activate a python virtual environment. NOTE: after inital creation, just activate the existing environment
```bash
python -m venv <venv_name>
```
For windows,
```bash
.\<venv_name>\Scripts\activate
```
For Mac/Linux users, 
```bash
source <venv_name>/bin/activate
```
Second, install all requirements using the following command
```bash
pip install -r requirements.txt
```
To run example query I've set up
```bash
python queries.py
```

## Explanation of File Structure
`models.py`contains the python classes used to represent our database tables\
`queries.py` establishes the database connection and can be used to execute queries\
`requirements.txt` contains a list of the python packages neccessary to interact with our database\
`.vscode/` contains editor settings. While you're not required to use vscode, these settings will keep our formatting consistent\
`.env` contains environment variables neccessary to connect to the database. NOTE: this is .gitignore'd, and you'll have to add this file yourself. This is becuase we do not want our database information stored on github. PLEASE PLEASE be careful with this and do not commit my connection info to github :)
