from datetime import datetime

class AccessibleTime(object):
    """ represents the period of time that a course/task is accessible """
    def __init__(self,val=None):
        """ 
            Parse a string/a boolean to get the correct time period.
            Correct values for val:
            True (task always open)
            False (task always closed)
            2014-07-16 11:24:00 (task is open from 2014-07-16 at 11:24:00)
            2014-07-16 (task is open from 2014-07-16)
            / 2014-07-16 11:24:00 (task is only open before the 2014-07-16 at 11:24:00)
            / 2014-07-16 (task is only open before the 2014-07-16)
            2014-07-16 11:24:00 / 2014-07-20 11:24:00 (task is open from 2014-07-16 11:24:00 and will be closed the 2014-07-20 at 11:24:00)
            2014-07-16 / 2014-07-20 11:24:00 (...)
            2014-07-16 11:24:00 / 2014-07-20 (...)
            2014-07-16 / 2014-07-20 (...)
        """
        if val is None or val == True:
            self.val = [None, None]
        elif val == False:
            self.val = [0, 0]
        else: #str
            values = val.split("/")
            if len(values) == 1:
                self.val = [self._parse_date(values[0].strip()), None]
            else:
                self.val = [self._parse_date(values[0].strip()), self._parse_date(values[1].strip())]
    
    def _parse_date(self,date):
        """ Parse a valid date """
        if date == "":
            return None
        
        for f in ["%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M", "%Y-%m-%d %H", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S","%d/%m/%Y %H:%M", "%d/%m/%Y %H", "%d/%m/%Y"]:
            try:
                return datetime.strptime(date, f)
            except:
                pass
        raise Exception("Unknow format for " +date)
    
    def is_open(self,when=None):
        """ Returns True if the course/task is still open """        
        if when == None:
            when = datetime.now()
            
        f,s = self.val
        if f != None and s != None and f >= s:
            return False
        if f != None and f > when:
            return False
        if s != None and s < when:
            return False
        return True