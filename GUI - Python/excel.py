import serial
import pandas as pd
from datetime import datetime
from time import sleep

# Khởi tạo kết nối serial với Arduino
arduino_port = 'COM7'  # Thay 'COMX' bằng cổng serial của Arduino
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
sleep(2)  # Đợi kết nối ổn định

# Khởi tạo DataFrame để lưu trữ dữ liệu
data = {'Time': [], 'Temperature': []}
df = pd.DataFrame(data)

# Hàm để ghi dữ liệu vào Excel
def update_excel(dataframe):
    excel_filename = 'temperature_data.xlsx'
    dataframe.to_excel(excel_filename, index=False)

try:
    while True:
        # Đọc dữ liệu từ cổng serial
        if ser.in_waiting > 0:
            data_read = ser.readline().decode().strip()
            temperature = float(data_read.split()[1])  # Lấy giá trị nhiệt độ từ dữ liệu

            # Thêm giá trị nhiệt độ và thời gian vào DataFrame
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Thêm dữ liệu mới vào danh sách
            # Thêm dữ liệu mới vào DataFrame bằng concat
            new_data = pd.DataFrame([{'Time': current_time, 'Temperature': temperature}])
            df = pd.concat([df, new_data], ignore_index=True)

            # df = df.append({'Time': current_time, 'Temperature': temperature}, ignore_index=True)
            print(f"Temperature: {temperature} °C | Time: {current_time}")

            # Ghi dữ liệu vào Excel
            update_excel(df)

except KeyboardInterrupt:
    ser.close()  # Đóng kết nối khi nhấn Ctrl+C
