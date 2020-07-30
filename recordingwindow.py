import os
import wx
import wx.lib.agw.shapedbutton as SB
from events import Event, EventHandler

class FileOpenEventArgs(Event):

    def __init__(self,filename: str):
        super().__init__("File.Open.Event.Args")
        self.__Filename =  filename

    @property
    def Filename(self):
        return self.__Filename


class ArgsInitialiser(object):

    def __init__(self, **kwargs):
        self.__Kwargs  =  kwargs;
        
    def Initial(self, field , value):
        if(type(field) != str):
            raise TypeError("@Initial: expecting a string field")
        else:
            if(field in self.__Kwargs) is not True:
                self.__Kwargs[field] = value;
    @property
    def Arguments(self):
        return self.__Kwargs;

class SizeCalculator(object):

    def __init__(self, width:float , height:float):
        self.__Width =  width;
        self.__Height = height

    def Width(self, percentage:float):
        return int(round((self.__Width * percentage) / 100,1))
    
    def Height(self, percentage:float):
        return int(round((self.__Height * percentage) / 100,1))

class wxCustomLabel(wx.StaticText):
    def __init__(self, parent , **kwargs):
        super().__init__(parent,  **kwargs)

    def SetLabel(self, label:str):
        width =  self.Size.Width;
        dcxt =  wx.ScreenDC()
        dcxt.SetFont(self.GetFont())
        textWidth  =  dcxt.GetTextExtent(label)[0];
        
        length = len(label);
        maxUiLength = int( (width *  length) / textWidth)
        newString = "";
        lines  =  int(textWidth / width)
        offsetX =  0;
        for index in range(0, lines):
            lineText = label[offsetX: maxUiLength]
            offsetX += maxUiLength
            maxUiLength = maxUiLength * 2
            newString +=lineText +"\n"
        newString +=   label[offsetX:maxUiLength ] 
        super().SetLabel(newString)
      

