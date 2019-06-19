for y in range(2005,2009):
    for m in range(1,13):
        if m in (1,3,5,7,8,10,12):
            d = 31
        elif m in (4,6,9,11):
            d = 30
        elif m == 2:
            if y%4 == 0:
                if y%100 == 0 and y%400 != 0:
                    d = 28
                else:
                    d = 29
            else:
                d = 28
        if m < 10:
            date = str(y)+"-0"+str(m)+"-01/to/"+str(y)+"-0"+str(m)+"-"+str(d)
            filename = "ERAinterim_"+str(y)+"_0"+str(m)+"_slp.nc"
        else:
            date = str(y)+"-"+str(m)+"-01/to/"+str(y)+"-"+str(m)+"-"+str(d)
            filename = "ERAinterim_"+str(y)+"_"+str(m)+"_slp.nc"
        print "Now retriving..."+date

        from ecmwfapi import ECMWFDataServer
        server = ECMWFDataServer()
        server.retrieve({
            "class": "ei",
            "dataset": "interim",
            "date": date,
            "expver": "1",
            "grid": "0.75/0.75",
            "levtype": "sfc",
            "param": "151",
            "step": "0",
            "stream": "oper",
            "time": "00:00:00/06:00:00/12:00:00/18:00:00",
            "type": "an",
            "area": "90/0/-90/360",
            "format": "netcdf",
            "target": filename,
        })

        # server.retrieve({
        #     # "class": "ei",
        #     # "dataset": "interim",
        #     # "date": date,
        #     # "expver": "1",
        #     # "grid": "0.75/0.75",
        #     # "levtype": "pl",
        #     # "levelist": "850",
        #     # "param": "138",
        #     # "step": "0",
        #     # "stream": "oper",
        #     # "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        #     # "type": "an",
        #     # "area": "90/0/-90/360",
        #     # "format": "netcdf",
        #     # "target": filename,
        # })

	print "Wrote data to..."+filename
