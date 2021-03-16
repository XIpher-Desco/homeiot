import serial

"""
winsen mh-z19b用クラス (Co2センサークラス)
Mhz19b.read_concentration_detailを呼び出すだけで、よしなに読み出してくれる
"""


class Mhz19b:
  STARTING_BYTE = 0xff  # 0byteは必ずコレ
  SENSOR_ID = 0x01  # 複数センサー使う時の判別？
  CMD_GAS_CONCENTRATION = 0x86  # co2濃度を読み込むためのコマンド
  CMD_CALIBRATE_ZERO_POINT = 0x87
  CMD_CALIBRATE_SPAN_POINT = 0x88
  CMD_ABC_LOGIC_ON_OFF = 0x79
  ABC_ON = 0xA0
  ABC_OFF = 0x00

  def __init__(self, serial_dev):
    # シリアル通信用の初期設定
    self.ser = serial.Serial(serial_dev, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1.0)

  def __read_concentration(self):
    # responseは9byte全てが帰ってくる。そのままでは使えないため隠蔽。
    packet = [0 for i in range(9)]
    packet[0] = self.STARTING_BYTE
    packet[1] = self.SENSOR_ID
    packet[2] = self.CMD_GAS_CONCENTRATION
    packet[8] = self.checksum(packet)

    self.send_message(packet)
    response = self.read_message()
    print(response)
    return response

  def read_co2(self):
    res = self.__read_concentration()
    co2 = (res[2] << 8) + res[3]
    return co2

  def ABC_logic_ON(self):
    # 自動キャリブレーションをオンに
    packet = [0 for i in range(9)]
    packet[0] = self.STARTING_BYTE
    packet[1] = self.SENSOR_ID
    packet[2] = self.CMD_ABC_LOGIC_ON_OFF
    packet[3] = self.ABC_ON
    packet[8] = self.checksum(packet)

    self.send_message(packet)
    return True

  def ABC_logic_OFF(self):
    # 自動キャリブレーションをオフに
    packet = [0 for i in range(9)]
    packet[0] = self.STARTING_BYTE
    packet[1] = self.SENSOR_ID
    packet[2] = self.CMD_ABC_LOGIC_ON_OFF
    packet[3] = self.ABC_OFF
    packet[8] = self.checksum(packet)

    self.send_message(packet)
    return True

  def zero_calibration(self):
    packet = [0 for i in range(9)]
    packet[0] = self.STARTING_BYTE
    packet[1] = self.SENSOR_ID
    packet[2] = self.CMD_CALIBRATE_ZERO_POINT
    packet[8] = self.checksum(packet)

    self.send_message(packet)
    return True

  def send_message(self, packet):
    # パケットはチェックサム含めた完成したlistを送ること
    command = 0
    for v in packet:
      command = (command << 8) + v
    try:
      self.ser.write(command.to_bytes(9, 'big'))
    except:
      raise Exception('Serial communication if failed')

  def read_message(self):
    # send_messageの直後に使う
    try:
      return self.ser.read(9)
    except:
      raise Exception('Serial communication if failed')

  def checksum(self, packet):
    # 送信用チェックサム生成. packetはchecksum含めた9個(16進数)を含むlist形式
    if 9 == len(packet):
      sum = 0
      for i in range(1, 8):
        sum = (sum + packet[i]) & 0xFF  # 255を超えた場合はオーバーフローなので切り捨て
      sum = 0xFF - sum  # 実際は0xFFとXOR
      sum += 1
      return sum
    else:
      raise ValueError('invalid packet size')
