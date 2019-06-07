# team GPStuy <img src="https://d1lss44hh2trtw.cloudfront.net/assets/article/2015/07/06/Azrael_Returns_feature.jpg" height="40">
Snitch Tung, WalkMax Lu, Jeffreezy Wusuk Lee, Ivan Z-hang

**[Devlog](https://github.com/WilliamLu0211/GPStuy/blob/master/doc/devlog.txt)**

## GPStuy: For Noobs...

### Abstract:
GPStuy is your personal navigator for Stuy. Input two rooms and we'll show you how to get there. Input your schedule and we'll map out your entire day. If you're an admin, you can mass email parents in preparation for Parent-Teacher Conferences.

### Dependencies: 
Our dependencies, as listed in requirements.txt, are as follows:
```
Click==7.0
Flask==1.0.3
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
Werkzeug==0.15.4
```

Install our dependencies with the follow command in the root directory of our repo:
```
pip3 install -r requirements.txt
```

### Instructions:
1. Clone the repo

**ssh**
```
git clone git@github.com:WilliamLu0211/GPStuy.git
```

**https**
```
git clone https://github.com/WilliamLu0211/GPStuy.git
```

2. (optional) make a virtual env
```
python3 -m venv <venv_name>
```

3. (optional) activate virtual env
```
. <path-to-venv>/bin/activate
```

4. enter the repo directory
```
cd <path-to-repo>
```

5. install requirements

**python 3.7**
```
pip3 install -r requirements.txt
```

**if in virtual env with python 3.7**
```
pip install -r requirements.txt
```

6. run the app.py with python3 (MUST BE PY3!!!!)

**python 3.7**
```
python3 app.py
```

**if in virtual env with python 3.7**
```
python app.py
```

7. go to localhost 127.0.0.1:5000 on any browser

   http://127.0.0.1:5000/

## Apache2 Launch Instructions
1. SSH into droplet

```$ ssh <username>@<ip>```

2. Go to www and create a directory named after your app
```
$ cd ../../var/www
$ mkdir <app>
$ cd <app>
```
3. Switch to root

```
$ sudo su
```

4. Create wsgi file

```
$ touch <app>.wsgi
```

5. Clone via https

```
$ git clone https://github.com/WilliamLu0211/GPStuy.git
```

6. Change permissions

```
$ chgrp -R www-data <app>
$ chmod -R g+w <app>
```

7. rename `app.py` and install requirements

```
$ cd <app>
$ mv app.py __init__.py
$ pip3 install -r requirements.txt
```

8. Enable Site

```
$ cd ~/../../etc/apache2/sites-enabled/
$ touch <app>.conf
$ a2ensite <app>
```

9. Reload and restart apache2

```
service apache2 reload
service apache2 restart
```
