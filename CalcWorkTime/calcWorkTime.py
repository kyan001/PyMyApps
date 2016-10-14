import datetime
import consoleiotools as cit

times = [
    ("2014/10/8 9:20", "2014/10/8 23:30"),
    ("2014/10/9 10:30", "2014/10/9 21:40"),
    ("2014/10/10 10:00", "2014/10/10 19:20"),
    ("2014/10/11 9:30", "2014/10/11 22:30"),
    ("2014/10/12 10:44", "2014/10/12 19:00"),
    ("2014/10/14 10:00", "2014/10/14 20:20"),
    ("2014/10/15 10:00", "2014/10/15 21:00"),
    ("2014/10/16 10:30", "2014/10/16 20:42"),
    ("2014/10/17 9:45", "2014/10/17 18:45"),
    ("2014/10/18 10:35", "2014/10/18 18:30"),
    ("2014/10/20 10:00", "2014/10/20 20:35"),
    ("2014/10/21 10:17", "2014/10/21 22:00"),
    ("2014/10/22 10:30", "2014/10/22 22:00"),
    ("2014/10/23 10:30", "2014/10/23 21:10"),
    ("2014/10/24 10:00", "2014/10/24 18:50"),
    ("2014/10/25 11:10", "2014/10/25 19:00"),
    ("2014/10/26 11:00", "2014/10/26 21:00"),
    ("2014/10/28 10:30", "2014/10/28 21:00"),
    ("2014/10/29 11:00", "2014/10/29 21:35"),
    ("2014/10/30 10:40", "2014/10/30 21:50"),
    ("2014/10/31 11:00", "2014/10/31 18:30"),
    ("2014/11/1 10:45", "2014/11/1 18:00"),
    ("2014/11/3 10:30", "2014/11/3 12:20"),
    ("2014/11/3 15:45", "2014/11/3 22:15"),
    ("2014/11/4 10:30", "2014/11/4 21:12"),
    ("2014/11/5 10:45", "2014/11/5 22:30"),
    ("2014/11/6 10:55", "2014/11/6 20:31"),
    ("2014/11/7 10:55", "2014/11/7 18:30"),
    ("2014/11/8 10:30", "2014/11/8 18:00"),
    ("2014/11/10 9:30", "2014/11/10 19:00"),
    ("2014/11/11 9:16", "2014/11/11 20:00"),
    ("2014/11/12 9:56", "2014/11/12 20:00"),
    ("2014/11/13 9:30", "2014/11/13 21:31"),
    ("2014/11/14 9:50", "2014/11/14 19:00"),
    ("2014/11/15 10:45", "2014/11/15 18:02"),
    ("2014/11/17 9:50", "2014/11/17 20:40"),
    ("2014/11/18 9:30", "2014/11/18 21:21"),
    ("2014/11/19 10:21", "2014/11/19 21:10"),
    ("2014/11/20 10:15", "2014/11/20 21:00"),
    ("2014/11/21 10:40", "2014/11/21 18:40"),
    ("2014/11/22 10:40", "2014/11/22 19:20"),
    ("2014/11/23 10:15", "2014/11/23 16:11"),
    ("2014/11/24 10:10", "2014/11/24 18:00"),
    ("2014/11/25 9:30", "2014/11/25 18:30"),
    ("2014/11/27 9:30", "2014/11/27 12:46"),
    ("2014/12/1 10:15", "2014/12/1 12:30"),
    ("2014/12/1 14:15", "2014/12/1 21:45"),
    ("2014/12/2 10:14", "2014/12/2 20:30"),
    ("2014/12/3 10:17", "2014/12/3 22:00"),
    ("2014/12/4 10:30", "2014/12/4 22:30"),
    ("2014/12/5 10:30", "2014/12/5 18:30"),
    ("2014/12/6 10:45", "2014/12/6 18:30"),
    ("2014/12/8 10:10", "2014/12/8 20:20"),
    ("2014/12/9 10:05", "2014/12/9 21:40"),
    ("2014/12/10 10:15", "2014/12/10 21:00"),
    ("2014/12/11 10:15", "2014/12/11 20:30"),
    ("2014/12/12 10:30", "2014/12/12 18:30"),
    ("2014/12/13 10:52", "2014/12/13 18:30"),
    ("2014/12/15 10:22", "2014/12/15 21:50"),
    ("2014/12/16 10:35", "2014/12/16 21:10"),
    ("2014/12/17 10:30", "2014/12/17 22:40"),
    ("2014/12/18 9:26", "2014/12/18 21:50"),
    ("2014/12/19 11:00", "2014/12/19 18:30"),
    ("2014/12/20 11:30", "2014/12/20 17:30"),
    ("2014/12/22 10:00", "2014/12/22 21:30"),
    ("2014/12/23 10:20", "2014/12/23 20:40"),
    ("2014/12/24 10:25", "2014/12/24 21:10"),
    ("2014/12/25 10:35", "2014/12/25 21:40"),
    ("2014/12/26 11:12", "2014/12/26 18:30"),
    ("2014/12/28 9:50", "2014/12/28 18:45"),
    ("2014/12/29 10:12", "2014/12/29 21:10"),
    ("2014/12/30 10:15", "2014/12/30 21:10"),
    ("2014/12/31 10:00", "2014/12/31 18:30"),
    ("2015/1/4 10:45", "2015/1/4 19:40"),
    ("2015/1/5 9:58", "2015/1/5 20:30"),
    ("2015/1/6 10:14", "2015/1/6 20:24"),
    ("2015/1/7 10:00", "2015/1/7 20:30"),
    ("2015/1/8 9:50", "2015/1/8 20:00"),
    ("2015/1/9 9:50", "2015/1/9 18:30"),
    ("2015/1/13 9:30", "2015/1/13 19:40"),
    ("2015/1/14 10:10", "2015/1/14 19:10"),
    ("2015/1/15 9:55", "2015/1/15 19:00"),
    ("2015/1/16 10:00", "2015/1/16 18:30"),
    ("2015/1/17 10:25", "2015/1/17 18:30"),
    ("2015/1/18 10:30", "2015/1/18 18:30"),
    ("2015/1/19 10:00", "2015/1/19 18:40"),
    ("2015/1/20 10:00", "2015/1/20 19:00"),
    ("2015/1/21 10:35", "2015/1/21 19:20"),
    ("2015/1/22 9:55", "2015/1/22 19:00"),
    ("2015/1/23 10:10", "2015/1/23 19:30"),
    ("2015/1/26 10:30", "2015/1/26 20:15"),
    ("2015/1/27 10:20", "2015/1/27 20:00"),
    ("2015/1/28 10:30", "2015/1/28 20:10"),
    ("2015/1/29 10:27", "2015/1/29 21:10"),
    ("2015/1/30 9:55", "2015/1/30 18:45"),
    ("2015/1/31 13:30", "2015/1/31 18:45"),
    ("2015/2/2 10:23", "2015/2/2 20:25"),
    ("2015/2/3 10:15", "2015/2/3 20:10"),
    ("2015/2/4 10:15", "2015/2/4 20:30"),
    ("2015/2/5 10:02", "2015/2/5 20:45"),
    ("2015/2/6 10:02", "2015/2/6 18:30"),
    ("2015/2/7 16:40", "2015/2/7 19:30"),
    ("2015/2/8 16:00", "2015/2/8 20:30"),
    ("2015/2/9 15:10", "2015/2/9 20:15"),
    ("2015/2/10 10:15", "2015/2/10 20:20"),
    ("2015/2/11 10:29", "2015/2/11 13:20"),
    ("2015/2/11 14:20", "2015/2/11 21:40"),
    ("2015/2/12 10:05", "2015/2/12 19:05"),
    ("2015/2/13 10:15", "2015/2/13 18:30"),
    ("2015/2/14 10:40", "2015/2/14 18:30"),
    ("2015/2/24 10:12", "2015/2/24 19:00"),
    ("2015/2/25 10:15", "2015/2/25 20:40"),
    ("2015/2/26 10:12", "2015/2/26 18:40"),
    ("2015/2/27 9:27", "2015/2/27 18:35"),
    ("2015/2/28 9:35", "2015/2/28 13:30"),
    ("2015/3/2 9:30", "2015/3/2 18:40"),
    ("2015/3/3 9:30", "2015/3/3 18:40"),
    ("2015/3/4 10:00", "2015/3/4 19:30"),
    ("2015/3/5 10:20", "2015/3/5 18:30"),
    ("2015/3/6 9:30", "2015/3/6 18:30"),
    ("2015/3/7 9:40", "2015/3/7 18:30"),
    ("2015/3/9 8:55", "2015/3/9 18:40"),
    ("2015/3/10 8:55", "2015/3/10 18:40"),
    ("2015/3/11 8:40", "2015/3/11 18:35"),
    ("2015/3/12 8:39", "2015/3/12 18:35"),
    ("2015/3/16 8:55", "2015/3/16 9:00"),
    ("2015/3/16 10:30", "2015/3/16 18:40"),
    ("2015/3/17 8:55", "2015/3/17 18:35"),
    ("2015/3/18 9:01", "2015/3/18 18:35"),
    ("2015/3/19 8:55", "2015/3/19 18:50"),
    ("2015/3/20 8:55", "2015/3/20 18:30"),
    ("2015/3/21 9:50", "2015/3/21 12:20"),
    ("2015/3/23 8:40", "2015/3/23 18:30"),
    ("2015/3/24 8:40", "2015/3/24 18:45"),
    ("2015/3/25 8:55", "2015/3/25 18:45"),
    ("2015/3/26 8:10", "2015/3/26 18:40"),
    ("2015/3/27 8:40", "2015/3/27 18:30"),
    ("2015/3/28 9:45", "2015/3/28 17:40"),
    ("2015/3/30 9:02", "2015/3/30 18:36"),
    ("2015/3/31 9:10", "2015/3/31 18:40"),
    ("2015/4/1 8:55", "2015/4/1 18:40"),
    ("2015/4/2 8:55", "2015/4/2 18:35"),
    ("2015/4/3 9:25", "2015/4/3 18:45"),
    ("2015/4/4 9:50", "2015/4/4 17:50"),
    ("2015/4/7 9:26", "2015/4/7 18:40"),
    ("2015/4/8 8:55", "2015/4/8 18:35"),
    ("2015/4/9 8:55", "2015/4/9 18:35"),
    ("2015/4/10 8:56", "2015/4/10 18:30"),
    ("2015/4/13 8:52", "2015/4/13 18:35"),
    ("2015/4/14 9:29", "2015/4/14 18:35"),
    ("2015/4/15 9:00", "2015/4/15 18:35"),
    ("2015/4/16 8:58", "2015/4/16 18:40"),
    ("2015/4/17 8:59", "2015/4/17 18:40"),
    ("2015/4/18 13:30", "2015/4/18 18:30"),
    ("2015/4/20 8:55", "2015/4/20 18:45"),
    ("2015/4/21 9:15", "2015/4/21 22:36"),
    ("2015/4/22 9:15", "2015/4/22 18:33"),
    ("2015/4/23 8:50", "2015/4/23 18:40"),
    ("2015/4/24 8:40", "2015/4/24 18:35"),
    ("2015/4/27 9:01", "2015/4/27 18:30"),
    ("2015/4/28 8:55", "2015/4/28 18:36"),
    ("2015/4/29 9:09", "2015/4/29 18:35"),
    ("2015/4/30 8:50", "2015/4/30 12:30"),
    ("2015/5/4 8:55", "2015/5/4 18:50"),
    ("2015/5/5 13:15", "2015/5/5 18:45"),
    ("2015/5/6 9:25", "2015/5/6 18:40"),
    ("2015/5/7 8:57", "2015/5/7 18:40"),
    ("2015/5/8 8:58", "2015/5/8 20:00"),
    ("2015/5/9 9:45", "2015/5/9 19:15"),
    ("2015/5/11 9:05", "2015/5/11 18:30"),
    ("2015/5/12 9:15", "2015/5/12 18:50"),
    ("2015/5/13 9:10", "2015/5/13 19:00"),
    ("2015/5/14 8:58", "2015/5/14 18:50"),
    ("2015/5/15 8:54", "2015/5/15 19:00"),
    ("2015/5/18 9:15", "2015/5/18 19:06"),
    ("2015/5/19 12:50", "2015/5/19 19:00"),
    ("2015/5/20 9:15", "2015/5/20 18:35"),
    ("2015/5/21 9:10", "2015/5/21 18:32"),
    ("2015/5/22 9:28", "2015/5/22 18:55"),
    ("2015/5/25 9:00", "2015/5/25 18:30"),
    ("2015/5/26 9:01", "2015/5/26 18:35"),
    ("2015/5/27 9:24", "2015/5/27 18:35"),
    ("2015/5/28 9:09", "2015/5/28 18:35"),
    ("2015/5/29 8:58", "2015/5/29 18:40"),
    ("2015/6/1 9:19", "2015/6/1 18:50"),
    ("2015/6/2 9:09", "2015/6/2 18:15"),
    ("2015/6/3 9:26", "2015/6/3 18:40"),
    ("2015/6/4 12:58", "2015/6/4 18:30"),
    ("2015/6/5 12:56", "2015/6/5 18:40"),
    ("2015/6/8 9:16", "2015/6/8 18:40"),
    ("2015/6/9 13:10", "2015/6/9 18:30"),
    ("2015/6/10 9:28", "2015/6/10 18:43"),
    ("2015/6/11 9:45", "2015/6/11 18:40"),
    ("2015/6/12 13:15", "2015/6/12 18:36"),
    ("2015/6/15 9:30", "2015/6/15 18:30"),  # ?
    ("2015/6/16 9:15", "2015/6/16 18:17"),
    ("2015/6/17 9:30", "2015/6/17 18:30"),  # ?
    ("2015/6/23 9:14", "2015/6/23 18:30"),
    ("2015/6/24 9:35", "2015/6/24 18:30"),
    ("2015/6/25 9:24", "2015/6/25 18:30"),
    ("2015/6/26 11:40", "2015/6/26 18:51"),
    ("2015/6/29 9:23", "2015/6/29 18:30"),
    ("2015/6/30 9:24", "2015/6/30 18:40"),
]


