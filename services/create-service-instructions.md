
# How To Create The Service On Raspberry Pi (Or any linux system)
This will start the program automataically when the system is finished booting

## Edit robot.service

* update the path to the program you want to run i.e. single_motor_test.py
* update the working directory i.e. pi-robots/python

## Enabling The Service
* run the following

```bash
sudo cp robot.service /etc/systemd/system/robot.service
sudo systemctl daemon-reload
sudo systemctl enable robot.service
sudo systemctl start robot.service
sudo systemctl status robot.service
```


