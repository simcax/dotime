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
        range_ok = bool( 0 <= day_number <= 7)
        return range_ok

    @classmethod
    def get_start_end_of_week(cls,the_date):
        '''
            Takes a date in iso format YYYY-MM-DD
            Returns start and end date for the week the date is in
        '''
        date_of_the_date = datetime.strptime(the_date, '%Y-%m-%d')
        start = date_of_the_date - timedelta(days=date_of_the_date.weekday())
        end = start + timedelta(days=6)
        return start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d")

    @classmethod
    def convert_minutes_to_hours(cls,minutes):
        '''
            Method to convert minuts into hours and minutes
            Takes: minutes
            Returns: hours and minutes (both ints)
            Thx to @Chris on Stack Overflow: https://stackoverflow.com/a/51566057
            for this simple solution :-)
        '''
        result_hours = minutes // 60
        result_minutes = minutes % 60
        return result_hours, result_minutes

    @classmethod
    def convert_hours_and_minutes_to_minutes(cls,hours_and_minutes):
        """
            Takes input as number of hours:minutes and converts it to a total number of minutes
        """
        return_value = False
        if ":" in hours_and_minutes and len(hours_and_minutes) == 5:
            minutes = int(hours_and_minutes.split(':')[0]) * 60
            minutes += int(hours_and_minutes.split(':')[1])
            return_value = minutes
        return return_value
