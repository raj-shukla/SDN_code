import math
import csv
from operator import itemgetter
import random
import statistics
import copy
import time
import simulation_data

chargingTimeSimulation = []
unallocatedVehiclesSimulation = []
chargingTimeMinDistance = []
unallocatedVehiclesMinDistance  = []


def Simulation (simulationData) :
#{
    vehicles = simulationData[0]
    stations = simulationData[1]
    schedules = simulationData[2]
    SOCr = simulationData[3][:vehicles]
    SOCt = simulationData[4][:vehicles]
    SOCc = simulationData[5][:vehicles]
    location = simulationData[6][:vehicles]
    requestTime = simulationData[7][:vehicles]
    speed = simulationData[8][:vehicles]
    dischargeRate = simulationData[9][:vehicles]
    direction = simulationData[10][:vehicles]
    stationLocation = simulationData[11][:stations]
    waitTime = simulationData[12][:stations]
    chargingRate = simulationData[13][:stations]
    powerAvailable = simulationData[14][:stations]
    busImpedance = simulationData[15][:stations]
    potentialStations = []
    chargingTime = []
    listToCompare = []
    travelTimeList = []
    stationAssigned = []
    
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

    tmpList = []

    for i, value in enumerate(chargingTime):
    #{
        tmpList.append((i, len(chargingTime[i]), sorted( list(zip(chargingTime[i], potentialStations[i])))  ))
        sortedChargingTime = sorted(tmpList, key= itemgetter(1))
    #}

    def SortChargingTime(sortedChargingTime) :
    #{
        tmpList = []
        for i, value in enumerate(sortedChargingTime):
        #{
            if(sortedChargingTime[i][2] != []):
            #{
                sortedChargingTime[i][2].sort()
            #}
        #}
    #}



    for i, val in enumerate(sortedChargingTime) :
    #{
        print(sortedChargingTime[i])
    #}

    n = 3
    m = 5

    positionCount = []

    for i in range(0, n) :
    #{
        positionCount.append([])
        for j in range(0, m):
        #{
            positionCount[i].append(0)
        #}
    #}


    def FindPositionCount(vehicleIndex, stationIndex, sortedChargingTime) :
    #{
        stationID = sortedChargingTime[vehicleIndex][2][stationIndex][1]
        chargingTimeToCompare =  sortedChargingTime[vehicleIndex][2][stationIndex][0]
        vehicleToAllocate = sortedChargingTime[vehicleIndex][0]

        for i, val in enumerate(listToCompare[vehicleToAllocate]) :
        #{
            if(val[1] == stationID):
            #{
                requestTime = val[2]
                travelTime = val[3]
                waitTime = val[4]
                chargeTime = val[5]
            #}
        
        for i in range(0, m) :
            #{
            for j in range(vehicleIndex + 1, len(sortedChargingTime)) :
            #{
                indexToCompare = sortedChargingTime[j][0]
                if (i >= len(sortedChargingTime[j][2])) :
                #{
                    continue
                #}
                if(sortedChargingTime[j][2][i][1] == stationID) :
                #{
                    for k, val in enumerate(listToCompare[indexToCompare]) :
                    #{
                        if (val[1] == stationID) :
                        #{
                            if(requestTime + travelTime < val[2] + val[3] < requestTime + travelTime + waitTime + chargeTime) :
                            #{
                                positionCount[stationIndex][i] = positionCount[stationIndex][i] + 1
                            #}
                        #}
                    #}
                    #{
                        positionCount[stationIndex][i] = positionCount[stationIndex][i] + 1
                    #}
                #}
                  
            #}
        #}
    #}


    def ClearPositionCount(positionCount) :
    #{
        for i in range(0, n) :
        #{

            for j in range(0, m):
            #{
                 positionCount[i][j] = 0
            #}
        #}
    #}



    assignedStations = []
    listForAverage = []

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
            if ( stationID in [value[1] for j, value in enumerate(sortedChargingTime[i][2])] ) :
            #{
                indexToUpdate =  [j for j, value in enumerate(sortedChargingTime[i][2]) if value[1] == stationID][0]
                for iteration, val in enumerate(listToCompare[index]) :
                #{
                    if (val[1] == stationID) :
                    #{
                        if(requestTime[vehicleAllocated] + travelTime < val[2] + val[3] < requestTime[vehicleAllocated] + travelTime + waitTime + chargeTime ) :
                        #{
                            tmpListToUpdate = list(sortedChargingTime[i][2][indexToUpdate])
                            tmpListToUpdate[0] = sortedChargingTime[i][2][indexToUpdate][0] +  requestTime[vehicleAllocated] + travelTime + waitTime + chargeTime  - val[2] - val[3]
                            sortedChargingTime[i][2][indexToUpdate] = tuple(tmpListToUpdate)
                        #}
                    #}
                #}
            #}
        #}
    #}

    def FindFirstElementTime(sortedChargingTime, index, stationID) :
    #{
        timeFirstElement = 0
        for i in range(index + 1, len(sortedChargingTime) - 1) :
        #{
            if(sortedChargingTime[i][2] != []) :
            #{
                if (sortedChargingTime[i][2][0][1] == stationID ) :
                #{
                    timeFirstElement = timeFirstElement + sortedChargingTime[i][2][0][0]
                #}
            #}
        #}
        return timeFirstElement
    #}
    tmpList = []
    for i, val in enumerate(sortedChargingTime) :
    #{
        if (sortedChargingTime[i][2] != []) :
        #{
            tmpVehicleAllocated = sortedChargingTime[i][0]
            tmpStationID = sortedChargingTime[i][2][0][1]
            tmpTimeToCharge = sortedChargingTime[i][2][0][0]
            for j, value in enumerate(sortedChargingTime[i][2]) :
            #{
                tmpList = copy.deepcopy(sortedChargingTime)
                diff1 = FindFirstElementTime(sortedChargingTime, i, sortedChargingTime[i][2][j][1])
                UpdateWaitingTime(i, tmpVehicleAllocated, tmpStationID, tmpTimeToCharge )
                diff2 = FindFirstElementTime(sortedChargingTime, i, sortedChargingTime[i][2][j][1])
                tmpDiff1 = diff2 - diff1
                sortedChargingTime = tmpList
                for k in range(j+1, len(sortedChargingTime[i][2]) - 2 ):
                #{
                    tmpList = copy.deepcopy(sortedChargingTime)
                    diff3 = FindFirstElementTime(sortedChargingTime, i, sortedChargingTime[i][2][k][1])
                    UpdateWaitingTime(i, tmpVehicleAllocated, sortedChargingTime[i][2][k][1], sortedChargingTime[i][2][k][0] )
                    diff4 = FindFirstElementTime(sortedChargingTime, i, sortedChargingTime[i][2][k][1])
                    sortedChargingTime = tmpList
                    tmpDiff2 = diff4 - diff3
                    diff5 = sortedChargingTime[i][2][k][0] - sortedChargingTime[i][2][j][0]
                    if(tmpDiff1 > diff5 and tmpDiff1 > tmpDiff2) :
                    #{
                        tmpStationID = sortedChargingTime[i][2][k][1]
                        tmpTimeToCharge = sortedChargingTime[i][2][k][0]
                        tmpDiff1 = tmpDiff2
                    #}
                #}
            #}
            vehicleAllocated = sortedChargingTime[i][0]
            stationID = tmpStationID
            timeToCharge = tmpTimeToCharge
            assignedStations.append((vehicleAllocated, timeToCharge, stationID))
            UpdateWaitingTime(i, vehicleAllocated, stationID, timeToCharge)
        #}
        SortChargingTime(sortedChargingTime)
    #}
        
    for i, val in enumerate (assignedStations) :
    #{
        listForAverage.append(val[1])
    #}

    averageChargingTime = statistics.mean(listForAverage)
    unallocatedVehicles = potentialStations.count([])


    print(assignedStations)
    for i, val in enumerate(sortedChargingTime) :
    #{
        print(sortedChargingTime[i])
    #}

    print(assignedStations)
    print(averageChargingTime)
    print(unallocatedVehicles)
    chargingTimeSimulation.append(averageChargingTime)
    unallocatedVehiclesSimulation.append(unallocatedVehicles)
    #}
