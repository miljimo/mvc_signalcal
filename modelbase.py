
from events import EventHandler;


class ModelBase(object):

    def __init__(self):
        self.__DataChanged = EventHandler();

    @property
    def DataChanged(self):
        return self.__DataChanged;

    @property
    def DataChanged(self, handler):
        if(handler == self.__DataChanged):
            self.__DataChanged = handler;


    




        
