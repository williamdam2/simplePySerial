import serial

def check_port_status(port_name: str, baudrate: int = 115200):

    if port_name is  None: 
        return 
    if baudrate is None:
        return 

    ## config 
    # baudrate = 115200 
    # port_name = "/dev/tty.SLAB_USBtoUART"

    try:
        # print("port name: ", port_name)
        # print("baudrate: ", baudrate)
        serial_port = serial.Serial(port=port_name, baudrate=baudrate, timeout=5)
        read_data = serial_port.read()
        print("end try")
    except serial.serialutil.SerialException as err:
        print("Enter except")
        ## get the error arguments and print 
        code = err # tuple 
        print("Code: ",code)
        print("return type:",type(code))
        if(code == 16): 
            print(f"port {port_name} is busy, please close and try again.")
            pass 
        elif(code == 2): 
            print(f"port name: {port_name} is not valid.")
            pass
        else:
            print("unknow code")
        
        return (False, code) 

    else:
        print('serial_port = ', serial_port.__dict__)
        print('read_data = ', read_data)
        print("serial port is not busy.")
        serial_port.close()
        return (True, 1) 


if __name__ == "__main__":
    # main() 
    port_name = 'COM3'
    baudrate = 115200 
    check_port_status(port_name=port_name, baudrate=baudrate)
    print("end program")