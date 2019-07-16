=====
West Coast Ocean Alliance
=====

WCOA is an app for the West Coast Ocean Data Portal.

## Install Ocean Portal

### Local Vagrant Development Env

requirements:
  - git
  - vagrant

1. Choose a working project directory that will be referred to from here has PROJDIR (i.e. /home/username/src/ ). It is best if it’s a directory you use to hold all of your dev projects.
  ```
  cd PROJDIR
  git clone https://github.com/Ecotrust/marco-portal2.git
  mv marco-portal2 ocean_portal
  cd ocean_portal
  git checkout origin/wcoa
  vagrant up
  vagrant ssh
  ```

2. Install dependencies
  ```
  sudo apt update
  sudo apt upgrade -y
  sudo apt install git python3 python3-dev python3-virtualenv python3-pip postgresql postgresql-contrib postgis postgresql-server-dev-10 libjpeg-dev gdal-bin python-gdal python3-gdal libgdal-dev -y
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
  cd /usr/local/apps/ocean_portal/
  python3 -m virtualenv env
  source /usr/local/apps/ocean_portal/env/bin/activate
  pip install -r /usr/local/apps/ocean_portal/requirements.txt
  pip uninstall numpy
  gdal-config --version
  pip install "pygdal<2.2.4"
  ```

6. Install database
  ```
  sudo -u postgres createdb -O postgres ocean_portal
  sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" ocean_portal
  sudo vim /etc/postgresql/10/main/pg_hba.conf
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
  cp config.ini.template config.ini
  vim config.ini
  ```

8. Edit config.ini
  - Add the following lines under `[App]`:
    ```
      PROJECT_APP = wcoa
      ?? * [ ] PROJECT_SETTINGS_FILE = True
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
  alias dj="/usr/local/apps/ocean_portal/env/bin/python3 /usr/local/apps/ocean_portal/marco/manage.py"

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
  dj collectstatic
  dj compress
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

 Upgrading to Wagtail 2.0+: https://wagtail.io/blog/upgrading-to-wagtail-2/


Quick start
-----------

1. Create an 'apps' directory (dir), if you do not already have one, in your project's top dir (*e.g.*, ocean_portal/apps/)

2. Clone this repo into the apps dir

3. INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wcoa',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('wcoa/', include('wcoa.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