class UITimesheetWindow(object):

    def __init__(self,parent):
        self.__Parent  =  parent;
        self._SetupUI()
        

    def  _SetupUI(self):
        self.__SizeCal  =  SizeCalculator(self.__Parent.Size.Width, self.__Parent.Size.Height);
        # Content Panel  UI 
        self.__ContentPane  =  wx.Panel(self.__Parent);
        if(self.__Parent.CanSetTransparent()):
            self.__ContentPane.SetTransparent(100)

        contentSizer    =  wx.BoxSizer(wx.VERTICAL)

        # Create the recording layout of the UI
        recordingPanel  =  wx.Panel(self.ContentPane, size =  wx.Size(0,100))
        recordingPanel.SetTransparent(100);

        # Layout the recording panel
        recordingSizer              =  wx.BoxSizer(wx.HORIZONTAL);

        # Layout the detail panel
        recordingDetailsPanelSize   =  wx.Size(self.__SizeCal.Width(75), 500);
        recordingDetailPanel        =  wx.Panel(recordingPanel , size=recordingDetailsPanelSize);        
        recordingDetailPanelSizer  =   wx.BoxSizer(wx.VERTICAL)
        
      
        #Start layouting out project combox
        
        pnlComboxProjects       =  wx.Panel(recordingDetailPanel)
        pnlComboxProjectsSizer  =  wx.BoxSizer(wx.HORIZONTAL)
        
        lblProjectCombox        =  wxCustomLabel(pnlComboxProjects, label="Select Projects:",
                                                 size=wx.Size(100, wx.DefaultSize.Height) ,
                                                 style = wx.ALIGN_LEFT)        
        projectCombox           = wx.ComboBox(pnlComboxProjects, size=wx.Size(320 ,wx.DefaultSize.Height) ,
                                              style= wx.CB_READONLY)
        self.btnOpenXlsTimesheet     = wx.Button(pnlComboxProjects, size  = wx.Size(100, wx.DefaultSize.Height), label = "Open Timsheet")
        
        pnlComboxProjectsSizer.Add(lblProjectCombox ,flag=wx.ALL | wx.EXPAND, border  =  1);
        pnlComboxProjectsSizer.Add(projectCombox,flag=wx.ALL, border  =  1);
        pnlComboxProjectsSizer.Add(self.btnOpenXlsTimesheet,flag=wx.ALL, border  =  1);
        pnlComboxProjectsSizer.Fit(pnlComboxProjects)
        pnlComboxProjects.SetSizer(pnlComboxProjectsSizer);
       
     
        #Start Layout the description field
        
        pnlPrjDescrition       =  wx.Panel(recordingDetailPanel)
        pnlPrjDescritionSizer  =  wx.BoxSizer(wx.HORIZONTAL)
        
        lblPrjDescrition       =  wxCustomLabel(pnlPrjDescrition, label="",
                                                 size=wx.Size(100, wx.DefaultSize.Height) )
        
        lblPrjDescritionText   =  wxCustomLabel(pnlPrjDescrition, label="Text here",
                                                 size=wx.Size(320, 100) ,
                                                 style = wx.ALIGN_LEFT)
        lblPrjDescritionText.Wrap(lblPrjDescritionText.Size.Width)

        pnlElapsedTimer  = wx.Panel(pnlPrjDescrition, size=wx.Size(100,100))
        pnlElapseTimerSizer  =  wx.BoxSizer(wx.VERTICAL)
        lblElapseTitle       =  wxCustomLabel(pnlElapsedTimer,
                                              label ="Elapsed Time",
                                              style = wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE,
                                              size=wx.Size(100, wx.DefaultSize.Height))


        lblElapseValue       =  wxCustomLabel(pnlElapsedTimer,
                                              label ="0:23:42.0920",
                                              style = wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE,
                                              size=wx.Size(100, wx.DefaultSize.Height))
        
       

        pnlElapseTimerSizer.Add(lblElapseTitle, flag= wx.ALL | wx.EXPAND, border=5);
        pnlElapseTimerSizer.Add(lblElapseValue, flag= wx.ALL | wx.EXPAND);
        pnlElapsedTimer.SetSizer(pnlElapseTimerSizer)
        
        
        pnlPrjDescritionSizer.Add(lblPrjDescrition ,flag=wx.ALL | wx.EXPAND, border  =  1);
        pnlPrjDescritionSizer.Add(lblPrjDescritionText,flag=wx.ALL, border  =  1);
        pnlPrjDescritionSizer.Add(pnlElapsedTimer,flag=wx.ALL, border  =  1);
        pnlPrjDescritionSizer.Fit(pnlPrjDescrition);
        pnlPrjDescrition.SetSizer(pnlPrjDescritionSizer);

        # Laying out the recording project details
        recordingDetailPanelSizer.Add(pnlComboxProjects, flag= wx.EXPAND | wx.ALL, border =0)
        recordingDetailPanelSizer.Add(pnlPrjDescrition, flag= wx.EXPAND | wx.ALL, border =0)       
        recordingDetailPanel.SetSizer(recordingDetailPanelSizer)
        
        recordingPanelOperator =  wx.Panel(recordingPanel, size=  wx.Size(self.__SizeCal.Width(25),500));
        position =  wx.Point(recordingDetailPanel.Size.Width , 0);
        recordingPanelOperator.SetPosition(position)
        
        #Layout the recording controls
        recordingPanelOperatorSizer =  wx.BoxSizer(wx.VERTICAL);
        btnStartRecording      =  wx.Button(recordingPanelOperator , label="Start")
        btnPauseRecording      =  wx.Button(recordingPanelOperator , label="Pause")
        btnStopRecording       =  wx.Button(recordingPanelOperator , label="Stop")
        
        recordingPanelOperatorSizer.Add(btnStartRecording)
        recordingPanelOperatorSizer.Add(btnPauseRecording)
        recordingPanelOperatorSizer.Add(btnStopRecording)
        recordingPanelOperator.SetSizer(recordingPanelOperatorSizer)
        #Add the left and right panel
        recordingSizer.Add(recordingDetailPanel , border = 0)
        recordingSizer.Add(recordingPanelOperator,border = 0)
        recordingPanel.Layout()
        recordingPanel.SetSizer(recordingSizer);
       
        contentSizer.Add(recordingPanel , flag = wx.EXPAND | wx.ALL, border=5)
        
        contentSizer.Fit( self.ContentPane);
        self.ContentPane.SetSizer(contentSizer)

    @property
    def ContentPane(self):
        return self.__ContentPane;
        
        
        
class TimesheetWindow(wx.Frame):
    DEFAULT_HEIGHT = 500
    DEFAULT_WIDTH  = 700
    
    def __init__(self, parent, **kwargs):
        self.__Initialiser  = ArgsInitialiser(**kwargs)
        self.__Initialiser.Initial('size', wx.Size(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT))   
        self.__Initialiser.Initial('pos' , wx.Point(0,0))
        # self.__Initialiser.Initial('style', wx.BORDER_DEFAULT | wx.BORDER_SIMPLE )
        self.__Initialiser.Initial('title' , 'Recording Timesheet')
        super().__init__(parent , **self.__Initialiser.Arguments)
        self.__ui  =  UITimesheetWindow(self);
        # Event Handler
        self.FileOpened  =  EventHandler();

        # Add Event Listener to self.__btnOpenXlsTimesheet
        self.__ui.btnOpenXlsTimesheet.Bind(wx.EVT_BUTTON, self.__OpenXLsTimesheet)


    def __OpenXLsTimesheet(self, evnt):
        filters  =  "XLS Files(*.xls) |*.xls|XLSX Files(*.xlsx)|*.xlsx| ODS Files(*.ods)|*.ods"
        dialog = wx.FileDialog(self, "Open Timesheet", wildcard=filters)
        status  = dialog.ShowModal();
        if(status == wx.OK):
            filename  =  dialog.GetPath();                
            if(os.path.exists(filename)):
                if(self.FileOpened is not None):
                    self.FileOpened(filename);


  
       
        

    @property
    def ContentPane(self):
        return self.__ui.ContentPane;
      
        


app = wx.App();
window  =  TimesheetWindow(None);
window.Show();
app.MainLoop();
