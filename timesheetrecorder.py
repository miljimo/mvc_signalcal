import datetime as dt;
import math
import time;
import threading;
from events import EventHandler, Event
from timeobject import TimeObject


class RecordingEventArgs(Event):

    def __init__(self, seconds):
        super().__init__("Timesheet.recorder.Elapse.event")
        if(type(seconds) != float):
            if(type(seconds) != int):
                raise TypeError("@ElapseEventArgs: expecting parameter 1 to be a floating number");
                 
        milliseconds     = 1000 * seconds;
        self.__Elapsed  = TimeObject(milliseconds);

    @property
    def Elapsed(self):
        return self.__Elapsed;

    
class RecordingFaultEvent(Event):
    def __init__(self, error: Exception):
        super().__init__("recorder.fault.event")
        self.__Error  =  error

    @property
    def Error(self):
        return self.__Error

class TimesheetRecorder(object):

    def __init__(self, interval=  1):
        self.__StartTime   =  dt.datetime.now();
        self.__IsStarted   =  False;
        self.__RunThread   =  None;
        self.__Interval    =   interval if ((type(interval) == float) or (type(interval) == int)) else 1;
        self.__Locker      =   threading.Lock();

        #Event Handler
        self.Completed      = EventHandler();
        self.Progressed     = EventHandler();
        self.Started        = EventHandler();
        self.Failured       = EventHandler();
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
                self.__RunThread  = threading.Thread(target  =  self.__StartRecording);
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
                    if(threading.current_thread().ident != self.__RunThread.ident):
                        self.__RunThread.join(1)
                        self.__RunThread = None
            self.__Locker.release()
        except Exception as err:
            self.__Locker.release()
            raise err
       

    def __StartRecording(self):

        try:
            self.__Locker.release();
            self.__IsStarted   =  True;
            now   = dt.datetime.now();
            total_seconds  =  0;
            
            if(self.Started is not None):
                self.Started(Event("recorder.start.event"));
         
            while (self.IsStarted):
                time.sleep(self.Interval);
                current_now    =  dt.datetime.now();
                delta_time     =  current_now - now;
                total_seconds  += delta_time.total_seconds();
                    
                #if progress events
                if(self.Progressed is not None):
                    self.Progressed(RecordingEventArgs(total_seconds));
                now = current_now;
                    

            if(self.Completed is not None):
                    self.Completed(RecordingEventArgs(total_seconds))
        except Exception as err:
            self.__IsStarted =  False
            self.Failured(RecordingFaultEvent(err))
           
                
       
       

if __name__ =="__main__":
    end  = ""

    def OnStarted(event):
        print("Starting Recording")
        
    def OnCompleted(event):
        print ("\nCompleted at = {0}:{1}:{2}.{3}".format(event.Elapsed.Hours, event.Elapsed.Minutes, event.Elapsed.Seconds, event.Elapsed.Milliseconds),end);

    def OnProgressing(event):
        print ("\nProgress at= {0}:{1}:{2}.{3}".format(event.Elapsed.Hours, event.Elapsed.Minutes, event.Elapsed.Seconds, event.Elapsed.Milliseconds),end);
    def OnFailed(event):
        print(event.Error)
        
    recorder  =  TimesheetRecorder();
    recorder.Started    += OnStarted
    recorder.Completed  += OnCompleted;
    recorder.Progressed += OnProgressing
    recorder.Failured   += OnFailed
    recorder.Start();

    count  = 0;
    try:
        while(True):
            time.sleep(1/100)
    except KeyboardInterrupt as err:
        recorder.Stop();
        
        
        

