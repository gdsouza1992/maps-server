# maps-server
How to run Python API?

1. It's better to use virtual environment, so you can keep it isolated from the system python. Python3 is preferred
    - `pip install virtualenv`
    - For python 2.x
      `virtualenv blogit` 
    - For python 3.x
      `virtualenv -p python3 blogit`
      
2. Clone the git repo
    - `cd blogit && git clone https://github.com/gdsouza1992/maps-server.git`

3. Install necessary python packages
    - For python 2.x `pip install -r maps-server/requirements.txt`
    - For python 3.x `pip3 install -r maps-server/requirements.txt`

4. Activate python virtual env
    - `source bin/activate`

5. Navigate to the app directory and start the program with appropriate host and port
    - `cd maps-server/app && python controller.py runserver --port 7777 --host 0.0.0.0`

6. Logs are located at *maps-server/app/logs/*


Password to access the DB is present /etc/blog-it/mongodb-passwd in the following format

{
  "user": "app",
  "password": "changeme",
  "db": "demo-blogit",
  "cipherkey": "secret-key"
}


<a href="https://github.com/gdsouza1992/maps">Client app here</a>
