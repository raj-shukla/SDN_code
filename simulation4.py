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
travelTimeList = []
stationAssigned = []

stationLocation.sort()

for i in range(0, vehicles):
#{
    potentialStations.append([])
    chargingTime.append([])
    listToCompare.append([])
    travelTimeList.append([])
    stationAssigned.append([])
#}

dth = []

stationLocation.sort()

for i in range (0, stations) :
#{    
    for j in range (0, schedules):
    #{
        waitTime[i].append(random.randrange(5, 10))
        powerAvailable[i].append(random.randrange(50, 100))
    #}
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
        travelTimeList[i].append((value, travelTime))
        waitAtStation = waitTime[value][slot]
        chargeTime = (SOCr[i] - (SOCc[i] -(abs(stationLocation[value] - location[i]))*dischargeRate[i] ))/chargingRate[value]
        chargingTime[i].append(travelTime + waitAtStation + chargeTime)
        travelTimeList[i].append((value, travelTime))
        listToCompare[i].append((i, value, requestTime[i],  travelTime, waitAtStation, chargeTime))
    #}
#}


def UpdateWaitingTime(listIndexAllocated, vehicleAllocated, stationID, travelTime, waitingTime, chargeTime) :
#{
    for i in range(listIndexAllocated + 1, len(listToCompare)) :
    #{
        for j, val in enumerate(listToCompare[i]) :
        #{
            if (val[1] == stationID) :
            #{
                if (requestTime[vehicleAllocated] + travelTime < val[2] + val[3] < requestTime[vehicleAllocated] + travelTime + waitingTime + chargeTime) :
                #{
                    tmpList = list(listToCompare[i][j])
                    tmpList[4] = listToCompare[i][j][4] + requestTime[vehicleAllocated] + travelTime + waitingTime + chargeTime - val[2] -  val[3]
                    listToCompare[i][j] = tuple(tmpList)
                #}
            #}
        #}
    #}
#}
 
AssignedStations = []
listForAverage = []
for i in range(0, vehicles) :
#{
    if(travelTimeList[i] != []) :
    #{
        vehicleAllocated = i
        stationAssigned[i].append(min(listToCompare[i], key= lambda x: x[3]))
        stationID = stationAssigned[i][0][1]
        travelTime = stationAssigned[i][0][3]
        waitingTime = stationAssigned[i][0][4]
        chargeTime = stationAssigned[i][0][5]
        AssignedStations.append((i, stationID, travelTime, waitingTime, chargeTime))
        UpdateWaitingTime(i, vehicleAllocated,  stationID, travelTime, waitingTime, chargeTime)
    #}
#}
        
print(potentialStations)



for i, val in enumerate (AssignedStations) :
#{    
    listForAverage.append(val[3] + val[4])
#}

averageChargingTime = statistics.mean(listForAverage)
unallocatedVehicles = potentialStations.count([])

print(AssignedStations)
print(averageChargingTime)
print(unallocatedVehicles)










