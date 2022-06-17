# Project One - Dogbit

**De inhoud van dit document schrijf je volledig in het Engels**

Omschrijf het project. Doe dit in het markdown formaat.
- [Syntax md](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

Hoe kan een externe persoon (die niets weet over de "ProjectOne" opdracht) het project snel runnen op de eigen pc?
Op github vind je verschillende voorbeelden hoe je een readme.md bestand kan structureren.
- [Voorbeeld 1](https://github.com/othneildrew/Best-README-Template)
- [Voorbeeld 2](https://github.com/tsungtwu/flask-example/blob/master/README.md)
- [Voorbeeld 3](https://github.com/twbs/bootstrap/blob/main/README.md)
- [Voorbeeld 4](https://www.makeareadme.com/)

## Inhoud
We will start out with setting up our pi, this ensures we have a workable environment.

Before we do anything else. Let's use this command to get admin rights so we don't have to type "sudo" every time we want to execute a command
sudo -i
to exit this mode use

exit
Next we will connect to our local WiFi connection. We can use this command to do that.
fill in your SSID (network name) and your password in the correct places

wpa_passphrase 'SSID' 'passphrase' >> /etc/wpa_supplicant/wpa_supplicant.conf
to avoid anyone can just see your SSID we will clear our history there are two ways to do it,

the first way, !this will clear your ENTIRE history:
            history -c
the second way, slightly slower but is more precise:
first we want to view our history

  history
this will return a list of commands you executed, they all have an index.

  history -d index
You can also find the passphrase in the wpa_supplicant fil and, it should be commented.

nano /etc/wpa_supplicant/wpa-supplicant.conf
use ctrl+X, Y, enter to save and quit the file

to check if we are connected to the internet we will use the following command

wget www.google.com


## instructables
https://www.instructables.com/member/BennoDi/instructables/
