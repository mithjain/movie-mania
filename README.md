## Installation

### Setup Database

```bash
 sudo su - postgres
 psql
 CREATE DATABASE <movie_mania>;
 CREATE USER <my-user-name> WITH PASSWORD 'password';
 GRANT ALL PRIVILEGES ON DATABASE <movie_mania> TO <my-user-name>;
 \q
```

### Setup Backend

```bash
 sudo apt install python3.9-dev
```

* Setting up the virtualenv

```bash
 # create virtualenv
 cd backend/
 virtualenv -p python3.9 venv
 source venv/bin/activate

# install requirements
 pip install -r requirements.txt

cp .moviesenv.sample .moviesenv

* After setting up above things, change the `.moviesenv` file according to your requirements
````

### To RUN backend

```bash
 python manage.py migrate
 
 # load movies.csv into database
 python manage.py loaddata movies
 
 python manage.py runserver
```

### Setup Frontend
only supports **Nodejs 14.x** and **NPM 7.x**,
install it before running below commands
```bash
  cd ..
  cd frontend
  npm install npm@7.0.7 -g
  npm ci
  npm run serve
```
* The server would be running on `localhost:8080`