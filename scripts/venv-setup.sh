!#/bin/bash
sudo apt install python3.10-venv python3-pip
rm -rf ./env
python3.10 -m venv ./env
chmod +x ./env/bin/activate
./env/bin/activate
pip3 install --no-cache-dir -r requirements.txt
