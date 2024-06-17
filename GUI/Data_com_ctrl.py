class DataMaster():
    def __init__(self):
       self.StartMultimeter="#S#M#C#\n"
       self.StopMultimeter="#S#M#P#\n"
       self.StartOChannel1="#S#O1#C#\n"
       self.StopOChannel1="#S#O1#P#\n"
       self.StartOChannel2="#S#O2#C#\n"
       self.StopOChannel12="#S#O2#P#\n"
       self.StartAWG="#S#A#C#\n"
       self.StopAWG="#S#A#P#\n"
       self.StartVSupply="#S#V#C#\n"
       self.StopVSupply="#S#V#P#\n"
       self.AWG_Data=[]
       self.PS_Data=[]
       self.x_data_CH1=[]
       self.y_data_CH1=[]
       self.Tempo_Ch1=0
       self.Tempo_CH2=0
       self.x_data_CH2=[]
       self.y_data_CH2=[]
       self.Oscil_Max_Points=100
    def Add_Multimeter_Data(self,Mult_Data,GUI):
        self.GUI=GUI
        if(Mult_Data[1]=='V'):
            #print("Tensao:",Mult_Data[2])
            for i in range(len(self.GUI.Multimeter)):
                self.GUI.Multimeter[i].label_tensao.config(text=f'V: {Mult_Data[2]}')
        elif(Mult_Data[1]=='I'):
            #print("Corrente:",Mult_Data[2])
            for i in range(len(self.GUI.Multimeter)):
                self.GUI.Multimeter[i].label_current.config(text=f'I: {Mult_Data[2]}')
        elif(Mult_Data[1]=='C'):
            #print("Capacidade:",Mult_Data[2])
            for i in range(len(self.GUI.Multimeter)):
                self.GUI.Multimeter[i].label_capacitance.config(text=f'C: {Mult_Data[2]}')
        elif(Mult_Data[1]=='R'):
            #print("Resistência:",Mult_Data[2])
            for i in range(len(self.GUI.Multimeter)):
                self.GUI.Multimeter[i].label_resistance.config(text=f'R: {Mult_Data[2]}')
        else:
            pass
            
 
if __name__=="__main__":
    DataMaster()
