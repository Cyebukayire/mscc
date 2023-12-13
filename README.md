# Make Sense Of The Copyright Office Comments

An application to summarize and create useful metadata from the comments made on Regulations.gov. This will be useful to the Copright Office and other people trying to understand the Comments as a demonstration of the utility of computational analysis of text.

## Geting started

### Clone project
Open terminal and run the command to download the project
```sh
 $ git clone [https://github.com/atlp-rwanda/rca-phantom-team1-fe.git](https://github.com/Cyebukayire/mscc.git)
```

### Go to project folder
Use 'cd' command to navigate to where the mscc folder is
```sh
 $ cd mscc
```

### Open working environment
Check if 'pip' is already installed on your device with this command: ``` pip version```
If the output does not run successfully to show the version of pip, then install pip.

Choose command to run below based on your computer's Operating System.
. Install pip on Linux: ``` python get-pip.py```
. Install pip on MAC OS: ``` python get-pip.py```
. Install pip on Linux OS: ``` C:> py get-pip.py```

Still in the 'mscc' folder, create a virtual environment where the project runs from. All dependencies and packages required to run the project will autumatically be installed in the virtual environment. 

```sh
 $ pipenv shell
```

### Run the project
In the same terminal, run the following command to start the project, replace the DEMO_KEY with your API Key from [Regulations.gov](https://open.gsa.gov/api/regulationsgov/). If you don't have the key already, the command below will still work for now using a DEMO_KEY as the default.

```sh
 $ API_KEY="DEMO_KEY" uvicorn main:app --reload
```
