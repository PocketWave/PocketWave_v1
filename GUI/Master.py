from GUI_Master import RootGUI
from Serial_Com_Ctrl import SerialCtrl
from Data_com_ctrl import DataMaster


MyData=DataMaster()
MySerial=SerialCtrl()
RootMaster=RootGUI(MySerial,MyData)

RootMaster.root.mainloop()
