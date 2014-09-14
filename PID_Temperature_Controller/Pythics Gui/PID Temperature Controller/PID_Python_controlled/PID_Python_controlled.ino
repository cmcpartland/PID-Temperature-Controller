#include <EEPROM.h>
#include <EEPROMAnything.h>

struct parameters {  // a structure containing all the PID parameters
    float P;         
    float I;
    float D;
    float set_temp;  // the set-temperature of the PID
}
params;

double Pterm = 0;
double Iterm = 0;
double Dterm = 0;
int controlPin = 2;        // sends PWM signal towards the TEC
int tempPin = A2;          // measures the thermistor's voltage
int totalPin = A4;         // measures the total jvoltage input 
int highPin = 22;          // powers the TH10K

double error;               // the difference between the set temp and the real temp
double error_sum = 0;           // the accumulated error 
double last_error = 0;      // the previous error
double delta_error;         // the change in error over one time step of the temperature collection
unsigned long last_time;           // the previous time stamp
double delta_time;          // the time step of the temperature collection
double PID_output = 0;

double temp = 0;            // the real temperature measured from thermistor
double last_temp = 0;       // the previous temperature measured from thermistor
double delta_temp;          // the change in temperature over one time step of the temperature collection
double v_therm,v25;         //  v_therm is voltage drop across the TH10K, v25vt is voltage drop adross R25, so voltage going into TH10k is v25-vt
double log_ratio_Rt_R25;    // log of the ratio between the current resistance of TH10K and resistance of TH10K at 298.15K(which is 10KOhm according to the instruction)
float a = 3.354e-3;        // parameters for obtaining temperature from TH10K datasheet
float b = 2.562e-4; 
float c = 2.14e-6; 
float d = -7.241e-8;                   
boolean ready = false;
boolean python_wants_data = false;
String ID = "PID Temperature Controller";

void setup() {
  Serial.begin(9600);
  pinMode(highPin,OUTPUT);
  EEPROM_readAnything(0, params); //read stored parameters from the EEPROM and store them in params
}

void loop() { 
  // confirm (one time only) that Serial is ready to send/receive data
  if (Serial && ready==false) { 
      Serial.println("Serial ready");
      ready=true;
  }
  else if (!Serial) {
    Serial.println("Serial not ready");
    ready=false;
  }
  
  // check for incoming commands from PID Controller
  if (Serial && Serial.available() > 0) {
      char response = Serial.read();
      // 'response' is which parameter you wish to change
      switch (response) {
        case 'p':  
          // change P      
          params.P = Serial.parseFloat();
          // send the command character and the parameter value back to Python side for confirmation
          Serial.print(response);Serial.print(",");Serial.println(params.P,5);
          break;
        case 'i':
          // change I
          params.I = Serial.parseFloat();
          Serial.print(response);Serial.print(",");Serial.println(params.I,5);
          break;
        case 'd':
          // change D
          params.D = Serial.parseFloat();
          Serial.print(response);Serial.print(",");Serial.println(params.D,5);
          break;
        case 's':
          // change set-temperature
          params.set_temp = Serial.parseFloat();
          Serial.print(response);Serial.print(",");Serial.println(params.set_temp,5);
          break;
        case 't': //'t'emperature wanted
          python_wants_data = true;
          Serial.println(response);
          break;
        case 'h': //'h'alt data sending
          python_wants_data = false;
          Serial.println(response);
          break;
        case 'g': //'g'ive current parameters to python
          Serial.println(response);
          Serial.print(params.P,5); Serial.print(","); 
          Serial.print(params.I,5); Serial.print(",");
          Serial.print(params.D,5); Serial.print(",");
          Serial.println(params.set_temp,5);
          break;
        case 'w': // 'w'rite params to eeprom, i.e. the params are good and will be used by the arduino until they are changed by the user.
          EEPROM_writeAnything(0, params);
          Serial.println(response);
          break;
        case 'r': // 'r'eveal Arduino ID:
          Serial.println(ID);
          break;
        Serial.flush();
      }
  }
  else if (!Serial) {
    Serial.println("Nothing sent/Serial not ready");
  }
  unsigned long time_now = millis();
  digitalWrite(highPin,HIGH);
  v25 = analogRead(totalPin);   //------------------ the voltage going into the TH10K, in binary range from 0 to 1023.
  v_therm = analogRead(tempPin);   //----------------- the voltage across the TH10K.
  // Rt,R25: the resistance of TH10K at temp T and resistance of TH10K at 25 degC (10kohm)
  // Given by formula R_therm/R25 = V/Vin,  R_therm = R25*vt/(v25-vt) --> R_therm/R25 = v_therm/(v25-v_therm)
  log_ratio_Rt_R25 = log(v_therm/(v25-v_therm));
  // formula for temperature, from TH10K datasheet
  temp = double(1.0/(a + b*log_ratio_Rt_R25 + c*(log_ratio_Rt_R25*log_ratio_Rt_R25)+d*(log_ratio_Rt_R25*log_ratio_Rt_R25*log_ratio_Rt_R25)) - 273.0); 
  if (python_wants_data) {
      Serial.print(time_now/1000.0); Serial.print(",");Serial.println(temp);
  }
  error = params.set_temp - temp;
  //No need to worry about rollover, it is taken care of by using unsigned variables.
  delta_time = (double)(time_now - last_time);
  delta_temp = temp - last_temp;
  Pterm = params.P*error;
  if (PID_output > 81 && PID_output < 219) 
    Iterm += params.I*error*delta_time;
  if (delta_time == 0.0)
    Dterm = 0.0;
  else
    Dterm = params.D*delta_temp/delta_time;
// FOR DEBUGGING
//  Serial.print("error");Serial.println(error);
//  Serial.print("Pterm");Serial.println(Pterm);
//  Serial.print("Iterm");Serial.println(Iterm);
//  Serial.print("Dterm");Serial.println(Dterm);
//  Serial.print("delta_error");Serial.println(delta_error);
  
  //The value written to the PWM pin (which is the signal that will later drive the TEC) is forced to take on a value between 80 and 220 
  //in order for the output to be symmetric. 
//  PID_output = constrain(previous_output + params.P*(error - last_error) + (params.I*params.It)*(error) + (params.D/params.Dt)*(lastlast_error - 2*last_error + error), 80, 220); // typical PID statement
  //PWM: 150 is the 'midpoint' of the output, so assuming temperature is perfectly stable, then Pterm, Iterm, and Dterm equal 0 and output should be 150
  PID_output = constrain(Pterm + Iterm - Dterm + 150, 80, 220); 
//  Serial.print("PID output");Serial.println(PID_output);
  last_error = error;   //--------------------------------- update error and time
  last_time = time_now;
  last_temp = temp;
  analogWrite(controlPin, int(PID_output)); //-------------------- drive the TEC with this PWM signal 

  delay(100);  //--------------------------------------------------- (in milliseconds)
}


