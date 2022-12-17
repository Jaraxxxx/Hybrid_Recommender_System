# Movie-Recommender-System

A Web Based Movie Recommendation Engine using Hybrid Filtering that comrpises of Content Based Filtering and Collaborative Filtering.
The Content Based Filtering filters the movies based on the parameters such as (genre,director_name,starcast,overview).
This set of Filtered Movies is the passed through an Collaborative Based Filtering which then filters the movies based on the interest shared by the other users in the sytem.

### Screenshot

###### Home page
![image](https://user-images.githubusercontent.com/49514423/208250592-9f4b07ab-ca39-441c-bb9a-f86ce38a811b.png)


###### Login Page
![image](https://user-images.githubusercontent.com/49514423/208250637-0503862f-1cf9-4569-a38f-4c6ca3709ec4.png)

###### Sign Up Page
![image](https://user-images.githubusercontent.com/49514423/208250675-4dcb66f6-55f7-4cb4-ab55-ffdcb7ab12c4.png)


###### Recommendation page
![image](https://user-images.githubusercontent.com/49514423/208250785-f45add15-00d8-421a-b46d-0bc0a46c5768.png)


###### Rating page
![image](https://user-images.githubusercontent.com/49514423/208250726-6f201c6f-06e5-42ba-8d86-5364674642d8.png)


### Technologies Used

#### Web Technologies
Html , Css , JavaScript , Bootstrap , Django

#### Machine Learning Library In Python3
Numpy , Pandas , Scipy

#### Database
SQLite

##### Requirements
```
python 3.6 or more

pip3

virtualenv
```
##### Setup to run

Extract zip file in your computer

Open terminal/cmd promt

Goto that Path

Example

```
cd ~/Destop/Movie-Recommender-System
```
Create a new virtual environment on that directory

```
If virtualenv is not installed on the machine.
virtualenv --python <path_to_python_director>\python.exe venv
virtualenv .
```

Activate Your Virtual Environment

for Linux
```
source bin/activate
```
for Windows
```
cd Scripts
then
activate
```
To install Dependencies

```
pip install -r requirements.txt
```

### Creating Local Server

Goto src directory, example

```
cd ../Movie-Recommender-System/src
```
To run
```
python manage.py runserver
```
Now open your browser and go to this address
```
http://127.0.0.1:8000
```
Thank you for visiting my repository.