#}


def SimulationMinDistance(simulationData) :
#{
    vehicles = simulationData[0]
    stations = simulationData[1]
    schedules = simulationData[2]
    SOCr = simulationData[3][:vehicles]
    SOCt = simulationData[4][:vehicles]
    SOCc = simulationData[5][:vehicles]
    location = simulationData[6][:vehicles]
    requestTime = simulationData[7][:vehicles]
    speed = simulationData[8][:vehicles]
    dischargeRate = simulationData[9][:vehicles]
    direction = simulationData[10][:vehicles]
    stationLocation = simulationData[11][:stations]
    waitTime = simulationData[12][:stations]
    chargingRate = simulationData[13][:stations]
    powerAvailable = simulationData[14][:stations]
    busImpedance = simulationData[15][:stations]
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
    chargingTimeMinDistance.append(averageChargingTime)
    unallocatedVehiclesMinDistance.append(unallocatedVehicles)

#}

runTime = []
meanValues = [[], [], [], [], [], []]

vehicles = 200
stations = 0
for i in range(0, 10):
#{
    stations = stations + 5
    variableParameter = stations
    for j in range(0, 10):
    #{
        startTime = time.time()
        simulationData = simulation_data.SimulationData()
        simulationData[0] = vehicles
        simulationData[1] = stations
        Simulation(simulationData)
        endTime = time.time()
        runTime.append(endTime - startTime)
        SimulationMinDistance(simulationData) 
    #}
    meanValues[0].append(variableParameter)
    meanValues[1].append(statistics.mean(chargingTimeSimulation))
    meanValues[2].append(statistics.mean(chargingTimeMinDistance))
    meanValues[3].append(statistics.mean(unallocatedVehiclesSimulation))
    meanValues[4].append(statistics.mean(unallocatedVehiclesMinDistance))
    meanValues[5].append(statistics.mean(runTime))
    print(chargingTimeSimulation)
    print(chargingTimeMinDistance)
    print(unallocatedVehiclesSimulation)
    print(unallocatedVehiclesMinDistance)
    print(runTime)
    chargingTimeSimulation.clear()
    chargingTimeMinDistance.clear()
    unallocatedVehiclesSimulation.clear()
    unallocatedVehiclesMinDistance.clear()
    runTime.clear()
#}

print(meanValues)

with open("outputStationsTime.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(meanValues)


'''
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

assignedStations = []
listForAverage = []
for i, val in enumerate(sortedChargingTime):
#{
    if (sortedChargingTime[i][2] != []) :
    #{
        timeToCharge = min((sortedChargingTime[i][2]))
        index = sortedChargingTime[i][2].index(min(sortedChargingTime[i][2]))
        vehicleAllocated = sortedChargingTime[i][0]
        stationID = sortedChargingTime[i][3][index]
        assignedStations.append((vehicleAllocated,  timeToCharge, stationID))
        UpdateWaitingTime(i, vehicleAllocated,  stationID, timeToCharge)
    #}
#}
for i, val in enumerate(sortedChargingTime) :
#{
    print(sortedChargingTime[i])
#}
    

for i, val in enumerate (assignedStations) :
#{
    listForAverage.append(val[1])
#}

averageChargingTime = statistics.mean(listForAverage)
unallocatedVehicles = potentialStations.count([])


print(assignedStations)
print(averageChargingTime)
print(unallocatedVehicles)
'''


