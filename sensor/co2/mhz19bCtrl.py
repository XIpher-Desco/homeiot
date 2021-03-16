from sensor.co2 import mhz19b
import argparse
import subprocess


class Mhz19bCtrl:
  SERIAL_DEV = '/dev/ttyS0'
  SERIAL_START = 'sudo systemctl start serial-getty@ttyS0.service'
  SERIAL_STOP = 'sudo systemctl stop serial-getty@ttyS0.service'

  def __init__(self):
    self.p = subprocess.call(self.SERIAL_STOP, stdout=subprocess.PIPE, shell=True)
    self.sensor = mhz19b.Mhz19b(self.SERIAL_DEV)

  def __del__(self):
    self.p = subprocess.call(self.SERIAL_START, stdout=subprocess.PIPE, shell=True)

  def calibration(self, status):
    if status == 'on':
      return self.sensor.ABC_logic_ON()
    elif status == 'off':
      return self.sensor.ABC_logic_OFF()
    elif status == 'zero':
      return self.sensor.zero_calibration()

  def read_co2(self):
    return self.sensor.read_co2()
