When you checkout this repo move all the files _(apart from the `README.md`)_ to your home directory (i.e. `~`). _Make sure to move `.conkyrc` as well. It is a hidden file so you might miss it_
```
~# sudo apt install conky-all
~# virtualenv .crypto
...
~# source .crypto/bin/activate
~(.crypto)# pip install -r requirements.txt
...
~(.crypto)# deactivate
~# crontab -e
...
# Minute   Hour   Day of Month       Month          Day of Week        Command    
# (0-59)  (0-23)     (1-31)    (1-12 or Jan-Dec)  (0-6 or Sun-Sat)                
   */30      *         *               *                *              python ~/crypto.py
...
~# ls -l
...
~# python crypto.py
~# ls | grep 'crypto_conky.txt'
crypto_conky.txt
...
```
Edit the coins in `crypto.py` to add your own coins

![Alt text](/screenshot.png?raw=true "Preview")