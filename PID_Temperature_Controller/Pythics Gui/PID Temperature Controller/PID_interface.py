# Created by Connor McPartland
# University of Pittsburgh 2013


#   This program interacts with an Arduino that is acting as a PID temperature controller.
#   An Arduino object is created in order to send commands and receive data from the Arduino (the temperature controller).
#   Functionality includes:
#       - plotting the recorded temperature over time
#       - changing the PID parameters (P, I, D)
#       - changing the set-temperature of the controller
#       - saving the parameters to the memory of the Arduino for future use
#       - commands sent to temperature controller are sent back to Python side to make sure
#           no command data was lost in transmission
#   User-friendliness:
#       - disconnects the Arduino if the user shuts down the program
#       - warns the user if parameters have been changed but not saved
#       
import math
import serial
import numpy as np
import time
import os
from Arduino import Arduino

class TimeoutException(Exception):
    pass

def initialize(P_knob, I_knob, D_knob, 
                     P_result_box, I_result_box,  D_result_box, 
                     com_choice, save_params_button, set_temp_button, display_params_button,
                     start_data, stop_data, current_temp, auto_collect, messages, plot, **kwargs):
    global params_changed
    params_changed = False
    P_knob.enabled=False
    I_knob.enabled=False
    D_knob.enabled=False
    P_result_box.enabled=False
    I_result_box.enabled=False
    D_result_box.enabled=False
    com_choice.enabled=False
    save_params_button.enabled=False
    display_params_button.enabled=False
    set_temp_button.enabled=False
    start_data.enabled=False
    stop_data.enabled=False
    auto_collect.enabled=False
    current_temp.value=0.00
    
    clear_plot(plot,**kwargs)
    clear_messages(messages, **kwargs)
    
    # Create Data folder if it hasn't already been created.
    global data_directory
    data_directory = os.getcwd() + '\\Data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

def terminate(**kwargs):
    try:
        global arduino
        if arduino.is_connected:
            arduino.disconnect()
            print 'Arduino closed.'
    except NameError:
        pass
     
def clear_plot(plot, **kwargs):
    plot.clear(rescale=True)
    plot.set_plot_properties(
            x_label='t (s)',
            y_label='Temperature ($^\circ$C)',
            x_scale='linear',
            y_scale='linear',
            aspect_ratio='auto')
    plot.new_curve('temperature', memory='growable', length= 100000, animated=False, 
                        line_style='-', line_width=1, line_color='red')
    plot.new_curve('set_temperature', memory='growable', length=100000, animated=False,
                        line_style='-', line_width=.5, line_color='black')

def clear_messages(messages, **kwargs):
    messages.clear()

def activate_com_choice(com_choice, manual_com_choice, **kwargs):
    if manual_com_choice.value:
        com_choice.enabled=True
    else:
        com_choice.enabled=False

