import tkinter as tk
from events import EventHandler , Event;
from valuechangedevent import ValueChangedEvent;



class CalculatorView(tk.Frame):

    def __init__(self, parent= tk.Tk()):
        super().__init__(master  = parent,background="white",
                                width =500,
                                relief=tk.FLAT,
                                height=250,
                                bd=1)
        self.parent  =  parent;
        self.parent.title("Signal Calculator");
        self.pack();
        self.__acceptValue ="";
        self.SetUI();
        self.Clicked      = EventHandler();
        self.ValueChanged = EventHandler();
        self.Result =  0.0

    def SetUI(self):

        fieldpanel  =  tk.LabelFrame(self, width =40);
            
        lblvalue  =  tk.Label(fieldpanel,
                              text="Value :",
                              bg="#ffffff",
                              font=("Courier", 20));

        lblvalue.pack(side = tk.LEFT);

        self.__txtVal =  tk.StringVar();
        self.__txtVal.trace('w', self.text_changed);
        

        self.txtvalue  =  tk.Entry(fieldpanel, width= 15,
                              bg="#ffffff",
                              fg='red',
                              bd=0,
                              textvariable = self.__txtVal,
                              font=("Courier", 25),
                              relief=tk.FLAT);
        
        self.txtvalue.pack(side = tk.LEFT)

        fieldpanel.pack(padx=5, pady=5);
        

        # The Result
        panel_result =  tk.LabelFrame(self,width =40,bd=0);
        lblresult =  tk.Label(panel_result, text="Result is =",
                              font=("Courier", 25),
                              bg='#ffffff');
        lblresult.pack(side =tk.LEFT);


         # Create a button.
        self.button = tk.Button(panel_result ,
                       text="0.00",
                       bd=0,
                       padx=0, pady=0,
                       fg='#e6f9ff',
                       font=("Courier", 17),
                       activebackground ="#66ccff",
                       activeforeground ="#4d3d00",
                       width = 10,
                       bg="#0086b3",
                       command  = self.button_clicked);
        self.button.pack(side =tk.RIGHT);

        panel_result.pack();
        self.parent.resizable(0,0);
        self.pack(padx=5, pady=5);
        self.config(bg="white");
        self.parent.config(bg='white');
        #self.parent.overrideredirect(1)

    def button_clicked(self):       
       self.clear_value("0.00");
       self.Result = "0.00";
       if(self.Clicked is not None):
           self.Clicked(Event("calview.click.event"));
       
       

    def text_changed(self,*args):
        entered_value = ""
        try:
            accepted_value  =  0.00;
            entered_value =  self.txtvalue.get();
            if(entered_value == ""):
                accepted_value = 0.00;
            else:
                accepted_value    = float(entered_value);
            #Success changed.
            if(accepted_value != self.__acceptValue):
                self.__acceptValue =  accepted_value               
                if(self.ValueChanged is not None):                   
                    self.ValueChanged(ValueChangedEvent(self,self.__acceptValue));
            
        except Exception as err:
            self.txtvalue.delete(0, len(entered_value));
            self.txtvalue.insert(0,self.__acceptValue);
            pos  = entered_value.find('.');
            if(pos < 0):
                pos = len(str(entered_value));
            self.txtvalue.icursor(pos-1);

    def clear_value(self, val):
       self.txtvalue.delete(0, len(self.txtvalue.get()));
       self.txtvalue.insert(0,val);

    @property
    def Result(self):
        return float(self.button.cget('text'));
    
    @Result.setter
    def Result(self, value):
        if(type(value) == float) or (type(value) ==int):
            self.button['text']= str(value);
            #self.button.config(height= int(self.Result))
            

    def Show(self):
        self.pack();
        self.mainloop();

    @property
    def Value(self):
        return self.__acceptValue;
    
    @Value.setter
    def Value(self , value):
        if(value != self.__acceptValue):
            accepted_value    = float(value);
            self.clear_value(str(accepted_value));
        
        
def OnValueChanged(evt):
    print(evt.Value);

if __name__ =="__main__":
    frame  =  CalculatorView(tk.Tk());
    frame.ValueChanged+=OnValueChanged;

    frame.Value  = 78.0;
    frame.Value = 781.0;
    frame.Show();
    
    
   
   
