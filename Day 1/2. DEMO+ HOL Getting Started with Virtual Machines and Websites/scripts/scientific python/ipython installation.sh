sudo apt-get update && sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get install -y python-setuptools python-pip
sudo pip install ipython

sudo apt-get install -y python-matplotlib python-tornado python-zmq python-jinja2 python-scipy python-pandas && sudo pip install azure scikit-learn

ipython profile create nbserver
cd ~/.ipython/profile_nbserver/
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
python -c "import IPython;print IPython.lib.passwd()" 
nano ipython_config.py

ipython notebook --profile=nbserver
