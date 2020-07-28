import datetime as dt;
import math
import time;
from   threading import Thread, Lock
from events import EventHandler, Event


class ElapseEventArgs(Event):

    def __init__(self, seconds):
        super().__init__("Timesheet.recorder.Elapse.event")
        if(type(seconds) != float):
            if(type(seconds) != int):
                raise TypeError("@ElapseEventArgs: expecting parameter 1 to be a floating number");
            
        self.__Seconds      = int(seconds);
        self.__MiliSeconds  = round(seconds - self.__Seconds, 2);
        self.__Minutes      = int(self.__Seconds / 60);
        self.__Hours        = int(self.__Minutes / 60);
        self.__Elapsed      = seconds;

    @property
    def Elapsed(self):
        return self.__Elapsed;

    @property
    def Seconds(self):
        return self.__Seconds;

    @property
    def Hours(self):
        return self.__Hours;

    @property
    def Minutes(self):
        return self.__Minutes;

    @property
    def MiliSeconds(self):
        return self.__MiliSeconds
    

class TimesheetRecorder(object):

    def __init__(self, interval=  1):
        self.__StartTime   =  dt.datetime.now();
        self.__IsStarted   =  False;
        self.__RunThread   =  None;
        self.__Interval    =   interval if ((type(interval) == float) or (type(interval) == int)) else 1;
        self.__Locker      =   Lock();

        #Event Handler
        self.Completed      = EventHandler();
        self.Progressed     = EventHandler();
        pass;

    @property
    def Interval(self):
        return self.__Interval;
    
    @property
    def IsStarted(self):
        return self.__IsStarted;

    def Start(self):
        try:
            self.__Locker.acquire();
            if(self.IsStarted != True):
                self.__RunThread  = Thread(target  =  self.__StartRecording);
                self.__RunThread.daemon  = True
                self.__RunThread.start();
        except Exception as err:
            self.__Locker.release();
            raise err     
      

    def Stop(self):
        try:
            self.__Locker.acquire();
            if(self.IsStarted is True):
                self.__IsStarted = False;
                if(self.__RunThread != None):
                    self.__RunThread.join(1)
                    self.__RunThread = None
            self.__Locker.release()
        except Exception as err:
            self.__Locker.release()
            raise err
       

    def __StartRecording(self):
       
        self.__Locker.release();
        self.__IsStarted   =  True;
        now   = dt.datetime.now();
        total_seconds  =  0;
     
        while (self.IsStarted):
            time.sleep(self.Interval);
            current_now    =  dt.datetime.now();
            delta_time     =  current_now - now;
            total_seconds  += delta_time.total_seconds();
                
            #if progress events
            if(self.Progressed is not None):
                self.Progressed(ElapseEventArgs(total_seconds));
            now = current_now;
                

        if(self.Completed is not None):
                self.Completed(ElapseEventArgs(total_seconds))
                
       
       

if __name__ =="__main__":
    end  = "\n\r"
    def Completed(event):
        print ("\nCompleted at = {0}:{1}:{2}.{3}".format(event.Hours, event.Minutes, event.Seconds, event.MiliSeconds),end);

    def Progressing(event):
        print ("\nProgress at= {0}:{1}:{2}.{3}".format(event.Hours, event.Minutes, event.Seconds, event.MiliSeconds),end);

        
    recorder  =  TimesheetRecorder();
    recorder.Completed += Completed;
    recorder.Progressed+= Progressing
    recorder.Start();

    count  = 0;
    try:
        while(True):
            option  =  input("\nEnter e for stop = ");
            if(option =='e'):
                recorder.Stop()
            elif(option =='s'):
                if(recorder.IsStarted is not True):
                    recorder.Start()
            time.sleep(1/100)
    except KeyboardInterrupt as err:
        recorder.Stop();
        
        
        

