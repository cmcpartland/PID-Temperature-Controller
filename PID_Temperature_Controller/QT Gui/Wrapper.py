# Import the visa library
try:
    import visa
    VISA_MOD_AVAILABLE = True
except:
    VISA_MOD_AVAILABLE = False

# System library is imported
import sys

import numpy as np

# Import the PyQt4 modules for all the commands that control the GUI.
# Note: Importing as from "Module" import * implies that everything from that module is not part of this module.
# And one does not have to put the module name before its commands. (Example: import numpy as np --> np.sin(x)   where as: from numpy import * --> sin(x))
from PyQt4.QtCore import * 
from PyQt4.QtGui import *

# This imports the GUI created earlier using Qt Designer
# This is how to import from a sub directory in python.
# To do this though, one must create a __init__.py file in sub folder. It does not have to have anything in it, but just has to have that name.
# It is how python know that this is a sub directory to import from. Just create a new text file and save it to this folder than rename it to __init__.py
# The syntax to import from a sub folder is as follows: SUB_FOLDER_NAME.MODULE_NAME
from GUI_Sub_Folder.GUI import Ui_MainWindow


# The class that controls all the operations of the GUI. This is the main class that contains all the functions that control the GUI.
class MyForm(QMainWindow):
    
    # The __init__ function is what is everything the user wants to be initialized when the class is called.
    # Here we shall define the trig functions to corresponding variables.
    # Note that the "self" variable means that the function is part of the class and can be called inside and outside the class.(Although __init__ is special.)
    def __init__(self, parent = None):
        
        # standard GUI code
        QWidget.__init__(self, parent)
        
        # That class that contains all the GUI data and widget names and commands is defined to "self.ui"
        # Thus to do anything on the GUI the commands must go through this variable.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Defines labels and a title to the plot.
        self.ui.temperature_plot.axes.set_title("Temperature (C)")
        self.ui.temperature_plot.axes.set_xlabel("t (s)")
        self.ui.temperature_plot.axes.set_ylabel("C")
        
        # Disable buttons/boxes initially. 
        self.disable_parameters()
        
        self.connected = False 
        self.params_saved = True
        
        
        self.connect(self.ui.connect_disconnect_button, SIGNAL("clicked()"), self.connect_disconnect_arduino)
        #self.connect(self.ui.start_collection, SIGNAL("clicked()"), self.start_data_collection)
        #self.connect(self.ui.stop_collection, SIGNAL("clicked()"), self.stop_data_collection)
        self.connect(self.ui.start_stop_button, SIGNAL("clicked()"), self.start_stop_collection)
        self.connect(self.ui.P_box, SIGNAL("valueChanged()"), self.set_P_parameter)
        self.connect(self.ui.I_box, SIGNAL("valueChanged()"), self.set_I_parameter)
        self.connect(self.ui.It_box, SIGNAL("valueChanged()"), self.set_It_parameter)
        self.connect(self.ui.D_box, SIGNAL("valueChanged()"), self.set_D_parameter)
        self.connect(self.ui.Dt_box, SIGNAL("valueChanged()"), self.set_Dt_parameter)
        self.connect(self.ui.set_temp_button, SIGNAL("clicked()"), self.set_temp)
        
        self.search_for_coms()
        
    def search_for_coms(self):
                # Pulls all active visa ports
        # The try.except clause is in case there are no visa port on the computer. Without it, an error is returned
        try:
            # Collects a list of all the visa ports on the computer
            visas = visa.get_instruments_list()
        except:
            # If there are no visas connected to the computer, get_instruments_list returns an error
            # When that occurs, the variable, "visas", the list is defined to is instead defined to an empty string which shows nothing in the combo box
            visas = ''
        # Removes any previous data in the combo box
        self.ui.com_box.clear()
            
        if visas == '':
            self.ui.connected_result.setText('No devices found!')
            self.ui.connect_disconnect_button.setEnabled(False)
        else:
            self.ui.com_box.setEnabled(True)
            self.ui.connect_disconnect_button.setEnabled(True)
            for each_visa in visas:
                self.ui.com_box.addItem(each_visa)
    
    def enable_parameters(self):
        #self.ui.start_collection.setEnabled(True)
        #self.ui.stop_collection.setEnabled(True)
        self.ui.set_temp_box.setEnabled(True)
        self.ui.P_box.setEnabled(True)
        self.ui.I_box.setEnabled(True)
        self.ui.It_box.setEnabled(True)
        self.ui.D_box.setEnabled(True)
        self.ui.Dt_box.setEnabled(True)
        self.ui.com_box.setEnabled(True)
        
    def disable_parameters(self):
        #self.ui.start_collection.setDisabled(True)
        #self.ui.stop_collection.setDisabled(True)
        #self.ui.connect_disconnect_button.setDisabled(True)
        self.ui.start_stop_button.setDisabled(True)
        #self.ui.disconnect_button.setDisabled(True)
        self.ui.save_params_button.setDisabled(True)
        self.ui.set_temp_box.setDisabled(True)
        self.ui.set_temp_button.setDisabled(True)
        self.ui.P_box.setDisabled(True)
        self.ui.I_box.setDisabled(True)
        self.ui.It_box.setDisabled(True)
        self.ui.D_box.setDisabled(True)
        self.ui.Dt_box.setDisabled(True)
        self.ui.com_box.setDisabled(True)

    # Connect to arduino via serial communication.
    def connect_disconnect_arduino(self):
        if not self.connected:
            self.parameters = np.zeros(6)
            visa_chosen = str(self.ui.com_box.currentText())
            try:
                self.arduino = visa.instrument(visa_chosen)
                self.connected=True
                self.ui.connected_result.setText('Connected on %s' % visa_chosen)
            except:
                self.connected=False
                self.ui.connected_result.setText('Failed to connect on %s' % visa_chosen)
            if self.connected:
                self.collecting = False
                self.enable_parameters()
                self.initialize_parameters()
                self.ui.connect_disconnect_button.setText('Disconnect')
        elif self.connected:
            try:
                self.arduino.close()
                self.disable_parameters()
                self.ui.connected_result.setText('Diconnected')
                self.connected = False
                self.ui.connect_disconnect_button.setText('Connect')
            except:
                self.ui.connected_result.setText('Failed to disconnect!')
            
    #def disconnect_arduino(self):
    #    if self.connected:
    #        try:
    #            self.arduino.close()
    #            self.disable_parameters()
    #            self.ui.connected_result.setText('Diconnected')
    #        except:
    #            self.ui.connected_result.setText('Failed to disconnect!')
                
    def initialize_parameters(self):
        self.parameters = self.get_params()
        
        self.ui.save_params_button.setDisabled(True)
   
        self.ui.P_box.setValue(self.parameters[0])
        self.ui.I_box.setValue(self.parameters[1])
        self.ui.It_box.setValue(self.parameters[2])
        self.ui.D_box.setValue(self.parameters[3])
        self.ui.Dt_box.setValue(self.parameters[4])
        self.ui.set_temp_box.setValue(self.parameters[5])
        #self.set_P_parameter()
        #self.set_I_parameter()
        #self.set_It_parameter()
        #self.set_D_parameter()
        #self.set_Dt_parameter()
        #self.set_temp()
        self.params_saved = True
        
        
    def get_params(self):
        params = self.arduino.ask('g')
        params = params.split(',')
        #params_box.value= 'P: %s\tI: %s\tIt: %s\tD: %s\tDt: %s\tSet Temp: %s' % (tuple(params))
        return params
        
    def set_P_parameter(self):
        if connected:
            self.arduino.write('p')
            self.arduino.write(self.ui.P_box.value())
            self.parameters[0] = self.ui.P_box.value()
            self.ui.save_params_button.setEnabled(True)
            self.params_saved = False
            
    def set_I_parameter(self):
        if connected:
            self.arduino.write('i')
            self.arduino.write(self.ui.I_box.value())
            self.parameters[1] = self.ui.I_box.value()
            self.ui.save_params_button.setEnabled(True) 
            self.params_saved = False
    
    def set_It_parameter(self):
        if connected:
            self.arduino.write('j')
            self.arduino.write(self.ui.It_box.value())
            self.parameters[2] = self.ui.It_box.value()
            self.ui.save_params_button.setEnabled(True) 
            self.params_saved = False
    
    def set_D_parameter(self):
        if connected:
            self.arduino.write('d')
            self.arduino.write(self.ui.D_box.value())
            self.parameters[3] = self.ui.D_box.value()
            self.ui.save_params_button.setEnabled(True) 
            self.params_saved = False
    
    def set_Dt_parameter(self):
        if connected:
            self.arduino.write('e')
            self.arduino.write(self.ui.Dt_box.value())
            self.parameters[4] = self.ui.Dt_box.value()
            self.ui.save_params_button.setEnabled(True) 
            self.params_saved = False
    
    def set_temp(self):
        if connected:
            self.arduino.write('s')
            self.arduino.write(self.ui.set_temp_box.value())
            self.parameters[5] = self.ui.set_temp_box.value()
            self.ui.save_params_button.setEnabled(True) 
            self.params_saved = False
        
    ## Begin temperature data collection. 
    #def start_data_collection(self):
    #    self.reset_plot()
    #    self.arduino.write('t')               # ask arduino to send temperature data
    #    #time.sleep(.5)
    #    self.disable_parameters()
    #    self.ui.stop_collection.setEnabled(True)
    #    #while not stop_data.value:
    #    data = self.arduino.read()      # read data sent from arduino and plot it
    #    data = data.split(',')
    #    #try:
    #    #    t = float(data[0])/1000.0   # convert from milliseconds to seconds
    #    #    temp = float(data[1])
    #    #    #plot.append_data('temperature', (t, temp))
    #    #    self.ui.current_temp_box.setText(str(temp))
    #    #except:
    #    #    print 'no data sent'
    
    #def stop_data_collection(self):
    #    self.arduino.write('h')
    #    self.enable_parameters()
    #    #time.sleep(.1)
    
    def start_stop_collection(self):
        if not self.collecting: #, then start collecting data
            self.reset_plot()
            self.arduino.write('t')               # ask arduino to send temperature data
            self.ui.start_stop_button.setText('Stop Temperature Collection')
            #time.sleep(.5)
            self.disable_parameters()
            self.ui.stop_collection.setEnabled(True)
            #while not stop_data.value:
            data = self.arduino.read()      # read data sent from arduino and plot it
            data = data.split(',')
            #try:
            #    t = float(data[0])/1000.0   # convert from milliseconds to seconds
            #    temp = float(data[1])
            #    #plot.append_data('temperature', (t, temp))
            #    self.ui.current_temp_box.setText(str(temp))
            #except:
            #    print 'no data sent'
        if self.collecting:
            self.arduino.write('h')
            self.enable_parameters()
            self.ui.start_stop_button.setText('Start Data Collection')
        
        
        
    # Resets the plot to its default state. The only problem is that the "self.ui.mplwidgetPlot" has to defined to a new variable, "self.axes" is used
    # The only way to rid the plot of a colorbar is through "figure.clear" and that removes the entire figure. Thus a new plot has to be created.
    def reset_plot(self):
        
        self.ui.temperature_plot.figure.clear()
        
        # Creates the new plot and is defined to self.axes. (Note: If one does not need to clear the plot, if colorbars are never used, this does not have to be done
        # All one needs to do to create a plot is "self.ui.mplwidgetPlot.axes" used equivalently to "self.axes" above and a new subplot does not have to be defined, as
        # done below.)
        self.axes = self.ui.temperature_plot.figure.add_subplot(111)

    # Following function runs whenever the user presses the "x" button to close the window
    # It is intended to prevent an unwanted quit by asking the user to exit again.
    def closeEvent(self, event):
    
        if not self.params_saved:
            quit_msg = 'Parameters have not been saved! Are you sure you want to exit the program?'
        elif self.connected:
            quit_msg = 'Arduino has not been disconnected! Are you sure you want to exit the program?'
        else:
            quit_msg = "Are you sure you want to exit the program?"
        
        # Creates a message box that displays the quit_msg and has two pushButtons
        reply = QMessageBox.question(self, 'Message', 
                                            quit_msg, QMessageBox.Yes, QMessageBox.No)
        # Yes means the user wants to quit. Thus the window is closed.
        if reply == QMessageBox.Yes:
            event.accept()
        
        # No means the event is ignored and the window stays open.
        else:
            event.ignore()
            
# The if statement below checks to see if this module is the main module and not being imported by another module
# If it is the main module if runs the following which starts the GUI
# This is here in case it is being imported, then it will not immediately start the GUI upon being imported
if __name__ == "__main__":
    # Opens the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()
    
    # Shows the GUI
    myapp.show()
    
    # Exits the GUI when the x button is clicked
    sys.exit(app.exec_())
