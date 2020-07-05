import smbus
import math
import time


class MPU6050:
    def __init__(self):
        # Power management registers
        self.power_mgmt_1 = 0x6b
        # self.power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68  # This is the address value read via the i2cdetect command
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)


if __name__ == '__main__':
    ALPHA = 1.0 / 5.0 # approximate moving average of X samples
    DAMP = 1 - ALPHA

    x_filt = 0.0
    y_filt = 0.0
    z_filt = 0.0

    print("X_RAW, X_SCALED, X_FILT, Y_RAW, Y_SCALED, Y_FILT")
    print("LSB/g, g, g, LSB/g, g, g")
    mpu = MPU6050()

    time.sleep(0.1)

    while True:
        gyro_xout = mpu.read_word_2c(0x43)
        gyro_yout = mpu.read_word_2c(0x45)
        gyro_zout = mpu.read_word_2c(0x47)

        #print ("gyro_xout : ", gyro_xout, " scaled: ", (gyro_xout / 131))
        #print ("gyro_yout : ", gyro_yout, " scaled: ", (gyro_yout / 131))
        #print ("gyro_zout : ", gyro_zout, " scaled: ", (gyro_zout / 131))

        accel_xout = mpu.read_word_2c(0x3b)
        accel_yout = mpu.read_word_2c(0x3d)
        accel_zout = mpu.read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        x_filt = ALPHA * accel_xout + DAMP * x_filt
        y_filt = ALPHA * accel_xout + DAMP * y_filt
        z_filt = ALPHA * accel_xout + DAMP * z_filt

        print(accel_xout, ", ", accel_xout_scaled, ", ", x_filt, ", ", accel_yout, ", ", accel_yout_scaled, ", ", y_filt)
        #print ("accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled)

        #print ("x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
        #print ("y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))

        time.sleep(0.250)
