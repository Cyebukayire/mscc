# Make Sense Of The Copyright Office Comments

An application to summarize and create useful metadata from the comments made on Regulations.gov. This will be useful to the Copyright Office and other people trying to understand the Comments as a demonstration of the utility of computational analysis of the text.

## Getting started

### Clone project
Open the terminal and run the command to download the project
```sh
 $ git clone [https://github.com/atlp-rwanda/rca-phantom-team1-fe.git](https://github.com/Cyebukayire/mscc.git)
```

### Go to the project folder
Use the 'cd' command to navigate to where the project folder is
```sh
 $ cd mscc
```

### Open working environment
Check if 'pip' is already installed on your device with this command: ``` pip version```

If the output does not run successfully to show the version of pip, then install pip with the command below.

Choose the command to run based on your computer's Operating System.

. Install pip on Linux: ``` python get-pip.py```

. Install pip on MAC OS: ``` python get-pip.py```

. Install pip on Linux OS: ``` C:> py get-pip.py```


Still in the 'mscc' folder, create a virtual environment where the project runs. All dependencies and packages required to run the project will automatically be installed in the virtual environment. 

```sh
 $ pipenv shell
```

### Run the project
In the same terminal, run the following command to start the project, replace the DEMO_KEY with your API Key from [Regulations.gov](https://open.gsa.gov/api/regulationsgov/). If you don't have the key already, the command below will still work for now using a DEMO_KEY as the default.

```sh
 $ API_KEY="DEMO_KEY" uvicorn main:app --reload
```


#### On successful execution, this link(http://127.0.0.1:8000) will appear in your terminal. Open the link in your browser.

This is the current output in the browser:

![image](https://github.com/Cyebukayire/mscc/assets/55869293/2b987518-d16a-49d9-b611-02b51aa54648)


#### Navigate to the documentation of the API (http://127.0.0.1:8000/docs)

Below is a screenshot of the current API documentation:

![image](https://github.com/Cyebukayire/mscc/assets/55869293/3e6873ac-847e-46f8-afc5-70602ef1135b)


### Test the API by extracting simple metadata

#### Click on the "Get" button:

![image](https://github.com/Cyebukayire/mscc/assets/55869293/200db5c8-fe2f-4fe6-8e8c-0c28725e91fd)


#### Click on the "Try it out" button to test the API:

![image](https://github.com/Cyebukayire/mscc/assets/55869293/0f0e7cf4-08e0-4c7c-9c64-ccfcc4b5ab9d)


#### Input a valid comment ID in the empty field then press the "Execute" button to retrieve the metadata of that comment:

![image](https://github.com/Cyebukayire/mscc/assets/55869293/71c29721-5b1c-4328-a178-af587ec2610f)


On a successful extraction of data, the metadata is displayed:

![image](https://github.com/Cyebukayire/mscc/assets/55869293/db95fcd6-ab95-4956-9964-d69580af7747)


### Access the output metadata

After extracting the metadata of a comment, the "output" folder is created in the project directory. The folder contains an Excel file "metadata.xlsx"

Every time new metadata is extracted, the metadata is added to the Excel file.



