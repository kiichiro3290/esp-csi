import sys
import argparse
import serial
import datetime

def read_serial(ser_port, dest, baudrate):
    ser = serial.Serial(port=ser_port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1)

    if ser.isOpen():
        print('open success')
    else:
        print('open failed')
        return
    
    with open(f'{dest}.txt', 'w') as f:
        while True:
            try:
                line = str(ser.readline().decode('utf-8'))
            except UnicodeDecodeError:
                continue

            index = line.find('CSI_DATA')
            if index == -1:
                continue

            # ファイルに書き込む
            l = line.rstrip() + str(datetime.datetime.now().strftime("%Y_%m%d_%H%M%S") + "\n")
            f.write(l)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="シリアルポート経由でデータを取得してローカルに保存する")

    parser.add_argument("ser_port", help="シリアルポート")
    parser.add_argument("dest", help="保存先ファイル")
    parser.add_argument("-b", "--baudrate", help="ボードレート")

    args = parser.parse_args()
    ser_port = args.ser_port
    dest = args.dest
    if args.baudrate:
        baudrate = args.baudrate
    else:
        baudrate = 921600

    read_serial(ser_port=ser_port, dest=dest, baudrate=baudrate)