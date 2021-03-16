# homeiot

雑に作った mhz19b (mhz14a も同じ) 操作用 python モジュール  
UART 通信想定 tty0s (raspberry pi3, UART0 想定)

## 使い方
```
from sensor.co2 import mhz19bCtrl
co2 = mhz19bCtrl.Mhz19bCtrl()
co2_value = co2.read_co2()
```
