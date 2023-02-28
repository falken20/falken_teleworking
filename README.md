<div align="center">
  
<!-- Para logo se puede usar https://studio.tailorbrands.com/-->
<img src="./static/assets/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://richionline-portfolio.nw.r.appspot.com/static/assets/falken_logo.ico" width=40 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.5.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/falken_teleworking) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/falken_teleworking) ![Test coverage](https://img.shields.io/badge/test%20coverage-88%25-green) ![GitHub License](https://img.shields.io/github/license/falken20/falken_teleworking)[![Python used version](https://img.shields.io/static/v1?label=python&message=3.8&color=blue&logo=python&logoColor=white)

  
[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com) [![Twitter](https://img.shields.io/twitter/follow/richionline?style=social)](https://twitter.com/richionline)
</div>

---
# falken_teleworking
App for teleworking days control

##### Deploy
```bash
gcloud app deploy
```

##### Setup
```bash
pip install -r requirements.txt
```

##### Running the app
```bash
flask run
```

##### Setup tests
```bash
pip install -r requirements-tests.txt
```

##### Running the tests with pytest and coverage
```bash
./check_app.sh
```
or
```bash
coverage run -m pytest -v && coverage html --omit=*/venv/*,*/tests/*
```

##### Environment vars
```bash
FALKEN_VERSION = "1.0.0"
ENV_PRO = N
LEVEL_LOG = ["DEBUG", "INFO", "WARNING", "ERROR"]
```

---

##### Versions
- 1.5.0 Save data with logged user
- 1.4.0 Adding new calendar component
- 1.3.0 Adding calendar
- 1.2.0 Include login module and new design
- 1.0.1 Including tests
- 1.0.0 Application

---
##### learning tips
- flash(): By calling flash function, you can send a message to the next request.
- UserMixin: Flask-Login can manage user sessions. 
- LoginManager: A user loader tells Flask-Login how to find a specific user from the ID that is stored in their session cookie. 
- @login-required: Decorator to protect a page when using Flask-Login.
- current_user: Object that represents the user from the database and provides access all of the attributes of that user with dot notation.
- Bulma: CSS framework (https://bulma.io/)
- Help to apply Flask-Login (https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)
- Calendar component (https://fullcalendar.io/)