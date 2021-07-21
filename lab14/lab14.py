import pandas as pd
import numpy as np
data = pd.read_csv('clean_data.csv')


avg_acc_z = data['Accel-Z'].mean()
median_acc_x = data['Accel-X'].median()
median_acc_y = data['Accel-Y'].median()
median_acc_z = data['Accel-Z'].median() 
print("median vertical acceleration", median_acc_z)

acc_x = data['Accel-X'].to_numpy()
acc_y = data['Accel-Y'].to_numpy()
acc_z = data['Accel-Z'].to_numpy()

accs = np.vstack((acc_x, acc_y, acc_z))

avg_acc_mag = np.average(np.sqrt(acc_x ** 2 + acc_y ** 2 + acc_z ** 2))
avg_acc_mag = np.average(np.linalg.norm(accs, axis=0)) # ^ does the same thing iin more concise way
print(avg_acc_mag)
avg_acc_median = np.median(np.linalg.norm(accs, axis=0))
print(avg_acc_median)

# average tilt = theta
# cos(theta) = g / (avg z acceleration)
# theta = arccos(g / (avg z acceleration))
g = 9.80665 # m/s^2
avg_tilt = np.arccos(avg_acc_z / g)
print(avg_tilt * 180 / np.pi)
median_tilt = np.arccos(median_acc_z / g)
print(median_tilt * 180 / np.pi)

# v_x[i] = v_x[i-1] + a_x[i]*t
data['Timestamp (UTC)'] = data['Timestamp (UTC)'].apply(pd.to_datetime)
dt = (data['Timestamp (UTC)'][1] - data['Timestamp (UTC)'][0]).total_seconds()
# ^ number of seconds between first time AUV recorded acceleration and the second time

length = data['Accel-X'].shape[0] # length of data
v_x = np.zeros(length) # array of velocities in x-axis
v_y = np.zeros(length) # array of velocities in y-axis
dt = np.zeros(length) # array of velocities in y-axis
print(length + 1)
for i in range(1, length):
    # print(data['Timestamp (UTC)'][i] - data['Timestamp (UTC)'][i-1])
    dt[i] = (data['Timestamp (UTC)'][i] - data['Timestamp (UTC)'][i-1]).total_seconds()
    v_x[i] = v_x[i-1] + data['Accel-X'][i] * dt[i]
    v_y[i] = v_y[i-1] + data['Accel-Y'][i] * dt[i]
print(v_x)
dx = v_x * dt
dy = v_y * dt
# print(v_x)
# print(v_y)
# print(dt)
np.savetxt('v_x.txt', v_x)
print(sum(dx))
print(sum(dy))