# Connect to arduino via serial communication.
def connect_arduino(P_knob, I_knob, D_knob, 
                     P_result_box, I_result_box,  D_result_box, 
                     connected_result, com_choice, connect_button, disconnect_button, set_temp_box, manual_com_choice, 
                     start_data, stop_data, save_params_button, display_params_button, params_box, set_temp_button, auto_collect, current_temp, 
                     plot, messages, **kwargs):
    global parameters
    global arduino
    arduino = Arduino()
    parameters = np.zeros(6)
    found_PID_controller = False
    found_arduino = False
    if manual_com_choice.value:
        arduino = Arduino('COM%s'%com_choice.value, 9600, 1.0)
        if arduino.connect():
            if arduino.ID == 'PID Temperature Controller':
                found_PID_controller = True
                found_arduino = True
                connected_result.value = 'Connected on COM%s'%(com_choice.value)
                messages.write('Successfully connected to Arduino on COM%s. '%com_choice.value)
            else:
                messages.write('Successfully connected to Arduino on %s but ID was not correct.\nID: %s\n' %(com_choice.value, arduino.ID))
                found_arduino = True
                arduino.disconnect()
        else:
            connected_result.value = 'Failed to connect on COM%s' %(com_choice.value)
    else:
        coms = []
        
        for x in map(str, range(1,101)): coms.append('COM'+x)
        for com in coms:
            arduino = Arduino(com, 9600, 1.0)
            if arduino.connect():
                if arduino.ID == 'PID Temperature Controller':
                    found_PID_controller = True
                    found_arduino = True
                    connected_result.value = 'Connected on %s' %(com)
                    messages.write('Successfully connected to Arduino on %s. '%com)
                    print arduino.ID
                else:
                    messages.write('Successfully connected to Arduino on %s but ID was not correct.\nID: %s\n' %(com, arduino.ID))
                    found_arduino = True
                    arduino.disconnect()
                    
            else:
                connected_result.value = 'Failed to connect on %s' %(com)
            if found_PID_controller: break
        if not found_arduino and not found_PID_controller:
            messages.write('Failed to connect to Arduino on COMs 1-100\n')
    if found_arduino:
        if found_PID_controller:
            messages.write('PID Temperature Controller found.\n')
            if arduino.is_connected and arduino.is_ready:
                time.sleep(.2)
                messages.write('Arduino is open for communication.\n')
                P_knob.enabled=True
                I_knob.enabled=True
                D_knob.enabled=True
                P_result_box.enabled=True
                I_result_box.enabled=True
                D_result_box.enabled=True
                connect_button.enabled = False
                disconnect_button.enabled = True
                save_params_button.enabled=False
                display_params_button.enabled=True
                params_box.value=''
                set_temp_button.enabled=True
                start_data.enabled=True
                stop_data.enabled=True
                auto_collect.enabled=True

                initialize_parameters(P_knob, I_knob, D_knob, 
                    P_result_box, I_result_box, 
                    D_result_box, set_temp_box, start_data, stop_data, 
                    current_temp, auto_collect, messages, plot, params_box, **kwargs)
            else:
                messages.write('Arduino connected but not yet ready for serial communication.\n')
        else:
            messages.write('Failed to find PID Temperature Controller, but Arduino boards detected.\n')
    else:
        arduino.disconnect()
        P_knob.enabled=False
        I_knob.enabled=False
        D_knob.enabled=False
        P_result_box.enabled=False
        I_result_box.enabled=False
        D_result_box.enabled=False
        disconnect_button.enabled=False
        connect_button.enabled=True
        set_temp_button.enabled=False
        display_params_button.enabled=False
        start_data.enabled=False
        stop_data.enabled=False
    

# Initialize parametrs. Upon opening the serial connection, arduino is forced to reset, erasing its current parameters. 
# To reset the arduino to its state before opening serial connection, the most recently used parameters have been saved
#    from the last time the arduino was closed. Load previously saved parameters and resend them to arduino.
def initialize_parameters(P_knob, I_knob,  D_knob, 
                            P_result_box, I_result_box, 
                            D_result_box,  set_temp_box, 
                            start_data, stop_data, current_temp, auto_collect, 
                            messages, plot,  params_box, **kwargs):
                            #It_knob,It_result_box, Dt_knob, Dt_result_box):
    global parameters
    parameters = get_params(params_box, messages, **kwargs) #np.loadtxt('parameters.txt',delimiter=',', dtype='float')
    if not parameters == '':
        P_knob.value = float(parameters[0])
        P_result_box.value = float(parameters[0])
        I_knob.value = float(parameters[1])
        I_result_box.value = float(parameters[1])
        D_knob.value = float(parameters[2])
        set_temp_box.value = float(parameters[3])
        
# Change the set-temperature.
def set_temp(set_temp_box, start_data, stop_data, plot, current_temp, auto_collect, save_temp_data, set_temp_button,
                P_knob, I_knob, D_knob, P_result_box, I_result_box, D_result_box, disconnect_button,
                display_params_button, save_params_button, messages, **kwargs):
    global parameters
    global params_changed
    global arduino
    set_temp = float(set_temp_box.value)
    arduino.write('s')
    arduino.write(set_temp)
    time.sleep(.2)
    response = arduino.read().split(',')
    messages.write('Message %s was received by Arduino\n'%response)
    if response[0] == 's' and np.around(float(response[1]),7) == np.around(set_temp,7):
        parameters[3] = set_temp
        messages.write('Set Temeprature set to %f\n' %set_temp)
        params_changed = True
        save_params_button.enabled = True
        if auto_collect.value:
            start_data_collection(start_data, stop_data, P_knob, I_knob, D_knob, P_result_box, I_result_box, D_result_box, 
                            disconnect_button, save_params_button, display_params_button,
                            plot, current_temp, auto_collect, save_temp_data, set_temp_button, set_temp_box, messages, **kwargs)
    else:
        set_temp_box.value = parameters[3]
        messages.write('Parameter not properly changed due to error in serial communication.\n')
        
