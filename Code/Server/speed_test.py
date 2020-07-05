import time
from Motor import Motor as M
from Ultrasonic import Ultrasonic

if __name__ == '__main__':
    motor = M()
    us = Ultrasonic()

    measures = []

    m_speed = 4095
    dt = 1.0

    for i in range(5):
        start = us.get_distance()
        print('Start distance: ' + str(start))

        motor.setMotorModel(m_speed, m_speed, m_speed, m_speed) # forward
        time.sleep(dt)
        motor.setMotorModel(0, 0, 0, 0)  # stop
        time.sleep(1.0)

        stop = us.get_distance()
        print('Stop distance : ' + str(stop))

        if start > stop:
            measures.append(start)
            measures.append(stop)
        else:
            print("Rejecting measure (stop >= start)")

        motor.setMotorModel(-m_speed, -m_speed, -m_speed, -m_speed)  # go backward
        time.sleep(dt)
        motor.setMotorModel(0, 0, 0, 0)  # stop
        time.sleep(1.0)

    speeds = []
    avg = 0
    for i in range(0, len(measures), 2):
        speed = ((measures[i] - measures[i + 1]) / 100.0) / dt

        if speed > 0:
            speeds.append(speed)
            avg = avg + speed
        else:
            print('Rejecting measures ' + str(i) + ' ' + str(i + 1) + ' -> negative speed')

    print('Measures: ' + str(measures))
    print('Speeds  : ' + str(speeds) + " m/s")
    print('Avg     : ' + str(avg/len(speeds)))

