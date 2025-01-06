West Coast Ocean Alliance (WCOA) Data Portal
=====

Django web application and Wagtail CMS for the West Coast Ocean Data Portal.

## Local Vagrant Development Env

requirements:
  - git
  - vagrant

1. Choose a working project directory that will be referred to from here has PROJDIR (i.e. /home/username/src/ ). It is best if it’s a directory you use to hold all of your dev projects.
  ```
  cd PROJDIR
  git clone https://github.com/Ecotrust/marco-portal2.git
  mv marco-portal2 ocean_portal
  cd ocean_portal
  vagrant up
  vagrant ssh
  ```

2. Install dependencies
  ```
  sudo apt update
  sudo apt upgrade -y
  sudo apt install git python3 python3-dev python3-virtualenv python3-pip postgresql postgresql-contrib postgis postgresql-server-dev-14 libjpeg-dev gdal-bin python3-gdal libgdal-dev -y
  ```

3. Edit requirements.txt
  ```
  vim /usr/local/apps/ocean_portal/requirements.txt
  ```

4. Add WCOA app to requirements.txt
  ```
  -e git+https://github.com/Ecotrust/wcoa.git@master#egg=wcoa-master
  ```

5. Set up virtualenv
  ```
  python3 -m pip install --user virtualenv
  cd /usr/local/apps/
  sudo chown ${USER}:${USER} ./
  python3 -m virtualenv env
  source /usr/local/apps/env/bin/activate
  pip install -r /usr/local/apps/ocean_portal/requirements.txt
  pip uninstall numpy
  gdal-config --version
  pip install "pygdal<'REPLACE with gdal-config version'"
  ```
  if any of your packages were copied locally rather than pulled via requirements.txt, use pip to install them now:
  ```
  pip install -e /usr/local/apps/ocean_portal/apps/...
  ```

6. Install database
  ```
  sudo -u postgres createdb -O postgres ocean_portal
  sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" ocean_portal
  sudo vim /etc/postgresql/12/main/pg_hba.conf
  #--------
  	<update line near bottom regarding ‘local   all   postgres’
  		Change ‘peer’ to ‘trust’ >
  #---------
  sudo service postgresql restart
  ```

7. Configure project
  ```
  cd /usr/local/apps/ocean_portal/marco
  mkdir media
  mkdir static
  mkdir /usr/local/apps/marco_portal_static/
  cp config.ini.template config.ini
  vim config.ini
  ```

8. Edit config.ini
  - Add the following lines under `[App]`:
    ```
      PROJECT_APP = wcoa
      PROJECT_SETTINGS_FILE = True
      MEDIA_ROOT = /usr/local/apps/ocean_portal/marco/media
  	  STATIC_ROOT = /usr/local/apps/ocean_portal/marco/static
    ```
  - Add the following under [DATABASE]:
    ```
      USER = postgres
  	  NAME = ocean_portal
    ```

9. Add shortcuts
  ```
  vim ~/.bashrc
  #----------
  alias dj="/usr/local/apps/env/bin/python3 /usr/local/apps/ocean_portal/marco/manage.py"

  alias djrun="dj runserver 0:8000"
  #----------
  ```

10. Exit ssh session and re-ssh in
  ```
  crtl+d
  vagrant ssh
  ```

11. Set up Django
  ```
  dj makemigrations
  dj migrate
  dj compress
  dj collectstatic
  dj loaddata /usr/local/apps/ocean_portal/marco/marco_site/fixtures/content.json
  djrun
  ```

12. Open http://localhost:8000 in your browser

13. Create super user
  ```
  dj createsuperuser
  ```

14. Open http://localhost:8000/django-admin and http://localhost:8000/admin in your browser to administer the site





Notes

Forked Marco-portal-2 from MidAtlanticPortal GitHub account to Ecotrust:
https://github.com/Ecotrust/marco-portal2

Cloned it locally, updated the vagrant file to give me an Ubuntu 18.04 LTS box

vagrant up
vagrant ssh

sudo apt-get update
sudo apt-get upgrade

The Compass install docs were a nice guideline for setting up MP, perhaps they will be useful for the portal as well….
https://github.com/Ecotrust/COMPASS/wiki/install

## Upgrading Wagtail
Upgrading to Wagtail 2.0+: https://wagtail.io/blog/upgrading-to-wagtail-2/

## Functional Testing
Functional testing is done with Selenium and the Chrome WebDriver. The tests are located in the `functional_tests.py` file. To run the tests, you will need to have Selenium, Google Chrome, and the Chrome WebDriver installed and available in your PATH. Here is how:

1. Install Selenium
  ```
  pip install selenium
  ```
2. Install Google Chrome
  ```
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo apt install ./google-chrome-stable_current_amd64.deb
  ``` 