def minutes2Str(minutes):
    return str(int(minutes / 60)) + ":" + str(minutes % 60)

total_working_hour = 0
total_working_minute = 0
overtime_days = 0
for (t1, t2) in times:
    time1 = datetime.datetime.strptime(t1, "%Y/%m/%d %H:%M")
    time2 = datetime.datetime.strptime(t2, "%Y/%m/%d %H:%M")
    if time1.day != time2.day or time1.month != time2.month:
        cit.err(datetime.datetime.strftime(time1, "%Y/%m/%d %H:%M") + "is not same day!")
    workingTime = (time2.hour * 60 + time2.minute) - (time1.hour * 60 + time1.minute)
    cit.info(str(t1) + "\t" + str(t2) + "  \t" + minutes2Str(workingTime))
    total_working_minute += workingTime
    if workingTime > 9 * 60:
        overtime_days += 1
total_working_hour = int(total_working_minute / 60)
actualWorkingDays = len(times)
total_days = 265
legalVacation = int(total_days / 7) * 2 - 1 + 1 + 3 + 1 + 1 + 0.5 + 1
# 2014.10.11 十一蹿休
# 2015.1.1 元旦
# 2015.18/19/20 春节
# 2015.4.5 清明
# 2015.5.1 劳动节
# 2015.5.4 青年节
# 2015.6.20 端午
workDays = total_days - legalVacation
cit.title("Conclusions")
cit.info("{0}\t| Actually working {0} days".format(str(actualWorkingDays)))
cit.info("{0}\t| Legal workday is {0} days".format(str(workDays)))
cit.info("{0}\t| additional workdays {0} days".format(str(actualWorkingDays - workDays)))
cit.info("{0}\t| Working more than 8+1 hours for {0} days ({1}%)".format(str(overtime_days), str(round(100 * overtime_days / actualWorkingDays, ndigits=2))))
cit.info("{0}\t| Total working {0} hours ({1} days)".format(str(total_working_hour), str(round(total_working_hour / 24, ndigits=2))))
cit.info("{0}\t| Working {0} hours per day".format(round(total_working_hour / actualWorkingDays, ndigits=2)))
cit.info("{0}\t| Working {0} hours per work day".format(round(total_working_hour / workDays, ndigits=2)))
cit.pause()
