import time
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import serial

class RootGUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("Serial communication")
        self.root.geometry("1700x700")
        self.root.config(bg="white")


# Class to setup and create the communication manager with MCU
class ComGui():
    def __init__(self, root, serial):
        # Initializing the Widgets
        self.root = root
        self.serial = serial
        self.frame = LabelFrame(root, text="Com Manager",
                                padx=5, pady=5, bg="white")
        self.label_com = Label(
            self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w")
        self.label_bd = Label(
            self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w")

         #control
        self.frame_control = LabelFrame(root, text="Control",
                                        padx=5, pady=5, bg="white")
        # temperature
        self.label_temperature = Label(
            self.frame_control, text="Temperature: ", bg="white", width=15, anchor="w")

        self.temper = StringVar()
        self.entry_pid_temp = Entry(self.frame_control, bg="white", width=20, textvariable=self.temper)

        # water level
        self.label_water = Label(
            self.frame_control, text="Water level: ", bg="white", width=15, anchor="w")

        self.water = StringVar()
        self.entry_pid_water = Entry(self.frame_control, bg="white", width=20, textvariable=self.water)

        # Submit
        self.button_summit = Button(
            self.frame_control, text="Submit", bg="grey", width=7, anchor="center", command=self.form_submit)

        self.button_jog_left = Button(self.frame_control, text= "Jog left", bg="white", width=10, anchor="center", command=self.jog_left)
        self.button_jog_right = Button(self.frame_control, text="Jog right", bg="white", width=10, anchor="center", command=self.jog_right)

        self.button_onUltra = Button(self.frame_control, text="On Ultrasound", bg="white", width=10, anchor="center", command=self.onUltra)
        self.button_offUltra = Button(self.frame_control, text="Off Ultrasound", bg="white", width=10, anchor="center", command=self.offUltra)

        self.button_runCyl = Button(self.frame_control, text="Run ", bg="white", width=10, anchor="center", command=self.runCyl)

        # Pump
        # self.button_pump = Button(self.frame_control, text="Pump", bg="pink", width=7, anchor="center", command=self.pump_feature)

        # Tạo một figure và subplot để vẽ đồ thị water
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_xlabel('Time (s)')
        self.subplot.set_ylabel('Water level(cm) 1')
        self.subplot.set_title('Real-time water level 1')

        # Tạo một canvas để hiển thị đồ thị Matplotlib trong giao diện Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)

        # Tạo một figure và subplot để vẽ đồ thị water
        self.figure3 = plt.Figure(figsize=(5, 4), dpi=100)
        self.subplot3 = self.figure3.add_subplot(111)
        self.subplot3.set_xlabel('Time (s)')
        self.subplot3.set_ylabel('Water level(cm) 2')
        self.subplot3.set_title('Real-time water level 2')

        # Tạo một canvas để hiển thị đồ thị Matplotlib trong giao diện Tkinter
        self.canvas3 = FigureCanvasTkAgg(self.figure3, master=root)

        # Tạo một figure và subplot để vẽ đồ thị temperature
        self.figure2 = plt.Figure(figsize=(5, 4), dpi=100)
        self.subplot2 = self.figure2.add_subplot(111)
        self.subplot2.set_xlabel('Time (s)')
        self.subplot2.set_ylabel('Temperature')
        self.subplot2.set_title('Real-time Temperature')

        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=root)

        # # Bắt đầu một luồng riêng biệt để nhận dữ liệu realtime từ UART
        self.start_time = time.time()
        # Image logo

        self.img = Image.open("img.png")  # Đặt đường dẫn đến hình ảnh của bạn ở đây
        self.img = self.img.resize((100, 125), Image.LANCZOS)  # Điều chỉnh kích thước ảnh nếu cần

        # Chuyển đổi ảnh PIL sang định dạng mà tkinter có thể hiểu được
        self.img_tk = ImageTk.PhotoImage(self.img)

        # Tạo label để hiển thị ảnh
        self.img_label = Label(self.root, image=self.img_tk, bg="white")

        # Water present
        self.label_water1 = Label(self.frame_control, text="Water level 1:", bg="white", width=15, anchor="w")
        self.display_water1 = Label(self.frame_control, text="", bg="white", width=20, anchor="w")

        self.label_water2 = Label(self.frame_control, text="Water level 2:", bg="white", width=15, anchor="w")
        self.display_water2 = Label(self.frame_control, text="", bg="white", width=20, anchor="w")

        self.label_temp = Label(self.frame_control, text="Temperature: ", bg="white", width=15, anchor="w")
        self.display_temp = Label(self.frame_control, text="", bg="white", width=20, anchor="w")


        # Setup the Drop option menu
        self.baudOptionMenu()
        self.ComOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_refresh = Button(self.frame, text="Refresh",
                                  width=10,  command=self.com_refresh)
        self.btn_connect = Button(self.frame, text="Connect",
                                  width=10, state="disabled",  command=self.serial_connect)

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()

    def publish(self):
        # self.frame.grid(row=0, column=0, rowspan=3,
        #                 columnspan=3, padx=5, pady=5)
        self.frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.label_com.grid(column=1, row=2)
        self.label_bd.grid(column=1, row=3)

        # Control
        self.frame_control.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.label_temperature.grid(row=2, column=0, padx=(10, 5))
        self.entry_pid_temp.grid(row=2, column=1, padx=(0, 10))

        self.label_water.grid(row=3, column=0, padx=(10, 5))
        self.entry_pid_water.grid(row=3, column=1, padx=(0, 10))

        self.button_summit.grid(column=1, row=4)

        # Jog
        self.button_jog_left.grid(column=0, row=6)
        self.button_jog_right.grid(column=1, row=6)
        self.button_runCyl.grid(column=2, row=6)
        self.button_onUltra.grid(column=3, row=6)
        self.button_offUltra.grid(column=3, row=7)
        #pump
        # self.button_pump.grid(column=2, row=6)

        # Do thi
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, rowspan=4, pady=10)
        self.canvas2.get_tk_widget().grid(row=2, column=4, columnspan=2, rowspan=4, pady=10)
        self.canvas3.get_tk_widget().grid(row=2, column=2, columnspan=2, rowspan=4, pady=10)

        self.drop_baud.grid(column=2, row=3, padx=self.padx, pady=self.pady)
        self.drop_com.grid(column=2, row=2, padx=self.padx)

        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3)

        # logo
        self.img_label.grid(row=0, column=1, padx=5, pady=5, sticky="ne")

    #     water present
        self.label_water1.grid(row=8, column=0, padx=(10, 5))
        self.display_water1.grid(row=8, column=1, padx=(0, 10))
        self.label_water2.grid(row=9, column=0, padx=(10, 5))
        self.display_water2.grid(row=9, column=1, padx=(0, 10))

        self.label_temp.grid(row=10, column=0, padx=(10, 5))
        self.display_temp.grid(row=10, column=1, padx=(0, 10))

    def ComOptionMenu(self):
        # Generate the list of available coms

        self.serial.getCOMList()

        self.clicked_com = StringVar()
        self.clicked_com.set(self.serial.com_list[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *self.serial.com_list, command=self.connect_ctrl)

        self.drop_com.config(width=10)

    def baudOptionMenu(self):
        self.clicked_bd = StringVar()
        bds = ["-",
               "300",
               "600",
               "1200",
               "2400",
               "4800",
               "9600",
               "14400",
               "19200",
               "28800",
               "38400",
               "56000",
               "57600",
               "115200",
               "128000",
               "256000"]
        self.clicked_bd .set(bds[0])
        self.drop_baud = OptionMenu(
            self.frame, self.clicked_bd, *bds, command=self.connect_ctrl)
        self.drop_baud.config(width=10)

    def connect_ctrl(self, widget):
        print("Connect ctrl")
        # Checking the logic consistency to keep the connection btn
        if "-" in self.clicked_bd.get() or "-" in self.clicked_com.get():
            self.btn_connect["state"] = "disabled"
        else:
            self.btn_connect["state"] = "active"


    def get_sensor_values_and_plot(self):

        data = self.serial.read_line()
        # -10
        current_time = int(time.time() - self.start_time - 6)
        if data and "," in data:
            sensor_data = data.split(",")  # Tách dữ liệu thành 2 giá trị
            print(sensor_data)
            print(current_time)
            if len(sensor_data) == 3:
                try:
                    value_sensor1 = int(sensor_data[0])
                    value_sensor2 = int(sensor_data[1])
                    # value_sensor3 = int(sensor_data[2])
                    value_sensor3 = float(sensor_data[2])
                    # self.data_sensor1.append(( value_sensor1))
                    # self.data_sensor2.append((value_sensor2))
                    self.display_water1.config(text=str(value_sensor1))
                    self.display_water2.config(text=str(value_sensor2))
                    self.display_temp.config(text=str(value_sensor3))

                    # Gọi các phương thức để vẽ dữ liệu lên đồ thị trong Tkinter
                    self.draw_water_level_plot_1(current_time, value_sensor1)
                    self.draw_water_level_plot_2(current_time, value_sensor2)
                    self.draw_temperature_plot(current_time, value_sensor3)

                except ValueError as e:
                    print(f"Error converting sensor data: {e}")

            # Lập lịch để gọi lại hàm sau 100ms
        self.root.after(1000, self.get_sensor_values_and_plot)


    def com_refresh(self):
        print("Refresh")
        # Get the Widget destroyed
        self.drop_com.destroy()

        # Refresh the list of available Coms
        self.ComOptionMenu()

        # Publish the this new droplet
        self.drop_com.grid(column=2, row=2, padx=self.padx)

        # Just in case to secure the connect logic
        logic = []
        self.connect_ctrl(logic)

    def serial_connect(self):
        if self.btn_connect["text"] in "Connect":
            # Start the serial communication
            self.serial.SerialOpen(self)

            # If connection established move on
            if self.serial.ser.status:
                # Update the COM manager
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disable"
                self.drop_baud["state"] = "disable"
                self.drop_com["state"] = "disable"
                #
                # self.get_sensor_values_and_plot()
                #
                InfoMsg = f"Successful UART connection using {self.clicked_com.get()}"
                messagebox.showinfo("showinfo", InfoMsg)

            else:
                ErrorMsg = f"Failure to estabish UART connection using {self.clicked_com.get()} "
                messagebox.showerror("showerror", ErrorMsg)
        else:

            # Closing the Serial COM
            # Close the serial communication
            self.serial.SerialClose(self)

            InfoMsg = f"UART connection using {self.clicked_com.get()} is now closed"
            messagebox.showwarning("showinfo", InfoMsg)
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_baud["state"] = "active"
            self.drop_com["state"] = "active"

    # Check valid temperature
    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def form_submit(self):
        temperature_value = self.temper.get()
        water_value = self.water.get()
        if self.is_float(temperature_value) and self.is_float(water_value):
            temperature_float = float(temperature_value)
            print("Temperature: ", temperature_float)

            water_float = float(water_value)
            print("Water level: ", water_float)
            temperature_float = float(temperature_value)
            water_float = float(water_value)

            # Tạo dữ liệu để gửi đi
            data_to_send = f"C,{temperature_float},{water_float}\r"
            print(data_to_send)
            # Gửi dữ liệu đến đối tượng SerialCtrl
            self.serial.write(data_to_send)
            self.get_sensor_values_and_plot()

            # self.serial.write(str(temperature_float).encode() + b'\n')  # Gửi dữ liệu nhiệt độ
            #
            # # Bắt đầu nhận dữ liệu và vẽ đồ thị
            # self.receive_data_flag = True
            # receive_thread = threading.Thread(target=self.receive_data)
            # receive_thread.start()
        else:
            messagebox.showerror("Error", "Temperature or Water Level must be number")

    def jog_left(self):
        # print("Test Temp On")
        # self.serial.write("A\r")
        return

    def jog_right(self):
        # print("Test Temp Off")
        # self.serial.write("B\r")
        # self.serial.write("M\r")
        return

    def pump_feature(self):
        return

    def onUltra(self):
        print("On Ultra")
        self.serial.write("A\r")
        return
    def offUltra(self):
        print("Off")
        self.serial.write("B\r")
        # self.serial.write("M\r")

    def runCyl(self):
        print("Run servo")
        self.serial.write("N\r")

    def draw_water_level_plot_1(self, x_data, y_data):
        if not hasattr(self, 'data_sensor1'):
            self.data_sensor1 = {'x': [], 'y': []}
        self.data_sensor1['x'].append(x_data)
        self.data_sensor1['y'].append(y_data)
        self.subplot.clear()
        self.subplot.plot(self.data_sensor1['x'], self.data_sensor1['y'])
        self.subplot.set_xlabel('Time (s)')
        self.subplot.set_ylabel('Water level (cm) 1')
        self.subplot.set_title('Real-time water level 1')
        self.canvas.draw()

    def draw_water_level_plot_2(self, x_data, y_data):
        if not hasattr(self, 'data_sensor2'):
            self.data_sensor2 = {'x': [], 'y': []}
        self.data_sensor2['x'].append(x_data)
        self.data_sensor2['y'].append(y_data)
        self.subplot3.clear()
        self.subplot3.plot(self.data_sensor2['x'], self.data_sensor2['y'])
        self.subplot3.set_xlabel('Time (s)')
        self.subplot3.set_ylabel('Water level (cm) 2')
        self.subplot3.set_title('Real-time water level 2')
        self.canvas3.draw()

    def draw_temperature_plot(self, x_data, y_data):
        if not hasattr(self, 'data_sensor3'):
            self.data_sensor3 = {'x': [], 'y': []}
        self.data_sensor3['x'].append(x_data)
        self.data_sensor3['y'].append(y_data)
        self.subplot2.clear()
        self.subplot2.plot(self.data_sensor3['x'], self.data_sensor3['y'])
        self.subplot2.set_xlabel('Time (s)')
        self.subplot2.set_ylabel('Temperature (C)')
        self.subplot2.set_title('Real-time Temperature')
        self.canvas2.draw()
    # def draw_temperature_plot(self, x_data, y_data):
    #     if not hasattr(self, 'data_sensor3'):
    #         self.data_sensor3 = {'x': [], 'y': []}
    #
    #     self.data_sensor3['x'].append(x_data)
    #     self.data_sensor3['y'].append(y_data)
    #
    #     self.subplot2.clear()
    #     self.subplot2.plot(self.data_sensor3['x'], self.data_sensor3['y'])
    #     self.subplot2.set_xlabel('Time (s)')
    #     self.subplot2.set_ylabel('Temperature (C)')
    #     self.subplot2.set_title('Real-time Temperature')
    #
    #     # Điều chỉnh giới hạn trục x và y để thu nhỏ đồ thị
    #     # Ví dụ: Hiển thị dữ liệu trong khoảng thời gian 0 đến 100 giây và nhiệt độ từ 0 đến 50 độ C
    #     self.subplot2.set_xlim(0, 100)  # Điều chỉnh giới hạn trục x tại đây
    #     self.subplot2.set_ylim(0, 50)  # Điều chỉnh giới hạn trục y tại đây
    #
    #     self.canvas2.draw()


if __name__ == "__main__":
    RootGUI()
    ComGui()