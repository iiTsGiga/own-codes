# convert time to minutes -> e.g. '10:30' to 630
def convert_time(time: str):
    t = time.split(":")
    return (int(t[0]) * 60) + int(t[1])


# get available, valid (in terms of duration) times
def get_available_times(meetings, timeRange, duration) -> []:
    availableTimes = []

    # check for free and valid time between timeranges start and first meetings start
    startTime = convert_time(timeRange[0])
    endTime = convert_time(meetings[0][0])
    if endTime - startTime >= duration:
        availableTimes.append([startTime, endTime])

    # check for free and valid times between meetings
    for i in range(len(meetings) - 1):
        startTime = convert_time(meetings[i][1])
        endTime = convert_time(meetings[i + 1][0])
        if endTime - startTime >= duration:
            availableTimes.append([startTime, endTime])

    # check for free and valid time between last meeting end and timerange end
    startTime = convert_time(meetings[len(meetings) - 1][1])
    endTime = convert_time(timeRange[1])
    if endTime - startTime >= duration:
        availableTimes.append([startTime, endTime])

    # return array of available times in format:
    # e.g. [[630, 690], [720, 730]] <- (10:30 to 11:30) and (12:00 to 12:10)
    return availableTimes


# convert minutes to time -> e.g. 630 to '10:30'
def convert_minutes(time: int) -> str:
    return str(int(time / 60)) + ":" + str(int(time % 60)).format('00:00')


# get all available bookingtimes
def get_bookings(meetings1, timeRange1, meetings2, timeRange2, meetingDuration) -> []:
    # convert and filter available times of each individual
	availableTimes1 = get_available_times(meetings1, timeRange1, meetingDuration)
    availableTimes2 = get_available_times(meetings2, timeRange2, meetingDuration)

	# check for available times in both individuals schedules
    available = []
    for t1 in range(len(availableTimes1)):
        for t2 in range(len(availableTimes2)):
            latestStartTime = max(availableTimes1[t1][0], availableTimes2[t2][0])
            earliestEndTime = min(availableTimes1[t1][1], availableTimes2[t2][1])
            if earliestEndTime - latestStartTime >= meetingDuration:
                available.append([convert_minutes(latestStartTime), convert_minutes(earliestEndTime)])

    return available


# example from the google interview: https://www.youtube.com/watch?v=3Q_oYDQ2whs
m1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
tr1 = ['9:00', '20:00']
m2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
tr2 = ['10:00', '18:30']
d = 30
print(get_bookings(m1, tr1, m2, tr2, d))
