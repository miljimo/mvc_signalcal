import time;
from events import EventHandler, Event
from valuechangedevent import ValueChangedEvent

    

class Calculator(object):

    def __init__(self, a: float, b: float):
        self.__a  =  a;
        self.__b  =  b;
        self.ValueChanged = EventHandler();
       

    @property
    def a(self):
        return self.__a;
    
    @a.setter
    def a(self, value):
        if(self.__a  != value):
            self.__a  =  value;
            if(self.ValueChanged  is not None):
                self.ValueChanged(ValueChangedEvent(self, self.__a))

    @property
    def b(self):
        return self.__b;

    def Sum(self):
        return self.__a + self.__b

    def Divide(self):
        return self.__a / self.__b;

def OnCalculateValueChanged(evt):
    print("Value has changed  = {0}".format(evt.Source.Sum()));

def OnFileWriter(evt):
    with open("valuechange.txt", mode="a+") as file:
        result =  "{0} + {1} = {2}\n".format(evt.Source.a , evt.Source.b, evt.Source.Sum());
        file.write(result);
        
if __name__ =="__main__":
    result =  0;
    cal =  Calculator(4,2);
    cal.ValueChanged  += OnCalculateValueChanged;
    cal.ValueChanged  += OnFileWriter;

    cal.a = 90;
    cal.a = 100;
    cal.a = 100;
    
       