# If P_knob is used, match the value of P_result_box below the knob to this value.
# If P_result_box is used, match the value of P_knob to this value, then send the value to arduino.
def set_P_box(P_result_box, P_knob, messages, save_params_button, **kwargs):
    P_result_box.value=P_knob.value
    set_P_parameter(P_result_box, P_knob, messages, save_params_button, **kwargs)
def set_P_parameter(P_result_box, P_knob, messages, save_params_button, **kwargs):
    global parameters
    global params_changed  
    global arduino
    
    P = float(P_result_box.value)

    if arduino.is_connected:
        arduino.write('p')
        arduino.write(P)      
        time.sleep(.2)
        response = arduino.read().split(',')
        messages.write('Message %s was received by Arduino\n'%response)
        if response[0] == 'p' and np.around(float(response[1]),7) == np.around(P,7):
            parameters[0] = P
            params_changed = True
            save_params_button.enabled = True
            messages.write('P set to %f\n' %P)
            P_knob.value=P_result_box.value
        else:
            P_result_box.value = float(parameters[0])
            P_knob.value = float(parameters[0])
            messages.write('Parameter not properly changed due to error in serial communication.\n')
        
# Repeat the procedure used for P parameter for the remaining parameters:
def set_I_box(I_result_box, I_knob, messages, save_params_button, **kwargs):
    I_result_box.value=I_knob.value
    set_I_parameter(I_result_box, I_knob, messages, save_params_button, **kwargs)
def set_I_parameter(I_result_box, I_knob, messages, save_params_button, **kwargs):
    global parameters
    global params_changed
    global arduino
    
    I = float(I_result_box.value)
    
    if arduino.is_connected:
        arduino.write('i')
        arduino.write(I)      
        time.sleep(.2)
        response = arduino.read().split(',')
        messages.write('Message %s was received by Arduino\n'%response)
        if response[0] == 'i' and np.around(float(response[1]),7) == np.around(I,7):
            parameters[1] = I
            params_changed = True
            save_params_button.enabled = True
            messages.write('I set to %f\n' %I)
            I_knob.value=I_result_box.value
        else:
            I_result_box.value = float(parameters[1])
            I_knob.value = float(parameters[1])
            print parameters[1]
            messages.write('Parameter not properly changed due to error in serial communication.\n')
        
def set_D_box(D_result_box, D_knob, messages, save_params_button, **kwargs):
    D_result_box.value=D_knob.value
    set_D_parameter(D_result_box, D_knob, messages, save_params_button, **kwargs)
def set_D_parameter(D_result_box, D_knob,  messages, save_params_button, **kwargs):
    global parameters
    global params_changed    
    global arduino
    
    D = float(D_result_box.value)
    
    if arduino.is_connected:
        arduino.write('d')
        arduino.write(D)      
        time.sleep(.2)
        response = arduino.read().split(',')
        messages.write('Message %s was received by Arduino\n'%response)
        if response[0] == 'd' and np.around(float(response[1]),7) == np.around(D,7):
            parameters[3] = D
            params_changed = True
            save_params_button.enabled = True
            messages.write('D set to %f\n' %D)
            D_knob.value=D_result_box.value
        else:
            D_result_box.value = float(parameters[3])
            D_knob.value = float(parameters[3])
            messages.write('Parameter not properly changed due to error in serial communication.\n')

