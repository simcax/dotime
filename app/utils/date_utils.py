'''Class to supply date help'''
from datetime import datetime,timedelta
class DoTimeDataHelp:
    '''Class supplying date help'''
    language = "en"

    @classmethod
    def all_days(cls,language):
        '''A list of all days in english'''
        if language == 'en':
            days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        else:
            days = []
        return days

    def day_name(self,language,day_number):
        '''
            Returns the day name for the language given
            Currently supports: en, da
        '''
        if language != 'en':
            dayname = "Language not supported"
        elif self.daynumber_within_range(day_number):
            dayname = self.en_dayname(language,day_number)
        else:
            dayname = "Daynumber out of range"
        return dayname

    def en_dayname(self, language,day_number):
        '''Return the dayname for a daynumber'''
        days = self.all_days(language)
        if len(days) != 0:
            return_day = days[day_number]
        else:
            return_day = "unknown"
        return return_day

    @classmethod
    def daynumber_within_range(cls,day_number):
        '''control method to make sure the values are within range'''
        range_ok = bool(day_number >= 0 and day_number <= 7)
        return range_ok

    @classmethod
    def get_start_end_of_week(cls,the_date):
        '''
            Takes a date in iso format YYYY-MM-DD
            Returns start and end date for the week the date is in
        '''
        dt = datetime.strptime(the_date, '%Y-%m-%d')
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        return start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d")