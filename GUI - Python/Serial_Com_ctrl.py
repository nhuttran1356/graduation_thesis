import serial
import serial.tools.list_ports  # pip install pyserial



class SerialCtrl():
    def __init__(self):

       
        pass

    def getCOMList(self):
        '''
        Method that get the lost of available coms in the system
        '''
        ports = serial.tools.list_ports.comports()
        self.com_list = [com[0] for com in ports]
        self.com_list.insert(0, "-")

    def SerialOpen(self, ComGUI):
        try:
            self.ser.is_open
        except:
            PORT = ComGUI.clicked_com.get()
            BAUD = ComGUI.clicked_bd.get()
            self.ser = serial.Serial()
            self.ser.baudrate = BAUD
            self.ser.port = PORT
            self.ser.timeout = 0.1

        try:
            if self.ser.is_open:
                print("Already Open")
                self.ser.status = True
            else:
                PORT = ComGUI.clicked_com.get()
                BAUD = ComGUI.clicked_bd.get()
                self.ser = serial.Serial()
                self.ser.baudrate = BAUD
                self.ser.port = PORT
                self.ser.timeout = 0.01
                self.ser.open()
                self.ser.status = True
        except:
            self.ser.status = False

    def SerialClose(self, ComGUI):
        '''
        Method used to close the UART communication
        '''
        try:
            self.ser.is_open
            self.ser.close()
            self.ser.status = False
        except:
            self.ser.status = False

    def write(self, data):

        try:
            if self.ser and self.ser.is_open:
                self.ser.write(data.encode())  # Write data to the serial port
        except Exception as e:
            print(f"Serial write error: {e}")

    def read_line(self):
        try:
            if self.ser and self.ser.is_open:
                return self.ser.readline().decode().strip('\r\n')
        except Exception as e:
            print(f"Serial read error: {e}")
            return None

    # def set_time(self):
    #     serial.Timeout