def convertDateFormats(Date, currentFormat, newFormat):
    SupportedFormats = ['mm-dd-yyyy', 'dd-mm-yyyy', 'yyyy-mm-dd', 'mm/dd/yyyy', 'dd/mm/yyyy', 'now-format']
    if currentFormat not in SupportedFormats:
        raise ValueError(f'{currentFormat} is not supported as currentFormat')
    if newFormat not in SupportedFormats:
        raise ValueError(f'{newFormat} is not supported as newFormat')

    monthLookup = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
                   10: 'October', 11: 'November', 12: 'December'}

    if currentFormat == 'mm-dd-yyyy':
        if newFormat == 'now-format':
            try:
                day, month, year = int(Date.split('-')[1]), monthLookup[int(Date.split('-')[0])], int(Date.split('-')[2])
            except ValueError:
                raise ValueError('currentFormat was not formatted correctly')
            except KeyError:
                raise KeyError('invalid month')

            newFormat = f'{month} {day}, {year}'
            return newFormat

    elif currentFormat == 'mm/dd/yyyy':
        if newFormat == 'now-format':
            try:
                day, month, year = int(Date.split('/')[1]), monthLookup[int(Date.split('/')[0])], int(Date.split('/')[2])
            except ValueError:
                raise ValueError('startDate was not formatted correctly')
            except KeyError:
                raise KeyError('invalid month')

            newFormat = f'{month} {day}, {year}'
            return newFormat

    elif currentFormat == 'yyyy-mm-dd':
        if newFormat == 'now-format':
            try:
                year, month, day = int(Date.split('-')[0]), monthLookup[int(Date.split('-')[1])], int(Date.split('-')[2])
            except ValueError:
                raise('currentFormat was not formatted correctly')
            except KeyError:
                raise KeyError('invalid month')

            newFormat = f'{month} {day}, {year}'
            return newFormat