#include <EEPROM.h>
#include <EEPROMAnything.h>

struct parameters {  // a structure containing all the PID parameters
    float P;         
    float I;
    float It;
    float D;
    float Dt;
    float set_temp;  // the set-temperature of the PID 
}
params;

int controlPin = 2;        // sends PWM signal towards the TEC
int tempPin = A2;          // measures the thermistor's voltage
int totalPin = A4;         // measures the total voltage input 
int highPin = 22;          // powers the TH10K

float error;               // the difference between the set temp and the real temp
float last_error = 0;      // the previous error
float lastlast_error = 0;  // the error before the previous error
float output = 0;

float temp = 25.0;         // the real temperature measured from thermistor
float v_therm,v25;           //  v_therm is voltage drop across the TH10K, v25vt is voltage drop adross R25, so voltage going into TH10k is v25-vt
float log_ratio_Rt_R25;    // log of the ratio between the current resistance of TH10K and resistance of TH10K at 298.15K(which is 10KOhm according to the instruction)
float a,b,c,d;             // datasheet parameters for obtaining temperature from TH10K      
boolean ready = false;
boolean python_wants_data = false;
float start_time = millis();

void setup() {
  Serial.begin(9600);
  pinMode(highPin,OUTPUT);
  Serial.println("Setup run");
  EEPROM_readAnything(0, params); //read stored parameters from the EEPROM and store them in params
}

void loop() { 
  // confirm (one time only) that Serial is ready to send/receive data
  if (Serial && ready==false) { 
      Serial.println('r');
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
          break;
        case 'i':
          // chagne I
          params.I = Serial.parseFloat();
          break;
        case 'd':
          // change D
          params.D = Serial.parseFloat();
          break;
        case 'j':
          // change It
          params.It = Serial.parseFloat();
          break;
        case 'e':
          // change Dt
          params.Dt = Serial.parseFloat();
          break;
        case 's':
          // change set-temperature
          params.set_temp = Serial.parseFloat();
          break;
        case 't': //'t'emperature wanted
          python_wants_data = true;
          start_time = millis();
          break;
        case 'h': //'h'alt data sending
          python_wants_data = false;
          break;
        case 'g': //'g'ive current parameters to python
          Serial.print(params.P); Serial.print(","); 
          Serial.print(params.I*params.It); Serial.print(",");
          Serial.print(params.It); Serial.print(",");
          Serial.print(params.D/params.Dt); Serial.print(",");
          Serial.print(params.Dt); Serial.print(",");
          Serial.println(params.set_temp);
          break;
        case 'w': // 'w'rite params to eeprom, i.e. the params are good and will be used by the arduino until they are changed by the user.
          EEPROM_writeAnything(0, params);
          break;
        Serial.flush();
      }
  }
  else if (!Serial) {
    Serial.println("Nothing sent/Serial not ready");
  }
  
  // set necessary constants
  a = 3.354e-3; b = 2.562e-4; c = 2.14e-6; d = -7.241e-8; //------ parameters given from TH10K datasheet
  digitalWrite(highPin,HIGH);
  v25 = analogRead(totalPin);   //------------------ the voltage going into the TH10K, in binary range from 0 to 1023.
  v_therm = analogRead(tempPin);   //----------------- the voltage across the TH10K.
  // Rt,R25: the resistance of TH10K at temp T and resistance of TH10K at 25 degC (10kohm)
  // Given by formula R_therm/R25 = V/Vin,  R_therm = R25*vt/(v25-vt) --> R_therm/R25 = v_therm/(v25-v_therm)
  log_ratio_Rt_R25 = log(v_therm/(v25-v_therm));
  // formula for temperature, from TH10K datasheet
  temp = 1/(a + b*log_ratio_Rt_R25 + c*(log_ratio_Rt_R25*log_ratio_Rt_R25)+d*(log_ratio_Rt_R25*log_ratio_Rt_R25*log_ratio_Rt_R25)) - 273; 
  if (python_wants_data) {
     Serial.println(temp);
  }
  error = temp - params.set_temp;
  
  float PID_output = output + params.P*(error - last_error) + (params.I*params.It)*(error) + (params.D/params.Dt)*(lastlast_error - 2*last_error + error); // typical PID statement
  output = constrain(PID_output, -255, 255); //-------------- protect against large new_output values. This might not be very useful! 
                                                   //         The range chosen will be an important factor. It should be there, but the limits should not be arbitrary. 
  lastlast_error = last_error;  //--------------------------------- update errors
  last_error = error;      
  float TEC_voltage = mapf(output, -255, 255,150, 220);   //-------- map the output from (-255 to 255) to appropriate range of PWM output, (60,220). 
                                                          //-------- the range (60,220) is used because the output TEC_voltage will be symmetric within this range,
                                                          //          i.e., TEC_voltage(pwm=(220-60)/2+60) = 0.0 V
                                                          //          This will later be converted to +/- 4 V to drive the TEC.
  analogWrite(controlPin, int(TEC_voltage)); //-------------------- drive the TEC with this PWM signal 
  
  delay(10);  //--------------------------------------------------- (in milliseconds)
}

// A mapping function similar to the Arduino map function, but returns a float instead of an int.
float mapf(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
