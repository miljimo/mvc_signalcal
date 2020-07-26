from calculator import Calculator,EventHandler , ValueChangedEvent;
import threading
from calcview import CalculatorView;
import time;


class View(object):

    def __init__(self):
        self.__value = 0;
        self.ValueChanged = EventHandler();

    def SetValue(self, value):
        if(self.__value != value):
            self.__value  =  value;
            self.ValueChanged(ValueChangedEvent(self, self.__value))
            
    @property
    def Value(self):
        return self.__value;

    def Show(self):
        print("Showing");
        
class Controller(object):

    def __init__(self , view, model):
        self.__Calc  = model;
        self.__View  = view;
        self.__View.ValueChanged += self.__OnViewValueChanged;
        self.__Calc.ValueChanged += self.__OnValueChanged;
        self.__Calc.ValueChanged += self.__OnFileWriter;
        self.__recordValues  = list();
        self.__View.Clicked+=   self.__OnReplay
        self.__IsPlaying = False;
        pass;

    def __OnViewValueChanged(self, event):
        self.__Calc.a =  event.Value;

    def __OnValueChanged(self, evt):
        self.__View.Value =  evt.Value;
        self.__View.Result = evt.Source.Sum();
        
        if(self.__IsPlaying != True):
            self.__recordValues.append(evt.Value);

    def __OnFileWriter(self, evt):
        with open("valuechange.txt", mode="a+") as file:
            file.write("{0}\n".format(evt.Source.Sum()));
            
    def __OnReplay(self, evt):
        t =  threading.Thread(target=self.__StartReplayer);
        t.daemon =True
        t.start();

    def  __StartReplayer(self):
        self.__IsPlaying = True;
        self.__View.Value  = 0.0;
        
        freq  =  len(self.__recordValues) + 1;
        period  = 1/freq;
        print(freq)
        for value in  self.__recordValues:
            self.__Calc.a= value;
            time.sleep(period);
        
        self.__IsPlaying = False;
        


    def Launch(self):
        if(self.__View is not None):
            self.__View.Show();




    
if __name__ =="__main__":
    view   = CalculatorView();
    calc   =   Calculator(2, 1);
    contrl =   Controller(view, calc);
    view.Value= 12;
    calc.a = 14;
    print(view.Value);
    contrl.Launch();
    


    


            
    
