'''Class to supply date help'''

class DoTimeDataHelp:
    language = "en"

    def all_days(self,language):
        '''A list of all days in english'''
        if language == 'en':
            days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        return days

    def day_name(self,language,day_number):
        '''
            Returns the day name for the language given
            Currently supports: en, da
        '''
        if self.daynumber_within_range(day_number):
            if language == 'en':
                dayname = self.en_dayname(language,day_number)
            else:
                dayname = "Language not supported"
        else:
            dayname = "Daynumber out of range"
        return dayname

    def en_dayname(self, language,day_number):
        '''Return the dayname for a daynumber'''
        days = self.all_days(language)
        return days[day_number]

    def daynumber_within_range(self,day_number):
        '''control method to make sure the values are within range'''
        if day_number >= 0 and day_number <= 7:
            range_ok = True
        else:
            range_ok = False
        return range_ok