# Begin temperature data collection. 
def start_data_collection(start_data, stop_data, P_knob, I_knob, D_knob, P_result_box, I_result_box, D_result_box, 
                            disconnect_button, save_params_button, display_params_button,
                            plot, current_temp, auto_collect, save_temp_data, set_temp_button, set_temp_box, messages, **kwargs):
    global arduino
    global data_directory
    plot.clear_data('temperature')
    plot.clear_data('set_temperature')
    arduino.write('t')              # ask arduino to send temperature data
    response = arduino.read()
    if response == 't':
        set_temp_button.enabled=False
        start_data.enabled=False
        P_knob.enabled=False
        I_knob.enabled=False
        D_knob.enabled=False
        P_result_box.enabled=False
        I_result_box.enabled=False
        D_result_box.enabled=False
        save_params_button.enabled=False
        display_params_button.enabled=False
        disconnect_button.enabled=False
        if save_temp_data.value:
            try: 
                dirs = data_directory+'\\'+time.strftime("\%d%b%Y_%Hh%Mm", time.localtime())
                os.makedirs(dirs)
                data_file = open(dirs+time.strftime("\Temperature_Data_%d%b%Y_%Hh%Mm.txt", time.localtime()), 'w')
                data_file.write('Time (s) \tTemperature (deg C)\n')
                params_file = open(dirs+time.strftime("\Params_Data_%d%b%Y_%Hh%Mm.txt", time.localtime()), 'w')
                params_file.write('Parameters:\n')
                params_file.write('P:\t%s\n' %P_result_box.value)
                params_file.write('I:\t%s\n' %I_result_box.value)
                params_file.write('D:\t%s\n' %D_result_box.value)
                params_file.write('Set temperature:\t%s deg C\n' %set_temp_box.value)
                params_file.close()
            except:
                message.write('Error creating data file. Data not saved!')
                save_temp_data.value = False
        messages.write('Collecting data...\n')
        while not stop_data.value:
            data = []
            current_time = time.time()
            temp = 0.0
            #Sample data for 0.8 seconds, then plot.
            while time.time() < current_time+0.8:
                response = arduino.read().split(",")
                time_from_arduino = float(response[0])
                temp = float(response[1])
                if save_temp_data.value:
                    data_file.write(str(time_from_arduino) + '\t' + str(temp) + '\n')
                data.append((time_from_arduino, temp))
            current_temp.value = temp
            plot.append_data('set_temperature', np.column_stack((np.linspace(data[0][0], data[-1][0], len(data)), np.ones(len(data))*float(set_temp_box.value))))
            #plot.append_data('set_temperature', np.column_stack((np.linspace(plot.plot_properties['ylimits'][0], plot.plot_properties['ylimits'][1], len(data)), np.ones(len(data))*float(set_temp_box.value))))
            plot.append_data('temperature', np.array(data))
        if save_temp_data.value:
            data_file.close()
        stop_data_collection(start_data, stop_data, set_temp_button, 
                            P_knob, I_knob, D_knob, P_result_box, I_result_box, D_result_box,
                            disconnect_button, save_params_button, display_params_button, messages, **kwargs)
    else:
        messages.write('Temperature collection failed to start due to error in serial communication.\n')
    
def stop_data_collection(start_data, stop_data, set_temp_button, 
                            P_knob, I_knob, D_knob, P_result_box, I_result_box, D_result_box,
                            disconnect_button, save_params_button, display_params_button, messages, **kwargs):
    global arduino
    global params_changed
    arduino.write('h')
    time.sleep(.2)
    
    # It's possible that temperature data sent by the Arduino is stuck on the buffer when command 'h' is sent.
    # Read from Arduino to clear the buffer. Stop when the proper response is heard. If proper response is not heard 
    #   in 3 seconds, assume communication has failed.
    end_time = time.time() + 3
    while time.time() < end_time:
        response = arduino.read()
        if response=='h':
            break
    if response=='h':
        stop_data.value=False
        start_data.enabled=True
        set_temp_button.enabled=True
        P_knob.enabled=True
        I_knob.enabled=True
        D_knob.enabled=True
        P_result_box.enabled=True
        I_result_box.enabled=True
        D_result_box.enabled=True
        disconnect_button.enabled=True
        if params_changed:
            save_params_button.enabled=True
        display_params_button.enabled=True
        messages.write('Data collection stopped.\n')
    else:
        messages.write('Temperature collection failed to stop due to error in serial communication.\n')
        disconnect_button.enabled=True
        
    
