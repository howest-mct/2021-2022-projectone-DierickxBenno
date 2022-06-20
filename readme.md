# ***Project One - DogBit***

# **Inhoud**

# Getting things ready for Project One 🎉 🎊

- ### Getting things ready for Project One 🎉 🎊

  - ### Installation

    - ### Downloading the image ⏳
    - ### Restoring the image ⏳
    - ### Linking the RasPi
    - ### Preparing raspi for further use

  - ### Configuration

    - ### ⚠ Do it yourself: Provide WiFi access on the RasPi for home use:
    - ### Already done: Full update/upgrade on 5 May 2022, if you want to upgrade, please
    - ### follow the list below:
    - ### Already done: Installing Apache
    - ### Already done: MariaDB

      - ### Already done: Installing MariaDB
      - ### Already done: Securing MariaDB
      - ### Already done: Create MariaDB User

    - ### ⚠ Do it yourself: Configure MySQLWorkbench
    - ### ⚠ Do it yourself: Configure Visual Studio :
    - ### ⚠ do it yourself: GitHub repo cloning:
    - ### Already done: Python ready:
    - ### Already done: Database import:
    - ### Already done: Chromium kiosk:
    - ### ⚠ do it yourself: run app.py:
    - ### ⚠ do it yourself: display front end in Apache.
    - ### ⚠ Do it yourself: When your project is finished, start automatically.

- ### Good luck!
- ### Demo project

# Installation

> During this installation you will download, install and configure the image for ProjectOne. After
> this, you will configure a preinstalled project so that you have a fully functioning front-end and
> backend at the end.

## Downloading the image ⏳

