# Crowd Funding 

<p align="center">
<img src="logo.png" alt="Build Status">
</p>

It is a Web Application for crowd funding projects.

# Installation

1. Install python version 3
2. Install Rails version 2.1
3. Install MySQL Database Engine
4. Create an empty database called **crowd_funding**
5. Edit settings.py and set ``username`` , `` password`` and `` host`` of your database engine. This will allow us to run the migrations.
6. create a new vertual environment 
```bash
virtualenv [environment name]
```
and activate it
```bash
source  [environment name]/bin/activate
```

7. Run the Following command to install the dependencies of the project inside the virtual environment
```bash
	pip3 install -r requirements.txt
```
8. Run the Following command to create migration files
```bash
	python3 manage.py makemigrations
```
then to create the tables in the database
```bash
	python3 manage.py migrate
```
## Usage

Run the following command to launch the app 
```bash
 python3 manage.py runserver
```

## User Features

1. Register.
2. Login (after email activation only).
3. View projects and make donations for them. 
4. Filter the current project to search for a specific Project.
5. Comment and rate the Projects.
6. Report any inappropriate content (projects or comments)
7. Post your own projects to get Donations.

## Built With

[Django 2.1.0](https://www.djangoproject.com/)
## Authors

* **Ahmed Adel**      - [AhmedAdelFahim](https://github.com/AhmedAdelFahim)
* **Basma Mohammed**  - [basmmohamed](https://github.com/basmmohamed)
* **Ebtsam Ali**      - [ebtsamali](https://github.com/ebtsamali)
* **Kareem Morsy**    - [kareemMorsy30 ](https://github.com/kareemMorsy30)
* **Maged Naim**      - [Maged-Naim ](https://github.com/Maged-Naim)
* **Mohammed Naguib** - [MNaguib2611](https://github.com/MNaguib2611)
