from events import Event;

class ValueChangedEvent(Event):
    def __init__(self, source , a):
        super().__init__("value.changed.event");
        self.__Value  =a;
        self.__Source  =  source;
        
    @property
    def Value(self):
        return self.__Value;

    @property
    def Source(self):
        return self.__Source;