3. Install Chrome WebDriver
You will need to know the current stable version of Chrome you installed in step 2. You can go to [https://chromedriver.com/download](https://chromedriver.com/download) to find the url for the latest stable version of the Chrome WebDriver. Then use the URL in the following command:
  ```
  wget <URL>
  ```
unzip and install the driver
  ```
  unzip chromedriver_linux64.zip
  sudo mv chromedriver-linux64/chromedriver /usr/local/apps/env/bin/
  ```

4. Run Tests
You can now run functional tests just like you would other Django tests.
**Note:** *You will need to have the server running to run the functional tests.* 
  ```
  python manage.py test
  ```





 ## Production Installation (Ubuntu 18.04 LTS)
 #### set up new server
 ```
 sudo apt update
 sudo apt upgrade -y
 sudo apt install git python3 python3-dev python3-virtualenv python3-pip postgresql postgresql-contrib postgis postgresql-server-dev-12 libjpeg-dev gdal-bin python-gdal python3-gdal libgdal-dev redis -y
 sudo mkdir /usr/local/apps
 ```
 change ownership of /usr/local/apps to be your primary sudo user:
 `sudo chown {USERNAME} /usr/local/apps`

 ```
 cd /usr/local/apps/
 git clone https://github.com/Ecotrust/marco-portal2.git
 mv marco-portal2 ocean_portal
 cd ocean_portal
 git checkout wcoa
 git pull
 ```

 #### Set up virtualenv
  ```
  python3 -m pip install --user virtualenv
  cd /usr/local/apps/ocean_portal/
  python3 -m virtualenv env
  source /usr/local/apps/ocean_portal/env/bin/activate
  pip install -r /usr/local/apps/ocean_portal/requirements.txt
  pip install -e git+https://github.com/Ecotrust/wcoa.git@master#egg=wcoa-master
  ```

#### Install PyGDAL
  ```
  pip uninstall numpy
  gdal-config --version
  ```
  Note what version is printed. You will want to intall the correct pygdal for your system's GDAL.

  For example, if the printed version is '2.2.3', then you will want the latest pyGDAL in the 2.2.3 family:
  `pip install "pygdal<2.2.4"`

  You should see a new version of numpy installed as well.

#### Install database
  Create a Database user. Come up with a meaningful username and a secure password. You will use the username in place of `{DBUSER}` below and you will be prompted to create the new user's password immediately.
  ```
  sudo -u postgres createuser -s -P {DBUSER}
  sudo -u postgres createdb -O {DBUSER} ocean_portal
  sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" ocean_portal
  sudo vim /etc/postgresql/10/main/pg_hba.conf
  ```
  Add the following line to the bottom of the pg_hba.conf file, replacing `{DBUSER}` with the username you created:
  ```
  local   ocean_portal    {DBUSER}                               md5
  ```
  Finally, restart postgres so your updated configuration can be implemented.
  ```
  sudo service postgresql restart
  ```

#### Configure project
  ```
  cd /usr/local/apps/ocean_portal/marco
  mkdir media
  mkdir static
  cp config.ini.template config.ini
  vim config.ini
  ```

#### Edit config.ini
  - Add the following lines under `[App]`:
    ```
      PROJECT_APP = wcoa
      PROJECT_SETTINGS_FILE = True
      MEDIA_ROOT = /usr/local/apps/ocean_portal/env/src/wcoa-master/media
  	  STATIC_ROOT = /usr/local/apps/ocean_portal/marco/static
      EMAIL_SUBJECT_PREFIX = [WCOA]
    ```
    - If you already know your URL, you can put that in for `ALLOWED_HOSTS`
  - Add the following under [DATABASE] (replacing `{DBUSER}` and `{DBPASSWORD}` with the database user and password you created above):
    ```
  	  NAME = ocean_portal
      USER = {DBUSER}
      PASSWORD = {DBPASSWORD}
    ```

#### Add Django shortcuts
  ```
  vim ~/.bashrc
  #----------
  alias dj="/usr/local/apps/ocean_portal/env/bin/python3 /usr/local/apps/ocean_portal/marco/manage.py"
  #----------
  ```
  Exit your terminal session and re-SSH in to the server to load your updates

#### Django Initialization
  ```
  dj migrate
  dj compress
  dj collectstatic
  ```

#### Load in initial data
  There is no prescribed method for this. If you have access to existing servers, you have the following two options.
  If you don't have access to existing servers, you'll need to just try to build from scratch.
  ##### With pg_dump
  You can use pg_dump to generate a .sql file representing the database. You can use scp to copy that onto your new server then do the following:
  ```
  sudo -u postgres dropdb ocean_portal
  sudo -u postgres createdb -O {DBUSER} ocean_portal
  sudo -u postgres psql ocean_portal < {YOUR_DUMP_FILE}
  dj migrate
  ```
  ##### With fixtures
  * on the source (old) server
  ```
  dj dumpdata --indent=2 {your app_models} > /usr/local/apps/ocean_portal/marco/marco/fixtures/initial_data.json
  ```
  * Use scp to copy that to your new server
  * on the target (new) server
  ```
  dj loaddata /usr/local/apps/ocean_portal/marco/marco/fixtures/initial_data.json
  ```

#### Configure and enable webapplication server stack: Nginx + uWSGI
For reference [go here](http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)

From inside your virualenv:
* `sudo apt-get install nginx uwsgi uwsgi-plugin-python3 -y`
* `pip install uwsgi`
* `sudo cp /usr/local/apps/ocean_portal/env/src/wcoa-master/deploy/nginx_config /etc/nginx/sites-available/wcoa`
* `sudo rm /etc/nginx/sites-enabled/default`
* `sudo ln -s /etc/nginx/sites-available/wcoa /etc/nginx/sites-enabled/wcoa`
* `sudo cp /usr/local/apps/ocean_portal/env/src/wcoa-master/deploy/emperor.ini /etc/uwsgi/`
* `sudo cp /usr/local/apps/ocean_portal/env/src/wcoa-master/deploy/uwsgi.service /etc/systemd/system/`
* `sudo systemctl enable uwsgi.service`
* `sudo cp /usr/local/apps/ocean_portal/env/src/wcoa-master/deploy/wcoa.ini /etc/uwsgi/apps-enabled/wcoa.ini`
* `sudo service nginx start`
   * If this fails, apache2 may already be running and hogging port 80.
      * you can stop apache2 with `sudo service apache2 stop` - but it will restart on reboot.
         * prevent it from launching on reboot with `sudo update-rc.d apache2 disable` OR
         * update your apache2 configuration to run on another port
* `sudo service nginx restart`
* `sudo reboot`
* In a few minutes, test your URL in a browser to see that everything came up as expected

#### Install munin
`sudo apt install munin munin-node -y`

#### Configure unattended upgrades
* `sudo apt install unattended-upgrades`
* `sudo vim /etc/apt/apt.conf.d/50unattended-upgrades`
   * Uncomment the "...-updates" line
   * Uncomment and configure:
      * Mail
      * MailOnlyOnError
   * Remove-Unused-Kernel-Packages "true";
   * Remove-Unused-Dependencies "true";
   * Automatic-Reboot "true";
   * Automatic-Reboot-Time "8:00";
      * The above assumes a UTC server with assumed 1 or 2 AM Pacific time downtime
* `sudo vim /etc/apt/apt.conf.d/20auto-upgrades`
```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
```
* `sudo unattended-upgrades --dry-run --debug`

#### Install Certbox and configure SSL Certs
Requirements:
   * URL for your site with DNS configured
   * external access to port 80
   * external access to port 443
   * access to a preferred email address to receive any alerts about your SSL certificates

If you have not already done so, edit /usr/local/apps/ocean_portal/marco/config.ini in the [APP] section:
   * `ALLOWED_HOSTS = {SITE_URL}` where `{SITE_URL}` is your site's intended address
Then restart uWSGI: `sudo service uwsgi restart`

Install certbot:
* `sudo apt install software-properties-common -y`
* `sudo add-apt-repository ppa:certbot/certbot`
   * press Enter to continue
* `sudo apt update`
* `sudo apt install python-certbot-nginx -y`

Configure NGINX:
```
sudo cp /etc/nginx/sites-available/wcoa /etc/nginx/sites-available/wcoa.http_only
sudo vim /etc/nginx/sites-available/wcoa
```
* Replace the line `server_name _;`  with `server_name {SITE_URL}` where `{SITE_URL}` is your site's URL address
* Save
* Test your NGINX configuration: `sudo nginx -t`
* Restart NGINX: `sudo service nginx restart`
* Test your website out in a browser to be sure your DNS is resolving correctly.

Get your SSL Certificate, replace `{SITE_URL}` with your URL address:
```
sudo certbot --nginx -d {SITE_URL}
```
* provide your email address
* agree to their terms: https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf
* choose whether or not to have your email address shared with eff.org
* select if you want users hitting the site using HTTP to be automatically redirected to HTTPS

Test your SSL Cert installation:
* hit your site using HTTPS (or HTTP if you chose to have automatic redirection)
* Inspect your URL using https://www.ssllabs.com/ssltest/
* Check that Certbot auto-renew is properly configured:
   * `sudo certbot renew --dry-run`


#### Set up external uptime monitoring
recommended: https://uptimerobot.com

#### Restart your server and test
