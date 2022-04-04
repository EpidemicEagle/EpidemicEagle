def GuessFormat(datestring):

    # define the bricks
    bricks = re.compile(r"""
            (?(DEFINE)
                (?P<year_def>[12]\d{3})
                (?P<year_short_def>\d{2})
                (?P<month_def>January|February|March|April|May|June|
                July|August|September|October|November|December)
                (?P<month_short_def>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)
                (?P<day_def>(?:0[1-9]|[1-9]|[12][0-9]|3[01]))
                (?P<weekday_def>(?:Mon|Tue|Wednes|Thurs|Fri|Satur|Sun)day)
                (?P<weekday_short_def>Mon|Tue|Wed|Thu|Fri|Sat|Sun)
                (?P<hms_def>T?\d{2}:\d{2}:\d{2})
                (?P<hm_def>T?\d{2}:\d{2})
                (?P<ms_def>\d{5,6})
                (?P<delim_def>([-/., ]+|(?<=\d|^)T))
            )
            # actually match them
            (?P<hms>^(?&hms_def)$)|(?P<year>^(?&year_def)$)|(?P<month>^(?&month_def)$)|(?P<month_short>^(?&month_short_def)$)|(?P<day>^(?&day_def)$)|
            (?P<weekday>^(?&weekday_def)$)|(?P<weekday_short>^(?&weekday_short_def)$)|(?P<hm>^(?&hm_def)$)|(?P<delim>^(?&delim_def)$)|(?P<ms>^(?&ms_def)$)
            """, re.VERBOSE)

    # delim
    delim = re.compile(r'([-/., ]+|(?<=\d)T)')

    # formats
    formats = {'ms': '%f', 'year': '%Y', 'month': '%B', 'month_dec': '%m', 'day': '%d', 'weekday': '%A', 'hms': '%H:%M:%S', 'weekday_short': '%a', 'month_short': '%b', 'hm': '%H:%M', 'delim': ''}

    parts = delim.split(datestring)
    out = []
    for index, part in enumerate(parts):
        try:
            brick = dict(filter(lambda x: x[1] is not None, bricks.match(part).groupdict().items()))
            key = next(iter(brick))

            # ambiguities
            if key == 'day' and index == 2:
                key = 'month_dec'

            item = part if key == 'delim' else formats[key]
            out.append(item)
        except AttributeError:
            out.append(part)

    return "".join(out)

import regex as re

datestrings = [datetime.now().isoformat(), '2006-11-02', 'Thursday, 10 August 2006 08:42:51', 'August 9, 1995', 'Aug 9, 1995', 'Thu, 01 Jan 1970 00:00:00', '21/11/06 16:30', 
'06 Jun 2017 20:33:10']

# test
for dt in datestrings:
    print("Date: {}, Format: {}".format(dt, GuessFormat(dt)))