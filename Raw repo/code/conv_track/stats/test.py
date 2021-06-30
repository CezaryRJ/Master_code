import datetime


def time_to_day(inn):

    out = int(inn[0])/24#hours

    if inn[1][0] == "0":#minutes
        out = out + int(inn[1][1])/24/60
    else:
        out = out +  int(inn[1])/24/60

    if inn[2][0] == "0":#minutes
        out = out +  int(inn[1][1])/24/60/60
    else:
        out = out +  int(inn[1])/24/60/60

    return out



def delta_to_days(delta):

    #print(delta)

    tmp = str(delta).split(" days, ")

    if len(tmp) == 1:
        return time_to_day(tmp[0].split(":"))
    else:
        return int(tmp[0]) + time_to_day(tmp[1].split(":"))






start = datetime.datetime(1000)
end   = datetime.datetime(2020,2,1,23,34)
delta = end-start

print(delta)

print(delta_to_days(delta))