# Generic function to send a message to arduino.
#def write_to_arduino(message, error_message):
#    global arduino
#    try:
#        arduino.write(message)
#        arduino.flushInput()
#        print 'Message "',message,'" sent to arduino'
#    except:
#        error_message.open()
#        print 'Failed to send.'
## Generic function to read incoming message from arduino.
#def read_from_arduino(error_message):
#    global arduino
#    arduino.flush()
#    try:
#        response = arduino.readline().strip()
#        return response
#    except:
#        error_message.open()
#        print 'No response found'

# Save the current parameters to a file.
def save_parameters(save_status, messages, save_params_button, **kwargs):
    # This method saves the parameters to a text file.
    #try:
    #    np.savetxt('parameters.txt', parameters, delimiter=',', fmt='%g')
    #    save_status.value=''
    #    save_status.value='Parameters succesfully saved.'
    #    messages.write('Parameters saved to parameters.txt\n')
    #except IOError:
    #    save_status.value='Failed to save parameters!'
    #    messages.write('Error writing to parameters.txt!\n')
    
    # Tell arduino to write current parameters to eeprom
    global params_changed
    global arduino
    arduino.write('w')
    time.sleep(.2)
    response = arduino.read()
    if response == 'w':
        save_status.value='Parameters saved to Arduino.'
        params_changed=False
        save_params_button.enabled=False
        messages.write('Parameters saved to Arduino EEPROM.\n')
    else:
        save_status.value='Error in saving parameters.'
        save_params_button.enabled=True
        messages.write('Parameters not saved due to error in serial communication.\n')
    

# Get the current PID parameters being used by the arduino from the arduino and print them
def get_params(params_box, messages, **kwargs):
    global arduino
    arduino.write('g')
    time.sleep(.2)
    response = arduino.read()
    if response == 'g':
        params = arduino.read()
        try:
            params = params.split(',')
            params_box.value= 'P: %s\tI: %s\tD: %s\tSet Temp: %s' % (tuple(params))

            messages.write("Parameters succesfully loaded from Arduino's EEPROM.\n")
            return params
        except:
            messages.write('Arduino sent invalid data, parameters failed to load\n')
            return ''
    else:
        messages.write('Parameters could not be loaded due to error in serial communication.\n')
        return ''
    
# Close the arduino. Save the current parameters.
def disconnect(P_knob, I_knob,  D_knob,
                     P_result_box, I_result_box,  D_result_box, 
                     connect_button, disconnect_button, connected_result, save_status, save_params_button, display_params_button, params_box,
                     current_temp, start_data, stop_data, set_temp_button, messages, save_params_message, **kwargs):
    global arduino
    global params_changed
    if arduino.is_connected:
        if params_changed:
            if save_params_message.open():
                save_parameters(save_status, messages, save_params_button, **kwargs)
                time.sleep(.5)
                disconnect(P_knob, I_knob, D_knob, 
                            P_result_box, I_result_box,  D_result_box, 
                            connect_button, disconnect_button, connected_result, save_status, save_params_button, display_params_button, params_box,
                            current_temp, start_data, stop_data, set_temp_button, messages, save_params_message, **kwargs)
            else:   
                params_changed=False
                disconnect(P_knob, I_knob,  D_knob, 
                        P_result_box, I_result_box, D_result_box, 
                        connect_button, disconnect_button, connected_result, save_status, save_params_button, display_params_button, params_box,
                        current_temp, start_data, stop_data, set_temp_button, messages, save_params_message, **kwargs)
        else:
            if arduino.disconnect():
                connected_result.value = 'Disconnected'
                messages.write('Arduino disconnected.\n')
                P_knob.enabled=False
                I_knob.enabled=False
                D_knob.enabled=False
                P_result_box.enabled=False
                I_result_box.enabled=False
                D_result_box.enabled=False
                display_params_button.enabled=False
                connected=False
                connect_button.enabled=True
                disconnect_button.enabled=False
                save_params_button.enabled=False
                save_status.value=''
                set_temp_button.enabled=False
                start_data.enabled=False
                stop_data.enabled=False
                params_box.value=''
                current_temp.value=0.0
                time.sleep(1)
            else:
                connected_result.value = 'Failed to disconnect'
                messages.write('Arduino failed to disconnect.\n')