from tkinter import messagebox
import serial.tools.list_ports
import serial
import time
import string
import numpy as np
from scipy import signal
class SerialCtrl():
    def __init__(self):
        self.port=None 
        self.ser=None
        self.OscilloscopeThreadFlag=False
        self.MultimeterThreadFlag=False 
        self.PSThreadFlag=False
        self.SGThreadFlag=False
        self.Receive_Thread=False
        self.Oscilloscope_Data_Flag=False
        self.Multimeter_Data_Flag=False
        #self.msg=None
        self.Oscilloscope1_Data_Flag=False
        self.Oscilloscope2_Data_Flag=False
        self.last_value = None
        self.last_falling_edge_time = None
        self.frequency = None
        self.MAX_POINTS = 100
    def SerialOpen(self,gui):
        self.GUI=gui
        def find_serial_port():
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if "STMicroelectronics STLink Virtual COM Port" in p.description:
                    return p.device
            return None
        
        self.port=find_serial_port()
        if self.port:
            self.ser = serial.Serial(self.port, baudrate=115200)
            if self.ser.is_open:
                self.ser.status=True
                messagebox.showinfo("Connection successful !","STM device connected to the PC")
                gui.CDbutton.config(text="Disconnect STM")
                gui.Canvas.coords(gui.CDbutton_window,340,360)
        else:
            messagebox.showwarning("Connection Error", "No STM device founded")

    def SerialClose(self):
        self.ser.close()
        print("Comunicação terminada")
   
    def SerialOscilloscopeData(self,GUI):
        self.OscilloscopeThreadFlag=True
        self.GUI=GUI
        while(self.OscilloscopeThreadFlag==True):
            try:
                if(self.ser.is_open):
                    try:
                            for i in range(self.MAX_POINTS):
                                data = float(self.ser.readline().decode().strip())
                                raw = (data / 4095 * 3.3) - 1.65
                                self.calculate_frequency(raw)
                                for i in range(len(self.GUI.Oscilloscope)):
                                    self.GUI.Oscilloscope[i].data_array.append(raw)  
                                    if len(self.GUI.Oscilloscope[i].data_array) > self.MAX_POINTS:
                                        self.GUI.Oscilloscope[i].data_array.pop(0)  
                                if(self.ser.in_waiting>100):
                                    self.ser.reset_input_buffer()
                            for i in range(len(self.GUI.Oscilloscope)):
                                self.GUI.Oscilloscope[i].draw_array()  
                            
                    except Exception as e:
                        print(e)
            except Exception:
                print(e)       

    def SerialMultimeterData(self,GUI):
            self.MultimeterThreadFlag=True
            self.GUI=GUI
            while(self.MultimeterThreadFlag==True):
                try:
                   
                        if(self.Multimeter_Data_Flag==True):
                            self.GUI.data.Add_Multimeter_Data(self.msg,self.GUI)
                            self.Multimeter_Data_Flag=False
                        else:
                            print("No new data for Multimeter")
                            time.sleep(1)
                            
                except Exception as e:
                     print(e)

    def SerialPowerSupplyData(self,GUI):
        self.PSThreadFlag=True
        self.GUI=GUI
        self.PS_Voltage=0.0
        self.PS_Current=0.0
        self.input_flag=0   
         
        while(self.PSThreadFlag==True):
            try:
                    if(self.PSThreadFlag==False):
                        break 
                    for i in range(len(self.GUI.PowerSupply)):
                        if(self.GUI.PowerSupply[i].voltage_flag==1     or   self.GUI.PowerSupply[i].current_flag==1):
                            self.input_flag=1
                            self.indice_flag=i
                    
                    if(self.input_flag==1): 
                        
                        self.GUI.PowerSupply[self.indice_flag].voltage_flag=0
                        self.GUI.PowerSupply[self.indice_flag].current_flag=0 
                        self.PS_Voltage=self.GUI.PowerSupply[self.indice_flag].Voltage.get()
                        self.PS_Current=self.GUI.PowerSupply[self.indice_flag].Current.get()
                        for i in range(len(self.GUI.PowerSupply)):
                            self.GUI.PowerSupply[i].Voltage.set( self.PS_Voltage)
                            self.GUI.PowerSupply[i].Current.set(self.PS_Current)
                            self.GUI.PowerSupply[i].Current_last_input=self.PS_Current
                            self.GUI.PowerSupply[i].Voltage_last_input=self.PS_Voltage
                        self.GUI.data.PS_Data=f"#D#PS#{self.PS_Voltage}#{self.PS_Current}\n"
                        print(self.GUI.data.PS_Data)
                        try:
                            self.ser.write(self.GUI.data.PS_Data.encode())
                            
                        except Exception as e:
                            print(e)
                            pass

                        self.input_flag=0
                    else:
                        print("User's input has not change")
                        time.sleep(1)
                    if(self.PSThreadFlag==False):
                        break   
            except Exception as e:
                print(e)   
            
    def SerialSignalGeneratorData(self,GUI):
            self.SGThreadFlag=True            
            self.GUI=GUI
            self.SG_Voltage=0.0
            self.SG_Frequency=0.0
            self.SG_Forma=None
            self.input_flag=0   
            
            while(self.SGThreadFlag==True):
                try:
                    
                        if(self.SGThreadFlag==False):
                            break 
                        for i in range(len(self.GUI.SignalGenerator)):
                            if(self.GUI.SignalGenerator[i].Frequencia_flag==1     or   self.GUI.SignalGenerator[i].Volts_flag==1 or self.GUI.SignalGenerator[i].Combo_flag==1):
                                self.input_flag=1
                                self.indice_flag=i
                        if(self.input_flag==1):    
                            self.GUI.SignalGenerator[self.indice_flag].Frequencia_flag=0
                            self.GUI.SignalGenerator[self.indice_flag].Volts_flag=0 
                            self.GUI.SignalGenerator[self.indice_flag].Combo_flag=0 
                            self.SG_Voltage=self.GUI.SignalGenerator[self.indice_flag].Volts.get()
                            self.SG_Frequency=self.GUI.SignalGenerator[self.indice_flag].Frequencia.get()
                            self.SG_Forma=self.GUI.SignalGenerator[self.indice_flag].Forma.get()
                            for i in range(len(self.GUI.SignalGenerator)):
                                self.GUI.SignalGenerator[i].Volts.set( self.SG_Voltage)
                                self.GUI.SignalGenerator[i].Frequencia.set(self.SG_Frequency)
                                self.GUI.SignalGenerator[i].Forma.set(self.SG_Forma)
                                self.GUI.SignalGenerator[i].Volts_last_input=self.SG_Voltage
                                self.GUI.SignalGenerator[i].Frequencia_last_input=self.SG_Frequency
                                self.GUI.SignalGenerator[i].Combo_last_input=self.SG_Forma  
                            if(self.SG_Voltage!=0 and self.SG_Frequency!=0 ):
                                num_waves = 1
                                self.Total_Time = num_waves * (1 / self.SG_Frequency)
                                self.T_SG = np.linspace(0, self.Total_Time, 256)
                                if(self.SG_Forma=="Sine"):
                                    self.Waveform = self.SG_Voltage * np.sin(2 * np.pi * self.SG_Frequency * self.T_SG )
                                elif(self.SG_Forma=="Square"):
                                    self.Waveform = self.SG_Voltage * signal.square(2 * np.pi * self.SG_Frequency * self.T_SG )
                                else:
                                    self.Waveform = self.SG_Voltage * signal.sawtooth(2 * np.pi * self.SG_Frequency * self.T_SG )

                                
                                Max=max( self.Waveform)
                                Min=min(self.Waveform)
                                scaling_factor = 3300 / (Max - Min)
                                Scaled_Values=  (self.Waveform - Min) *scaling_factor
                                rounded_values=np.round(Scaled_Values)
                                self.SG_Voltage_Array= rounded_values.astype(int)
                                
                                for i in range(len(self.SG_Voltage_Array)):
                                    if (i==0):
                                        self.GUI.data.AWG_Data.append(f'"#A#{self.SG_Voltage_Array[i]}#' )
                                    elif(i!=len(self.SG_Voltage_Array)-1):
                                        self.GUI.data.AWG_Data.append(f'{self.SG_Voltage_Array[i]}#' )
                                    else:
                                        self.GUI.data.AWG_Data.append(f'{self.SG_Voltage_Array[i]}\n' )  
                                #print(self.GUI.data.AWG_Data)  
                                combined_string = ''
                                for element in self.GUI.data.AWG_Data:
                                    combined_string += element
                                #print(combined_string)
                                #print(len(combined_string))
                                try:
                                    self.ser.write(combined_string.encode())  
                                  
                                except Exception as e:
                                    print(e)

                                self.input_flag=0
                                self.GUI.data.AWG_Data=[]
                            else:
                                self.GUI.data.AWG_Data=f"#A#SG#0#0#{self.SG_Forma}\n"
                                try:
                                    self.ser.write(self.GUI.data.AWG_Data.encode())  
                                except Exception as e:
                                    print(e)
                                self.input_flag=0
                                self.GUI.data.AWG_Data=[]
                        else:
                            print("User's input has not change")
                            time.sleep(1)
                        if(self.SGThreadFlag==False):
                            break  
                except Exception as e:
                    print(e)
  #  def Serial_Receive(self):
   #     self.Receive_Thread=True

    #    while(self.Receive_Thread==True):
     #       try:
      #          RawData=self.ser.readline()
       ##        #if(len(temp)> 0):
                 #   if "#" in temp:
                  #      self.msg=temp.split("#")
                   #     del self.msg[0]
                    #    del self.msg[len(self.msg)-1]
                     #   if(self.msg[0]=='M'):
                      #      self.Multimeter_Data_Flag=True
                       # elif(self.msg[0]=='O1'):
                        #    self.Oscilloscope1_Data_Flag=True
                        #elif(self.msg[0]=='O2'):
                         #   self.Oscilloscope2_Data_Flag=True
                        #else:
                         #   print("Nada")
          #  except Exception as e:
           #     print(e)

# Função para calcular a frequência do sinal
    def calculate_frequency(self,current_value):
        try:
            if self.last_value is None:
                self.last_value = current_value
                return
            
            if self.last_value > 0 and current_value <= 0:
                self.current_time = time.time()
                if self.last_falling_edge_time is not None:
                    self.period = self.current_time - self.last_falling_edge_time
                    self.frequency = 1 / self.period * 347000*2
                self.last_falling_edge_time = self.current_time
             
            self.last_value =current_value
        except Exception as e:
            print(e)
if __name__=="__main__":
     SerialCtrl()
