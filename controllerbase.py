

class IResource(object):
    pass;


class ControllerBase(object):

    """
      The base class for the view model that will provided the 
    """
    def __init__(self, parent = None,
                 resource  = None):
        if(parent is not None):
            if(isinstance(parent,ControllerBase) is not True):
                raise TypeError("@ViewModel : expecting parameter 1 to be ViewModel object")
        if(resource is not None):
            if(isinstance(resource,IResource) is not True):
                raise TypeError("@ViewModel : expecting parameter 2 to be IResource object")
        self.__parent    =  parent  
        self.__resource  =  resource

    def Localize(self, key:str , default_val:str = None):
        result  =  default_val;
        if(self.Resource is not None):
            result  = self.Resource.Get(key, default_val)
        return result

    @property
    def Resource(self):
        return self.__resource

    @property
    def Parent(self):
        return self.__parent
