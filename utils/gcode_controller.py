import serial
import time
import serial.tools.list_ports
import threading

class GcodeController:

    port = None
    connection = None
    is_connected = False
    baud = 115200
    gcode_file = None
    extruder_running = True  # Flag to control extruder state
    extruder_velocity = 100  # Default extruder velocity

    def available_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def set_selected_port(self, port):
        self.port = port

    def set_selected_baud(self, baud):
        self.baud = baud

    def print_console_out(self, message):
        current_time = time.localtime()
        formatted_date = time.strftime("[%m/%d/%Y]", current_time)
        print(f"{formatted_date}: {message}")

    def start_connection(self):
        if not self.connection or not self.connection.is_open:
            try:
                self.connection = serial.Serial(
                    self.port, self.baud,     
                    bytesize=serial.SEVENBITS,
                    parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=5.0
                )
                self.print_console_out(f'{self.connection.read()}')
                self.is_connected = True
            except IOError:
                self.print_console_out("port was already open")

        self.connection.write("\r\n\r\n")  # wake up the communication
        self.connection.flushInput()

    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.is_connected = False
            self.connection.close()

    def remove_comment(self, string):
        if string.find(';') == -1:
            return string
        else:
            return string[:string.index(';')]

    def read_gcode(self, file):
        try:
            self.start_connection()
            for line in file:
                l = self.remove_comment(line)
                l = l.strip()  # Strip all EOL characters for streaming
                if not l.isspace() and len(l) > 0:
                    self.print_console_out(f'Sending: {l}')
                    self.connection.write(f'{l}\n'.encode())  # Send g-code block
                    # Wait for response with carriage return
                    serial_out = self.connection.readline()
                    self.print_console_out(f':{serial_out.strip()}')
            file.close()
        except Exception as e:
            self.print_console_out(f"An error occurred in gcode stream: {e}")

    def send_gcode_command(self, command):
        self.start_connection()
        self.connection.write(command.encode())
        serial_out = self.connection.readline()
        self.print_console_out(f':{serial_out.strip()}')

    def set_extruder_velocity(self, velocity):
        self.extruder_velocity = velocity

    def start_extruder(self):
        self.extruder_running = True
        threading.Thread(target=self._run_extruder).start()

    def pause_extruder(self):
        self.extruder_running = False

    def _run_extruder(self):
        while self.extruder_running:
            self.send_gcode_command(f'M83\nG1 E100 F{self.extruder_velocity}\n') 
            time.sleep(1) 

