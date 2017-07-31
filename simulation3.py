from csv import reader
from math import exp
from operator import itemgetter
import random
import statistics
import simulation_data

vehicles = simulation_data.vehicles
stations = simulation_data.stations
schedules = 96
SOCr = simulation_data.SOCr[:vehicles]
SOCt = simulation_data.SOCt[:vehicles]
SOCc = simulation_data.SOCc[:vehicles]
location = simulation_data.location[:vehicles]
requestTime = simulation_data.requestTime[:vehicles]
speed = simulation_data.speed[:vehicles]
dischargeRate = simulation_data.dischargeRate[:vehicles]
direction = simulation_data.direction[:vehicles]
stationLocation = simulation_data.stationLocation[:stations]
waitTime = simulation_data.waitTime[:stations]
chargingRate = simulation_data.chargingRate[:stations]
powerAvailable = simulation_data.powerAvailable[:stations]
busImpedance = simulation_data.busImpedance[:stations]
potentialStations = []
chargingTime = []
listToCompare = []

stationLocation.sort()

for i in range(0, vehicles):
#{
    potentialStations.append([])
    chargingTime.append([])
    listToCompare.append([])
#}

dth = []

def FindSlot(requestTime) :
#{
    slot = int(requestTime/15)
    return slot
#}


for i in range(0, vehicles):
#{
    dth.append((SOCc[i] - SOCt[i])/dischargeRate[i])
    for iteration, val in enumerate(stationLocation):
    #{
        if (direction[i] == 1):
        #{
            if ( val > location[i] and val < location[i] + dth[i] ) :
            #{
                potentialStations[i].append(iteration)
            #}
        #}
        else :
        #{
            if ( val < location[i] and  val > location[i] - dth[i]) :
            #{
                potentialStations[i].append(iteration)
            #}
        #}
    #}
    for index, value  in enumerate(potentialStations[i]) :
    #{
        travelTime = (abs(stationLocation[value] - location[i]))/speed[i]        
        slot = FindSlot(requestTime[i] + travelTime)
        waitAtStation = waitTime[value][slot]
        chargeTime = (SOCr[i] - (SOCc[i] -(abs(stationLocation[value] - location[i]))*dischargeRate[i] ))/chargingRate[value]
        chargingTime[i].append(waitAtStation + chargeTime)
        listToCompare[i].append((i, value, requestTime[i],  travelTime, waitAtStation, chargeTime))
    #}
#}

print(potentialStations)

tmpList = []

for i, value in enumerate(chargingTime):
#{
    tmpList.append((i, len(chargingTime[i]), chargingTime[i], potentialStations[i]))
#}

sortedChargingTime = sorted(tmpList, key= itemgetter(1))

for i, val in enumerate(sortedChargingTime) :
#{
    print(sortedChargingTime[i])
#}


def UpdateWaitingTime(listIndexAllocated, vehicleAllocated, stationID, timeToCharge) :
#{
    for i, val in enumerate(listToCompare[vehicleAllocated]) :
    #{
        if(val[1] == stationID):
        #{
            travelTime = val[3]
            waitTime = val[4]
            chargeTime = val[5]
        #}
    #}
    for i in range (listIndexAllocated +1, len(sortedChargingTime)) :
    #{
        index = sortedChargingTime[i][0]
        if (stationID in sortedChargingTime[i][3] ) :
        #{
            for iteration, val in enumerate(listToCompare[index]) :
            #{
                if (val[1] == stationID) :
                #{
                    if(requestTime[vehicleAllocated] + travelTime < val[2] + val[3] < requestTime[vehicleAllocated] + travelTime + waitTime + chargeTime ) :
                    #{
                        sortedChargingTime[i][2][sortedChargingTime[i][3].index(stationID)] = sortedChargingTime[i][2][sortedChargingTime[i][3].index(stationID)] +  (requestTime[vehicleAllocated] + travelTime + waitTime + chargeTime  - val[2] - val[3] )
                    #}
                #}
            #}
        #}
    #}
#}

assignedStation = []
listForAverage = []
for i, val in enumerate(sortedChargingTime):
#{
    if (sortedChargingTime[i][2] != []) :
    #{
        timeToCharge = min((sortedChargingTime[i][2]))
        index = sortedChargingTime[i][2].index(min(sortedChargingTime[i][2]))
        vehicleAllocated = sortedChargingTime[i][0]
        stationID = sortedChargingTime[i][3][index]
        assignedStation.append((vehicleAllocated,  timeToCharge, stationID))
        UpdateWaitingTime(i, vehicleAllocated,  stationID, timeToCharge)
    #}
#}
for i, val in enumerate(sortedChargingTime) :
#{
    print(sortedChargingTime[i])
#}
    

for i, val in enumerate (assignedStation) :
#{
    listForAverage.append(val[1])
#}

averageChargingTime = statistics.mean(listForAverage)
unallocatedVehicles = potentialStations.count([])


print(assignedStation)
print(averageChargingTime)
print(unallocatedVehicles)



