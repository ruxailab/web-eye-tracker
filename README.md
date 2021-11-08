# 👁️ Eye Lab: Gaze Tracker API

Eye Lab is an open source tool to create eye tracking usability tests. It started as a final undergraduation work for Computer Engineering of student [Karine Pistili](https://www.linkedin.com/in/karine-pistili/) that created the first prototype. The idea is to evolve it to a more complete and useful tool with the help of the community.

The current version of the software allows users to create their usability sessions of an website, recording the webcam, screen and mouse movements and use this information to find out where the user has been looking into the screen by using heatmaps.

## 👩‍💻 Setting up project locally

The project consists of two parts, this repository contains the backend of the application and the frontend can be found [here](https://github.com/uramakilab/web-eye-tracker-front). Install it as well.

### Prerequisites

* [Python 3x](https://www.python.org/downloads/)

### 1. Create virtual environment

Before installing all dependencies and starting your Flask Server, it is better to create a python virtual environment. You can use the [venv package](https://docs.python.org/3/library/venv.html)

```
python -m venv /path/to/new/virtual/environment
```

Then activate your env. On windows for example you can activate with the script:

```
name-of-event/Scripts/activate
```

### 2. Install dependencies

Install all dependencies listed on the requirements.txt with:

```
pip install -r requirements.txt
```

### 3. Run the Flask API

```
flask run
```

### 4. Setting up Firebase Project

This backend uses Cloud Firestore as database. You will have to create a Firebase project and enable Cloud Firestore if you still want to use this configuration. 

After having it created you will need to generate a service account json key. Save it in the **root** of the project with the name **serviceAccountKey.json**


### 5. Deploy to Heroku

This project has been configured to be deployed in production on Heroku. If you want to deploy it there, you will need to first create a project and link it to the code.

### 6. GitHub CI/CD

CI/CD from the github actions workflows is implmented for deploy on heroku. If you want to use the workflow for repository you can edit *.github/workflows/main.yml* file with your settings.

## 🧑‍🤝‍🧑 Contributing

Anyone is free to contribute to this project. Just do a pull request with your code and if it is all good we will accept it. You can also help us look for bugs, if you find anything create and issue.

## 📃 License

This software is under the [MIT License](https://opensource.org/licenses/MIT). 

Copyright 2021 Uramaki Lab