- Download [project_one.img.zip](https://studenthowest-my.sharepoint.com/:u:/g/personal/pieter-jan_beeckman2_howest_be/EZJTscmkyydAj-VcWTAYtjsBiidK5Grxy54ltO-FoOeE2w?e=xf2jKi)
  to your local computer.

## Restoring the image ⏳

- ### ⚠ Unzip the file ⚠
- ### Place the file on an SD card of at least 8GB with Win32 Imager or Balena Etcher.
- ### After the image is written, you can remove the SD card and insert it into your RasPi.

## Connecting RasPi

- ### Boot your RasPi.
- ### Connect the RasPi to your computer with a network cable and make an SSH connection in Putty. to 192.168.169 for the user student with password W8w00rd.

> ATTENTION: The image has been created in AZERTY (as opposed to Sensors & Interfacing!)
> Should you have trouble logging in, try in qwerty Z! zààrd.

## Preparing raspi for further use

- ### After logging in, tap sudo raspi-config.
- ### In the menu choose (6) Advanced > (1) Expand Filesystem
- ### ⚠ REBOOT de Raspi

> ⚠ ATTENTION: All buses are still deactivated. Do not forget to activate them via raspi- config

# Configuration

## ⚠ Do it yourself: Provide WiFi access on the RasPi for home use:

- sudo -i to get administrator rights

- `wpa_passphrase <your_SSID@Home> <your_wifi password> >> /etc/wpa_supplicant/wpa_supplicant.conf`
  Replace <your_SSID@Home> with the name of your home network and <your_wifi password>
  with the corresponding password.
- wpa_cli -i wlan0 reconfigure to reload your wireless network card in the RasPi.
- wget [http://www.google.com](http://www.google.com) to see if the wireless internet works.

## Already done: Full update/upgrade on 5 May 2022, if you want to upgrade, please follow the list below:

- apt update to check which updates are available.
  (you still have sudo rights from the previous step, so no need to set sudo)
- apt upgrade to install the available updates.
- Y if you are asked if you are sure.
- Waiting, waiting, waiting, ...

## Already done: Install Apache

- apt install apache2 -y to install Apache, the web server. This package takes over for Full Stack
  Web Developlent / ProjectOne from the Live Server in Visual Studio Code.
- As we are working with Github in this exercise we will make it easy for ourselves by
  put all the material in one folder, both front-end and back-end, as we are used to doing in the
  Full Stack Web Development lessons. For this we will have to change Apache's default folder,
  along with the folder and file permissions, but we will only do this once we have created our
  folder structure.

## Already done: MariaDB

### **Already done: Installing MariaDB**

- apt install mariadb-server mariadb-client -y to install MariaDB, the fork of MySQL

### **Already done: Securing MariaDB**

- mysql_secure_installation to better secure the MariaDB
- First you are asked to enter the current root password for MariaDB. Since there is none yet, you
  can just press Enter here.
- Then you can change the password. Choose a password that you can remember! By default, the
  password chosen here is W8w00rd
- The next step is to delete anonymous users. Choose y here
- Prohibit root from logging in remotely. Choose y here.
- Then remove test database and access? Choose y.
- Finally, reload privilege databases: y

### **Already done: Create MariaDB User**

- Next, we configure the user student with password W8w00rd on the MariaDB server.
- mysql -u root -p to access the MariaDB server^
- grant all on `*.*` to `'student'@'localhost'` identified by `'W8w00rd'`; grant grant option on
  `*.*` to `'student'@'localhost'`; Creates a new user _student_ with password _W8w00rd_ who gets rights to all databases.
- `flush privileges` Reloads privileges
- `exit` exits from the MariaDB server

## ⚠ Do it yourself: Configure MySQLWorkbench

- ### Start MySQLWorkBench on your laptop
- ### Create a new connection.
  - ### Under Connection Method, select Standard TCP/IP over SSH.
  - ### SSH Hostname: 192.168.168.
  - ### SSH Username: student
  - ### SSH Password: W8w00rd
  - ### Save this if possible.
  - ### MySQL Hostname: 127.0.0.
  - ### MySQL Server Port: 3306
  - ### Username: student
  - ### Password: W8w00rd Save this if possible.

## ⚠ Do it yourself: Configure Visual Studio:

- Open Visual Studio
- Install the extension Remote-SSH
- Press F1 and tap SSH. Select the option Remote-SSH: Add New SSH Host
- Tap ssh student@192.168.168.169 - A
- Choose a way to save the file.
- Press F1 and tap SSH. Select the option Remote-SSH: Connect To Host
- Choose the option 192.168.
- A new window will open and the password for the RasPi will be requested.
- Type W8w00rd
- After this Visual Studio Codede connection will open and install a number of things on the RasPi.
  > Be patient. It takes a little longer the first time.

## ⚠ do it yourself: GitHub repo cloning:

- Press the Source Control logo on the left and choose Clone Repository.
- Go to the GitHub Classroom [https://classroom.github.com/a/F6MHgLx-] in a browser and
  accept the invitation. Refresh the page and go to the repo you created. Click the Code
  button and copy the git link.
- Paste the copied link into Visual Studio Code and press enter.
- Place the repo in the /home/student/ folder.
- Visual Studio Code will then ask to open this repo, click Yes
- Then open the file Code/Backend/app.py and give Visual Studio Code some time to load all the
  necessary things.

## Already done: Python ready:

- Before we can run the app.py we need to install some packages for python.
- We are NOT using venv here on the RasPi. Open a Terminal and type the following code:
  - pip install flask-cors
  - pip install flask-socketio
  - pip install mysql-connector-python
  - pip install gevent
  - pip install gevent-websocket
- There **_might_** be an easier way to do this with python

## Already done: Database import:

- Import the database into MariaDB via MySQLWorkbench.

## Already done: Chromium kiosk:

- We can make chrome start up by itself, but to do this we need to install a few pieces of software:

  - `pip install selenium`
  - `sudo apt install chromium-chromedriver`

- With selenium we can control the chrome browser (clicks, tab changes, text input), ...

## ⚠ do it yourself: run app.py:

- Try to run app.py. If you can't press Play (the green triangle) in the window, look in the extensions
  under the Python extension and click install on 192.168.168.169 and wait. Reload if asked.
- If all went well, the backend should now be running.

## ⚠ do it yourself: display front end in Apache.

- Surf on your PC to http://192.168.168.169.

- Normally, you should now see the Apache2 Debian Default Page , which is the default Apache
  page currently located in the /var/www/html/ folder on the RasPi. We will not use this default
  folder, but will use the front-end folder from the repo you just cloned.

- If you are no longer sudo: sudo -i

- `nano /etc/apache2/sites-available/000-default.conf`

- Use down arrow to go to the line where it now says _DocumentRoot /var/www/html_
  or _DocumentRoot /home/student/<name_of_your_repo>/front-end_ and change it to _DocumentRoot
  /home/student/<name_of_your_repo>/front-end_
- Save by doing _Ctrl + x_ , followed by Y and _Enter_
- Then we restart Apache by doing `service apache2 restart`
- Now we have to set the permissions on the root folder correctly.

  - Open nano /etc/apache2/apache2.conf and use the down arrow to look for the following
    lines:

    > ```
    >  <Directory />
    >  Options FollowSymLinks
    >  AllowOverride All
    >  Require all denied
    >  </Directory>.
    > ```

    and change it to:

    > ```
    > <Directory />
    > Options Indexes FollowSymLinks Includes ExecCGI
    > AllowOverride All
    > Require all granted
    > </Directory>.
    > ```

  - Save by doing _trl + x_ , followed by Y and _Enter_

  - Then restart Apache by doing service `apache2 restart`

  - Check if apache is started correctly: `service apache2 status`.
    You should get approximately the following output:

  > Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset:
  > enabled)
  > Active: active (running) since ...

## ⚠ Do it yourself: When your project is finished, start automatically.

- Create a file called myproject.service
- Place the following code in the file:

  ```
  [Unit]
  Description=ProjectOne Project
  After=network.target
  [Service]
  ExecStart=/usr/bin/python3 -u /home/student/<name_of_your_repo>/backend/app.py

  WorkingDirectory=/home/student/<name_of_your_repo>/backend
  StandardOutput=inherit
  StandardError=inherit
  Restart=always
  User=student
  [Install].
  WantedBy=multi-user.target
  ```

- Copy this file as root user to `/etc/systemd/system` with the command `sudo cp myproject.service/etc/systemd/system/myproject.service`
- Now you can test the file by starting it: sudo systemctl start myproject.service
- Stopping the file can be done by entering the command: sudo systemctl stop myproject.service
- If everything works well you can have the script start automatically after booting: `sudo systemctl enable myproject.service`
- The logs / console output can be seen via `journalctl -u myproject.service`

## Good luck!

> If everything works out, don't forget to take a selfie and submit it to the appropriate assignment!

# Demo project

The image shows an example project where we link a button and LED in real time to the website
and database

- First follow the steps in Installation and Configuration
- Connect a button to pin 20 (use safety resistor)
- Also connect a LED to pin 21 (don't forget its resistor)
- Start via terminal backend:
  > ```
  > cd ~/projectone-demo/backend/
  > python app.py
  > ```
- We will skip apache for a while and will also use python to serve the front-end. In a second
  terminal:
  > ```
  > cd ~/projectone-demo/front-end/
  > python -m http.server
  > ```
- Now you can go to http://192.168.168.169:8000

- The idea now is to get this code into your own repo
- So make sure that your own repo is cloned in `/home/student/<name_of_your_repo>`.

- We will copy the files to our repo:

  > `cp -r ~/projectone-demo/* /home/student/<name_of_your_repo>/`

      - So in my case this is `cp -r ~/projectone-demo/* /home/student/2021-2022-projectone-fgmnts/`

- When you have done this, make sure that apache is configured to display the front-end. The
backend code can be executed manually during development, but for production make sure
the code is started automatically via the service

- Make sure you commit and push your new code, this is the command for the kickoff on 20/

# **Instructables**

https://www.instructables.com/Dog-Health-Tracking-Device-the-DogBit/
