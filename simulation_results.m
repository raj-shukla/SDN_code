vehicles = [50,100,150,200,250,300,350,400,450,500]
stations = [5,10,15,20,25,30,35,40,45,50]

chargeTimeSubOptimalVehiclesRandomDistribution= [19.25294238,23.33375474,28.16416492,33.55484014,39.21678655,42.75729898,48.62000388,53.77243806,60.96583817,65.94201471]
chargeTimeMinDistanceVehiclesRandomDistribution = [27.75581288,51.14257269,83.58677576,118.0427538,141.6397228,163.964295,274.4675496,461.4110561,677.4241339,1079.143067]
requestNotMetVehiclesRandomDistribution = [15,30,47,65,79,100,117,135,145,163]

chargeTimeSubOptimalStationsRandomDistribution = [82.64215782,63.98856968,50.79414785,33.55484014,31.15597298,26.9972147,25.71220692,23.31874582,22.75079637,20.48532951]
chargeTimeMinDistanceStationsRandomDistribution = [799.5606868,576.4155796,487.8984549,118.0427538,118.9859505,107.7756303,157.5818159,86.32421978,70.13414966,63.65305055]
requestNotMetStationsRandomDistribution = [115,102,91,65,47,46,43,34,33,33]

chargeTimeSubOptimalVehiclesUniformDistribution = [32.16045326,43.74141334,52.60380054,64.48203046,73.78557333,84.60828084,96.24084182,106.747003,117.6862182,130.6750749]
chargeTimeMinDistanceVehiclesUniformDistribution = [34.55994853,93.54351372,196.7331286,311.3374561,593.3154689,1324.872334,2011.431248,5662.944532,13764.51566,30551.04051]
requestNotMetVehiclesUniformDistribution = [13,23,35,48,57,67,78,95,107,119]

chargeTimeSubOptimalStationsUniformDistribution = [90.2663543,64.48203046,66.44092429,42.60462961,34.56993655,30.28248175,26.71612992,24.51194908,22.32869511,21.20111057]
chargeTimeMinDistanceStationsUniformDistribution = [875.9044888,311.3374561,313.2553554,125.6523161,88.7355077,73.27630402,63.3122875,63.71937547,57.71496524,49.77869266]
requestNotMetStationsUniformDistribution = [98,48,25,14,5,8,5,5,4,3]

figure;
plot(vehicles, chargeTimeSubOptimalVehiclesRandomDistribution,  'r^-',  vehicles, chargeTimeMinDistanceVehiclesRandomDistribution, 'mo-' )
legend('Sub-optimal ', 'Minimum distance')
xlabel('Number of vehicles')
ylabel('Charging time (min)')
%axis([0 20  0 5])


figure;
plot(stations, chargeTimeSubOptimalStationsRandomDistribution,  'r^-',  stations, chargeTimeMinDistanceStationsRandomDistribution, 'mo-' )
legend('Sub-optimal ', 'Minimum distance')
xlabel('Number of charging stations')
ylabel('Charging time (min)')
%axis([0 20  0 5])


figure;
plot(vehicles, RequestNotMetVehiclesRandomDistribution,  'r^-',  vehicles, requestNotMetVehiclesUniformDistribution, 'mo-' )
legend('Random', 'Uniform')
xlabel('Number of vehicles')
ylabel('Number of requests not satisfied')
%axis([0 20  0 5])

figure;
plot(stations, RequestNotMetStationsRandomDistribution,  'r^-',  stations, requestNotMetStationsUniformDistribution, 'mo-' )
legend('Random', 'Uniform')
xlabel('Number of charging stations')
ylabel('Number of requests not satisfied')
%axis([0 20  0 5])
figure
plot(vehicles, chargeTimeSubOptimalVehiclesUniformDistribution,  'r^-',  vehicles, chargeTimeMinDistanceVehiclesUniformDistribution, 'mo-' )
legend('Sub-optimal ', 'Minimum distance')
xlabel('Number of vehicles')
ylabel('Charging time (min)')
%axis([0 20  0 5])

figure;
plot(stations, chargeTimeSubOptimalStationsUniformDistribution,  'r^-',  stations, chargeTimeMinDistanceStationsUniformDistribution, 'mo-' )
legend('Sub-optimal ', 'Minimum distance')
xlabel('Number of charging stations')
ylabel('Charging time (min)')
%axis([0 20  0 5])


figure;
plot(vehicles, chargeTimeSubOptimalVehiclesRandomDistribution,  'r^-',  vehicles, chargeTimeSubOptimalVehiclesUniformDistribution, 'mo-' )
legend('Random ', 'Uniform')
xlabel('Number of vehicles')
ylabel('Charging time (min)')
%axis([0 20  0 5])



figure;
plot(vehicles, chargeTimeSubOptimalStationsRandomDistribution,  'r^-',  vehicles, chargeTimeSubOptimalStationsUniformDistribution, 'mo-' )
legend('Random ', 'Uniform')
xlabel('Number of charging stations')
ylabel('Charging time (min)')
%axis([0 20  0 5])



