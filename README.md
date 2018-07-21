# maps-server
How to run Python API?

1. It's better to use virtual environment, so you can keep it isolated from the system python. Python3 is preferred
    - `pip install virtualenv`
    - For python 2.x
      `virtualenv blogit` 
    - For python 3.x
      `virtualenv -p python3 blogit`
      
2. `cd blogit && git clone https://github.com/gdsouza1992/maps-server.git`

3. `pip install -r maps-server/requirements.txt`    OR    `pip3 install -r maps-server/requirements.txt`

4. `cd maps-server/app && python controller.py runserver --port 7777 --host 0.0.0.0`

5. Logs are located at *maps-server/app/logs/*


Password to access the DB is present /etc/blog-it/mongodb-passwd in the following format

{
  "user": "app",
  "password": "changeme",
  "db": "demo-blogit"
}


<a href="https://github.com/gdsouza1992/maps">Client app here</a>
