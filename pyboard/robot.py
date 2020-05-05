from pyb import delay
from pyb import Pin
from pyb import LED
from pyb import ExtInt
from pyb import Timer
# Libraries - Motors
from pca9685fb import PCA9685
from adamotshv2fb import DCMotor

# Allocate an emergency exception buff to debug errors
#   that may occur inside interruptions
from micropython import alloc_emergency_exception_buf
from micropython import schedule 
alloc_emergency_exception_buf(100)


class Robot:
    
    def __init__(self):
        # Encoder Wheel variables
        self.left_wheel_counter = 0
        self.right_wheel_counter = 0
        self.distance_robot = 0
        self.left_encoder_pass = False
        self.right_encoder_pass = False

        # Encoder Wheel pins
        self.left_encoder_pin = Pin(Pin.board.X19, Pin.IN)
        self.right_encoder_pin = Pin(Pin.board.X20, Pin.IN)

        # Encoder Wheel timer
        self.tim_left_encoder = Timer(4, freq=1000)
        self.tim_right_encoder = Timer(2, freq=1000)

        #Speed wheel
        self.left_speed = 2048
        self.right_speed = 1987
                   
        # MotorShield communication and control
        # Create a PCA9685 on I2C bus 1 (SCL=X9, SDA=X10)
        pca = PCA9685(1)
        # Start the PWM timers
        pca.start()
        # Create a DC motor on ports M1 and M2
        # Functions available:
        #   throttle() - from -4095 to 4096
        #   brake() - no parameters
        self.m_left = DCMotor(pca, 1)
        self.m_right = DCMotor(pca, 3)

        self.m_left.brake()
        self.m_right.brake()
        
    # ENCODER INTERRUPTIONS
    def callback_check_left_encoder(self, tim):
        if self.left_encoder_pin.value() == 1:
            if self.left_encoder_pass == False:
                self.left_encoder_pass = True
                self.left_wheel_counter += 1
        else:
            if self.left_encoder_pass == True:
                self.left_encoder_pass = False
                self.left_wheel_counter += 1
         
    def callback_check_right_encoder(self, tim):
        if self.right_encoder_pin.value() == 1:
            if self.right_encoder_pass == False:
                self.right_encoder_pass = True
                self.right_wheel_counter += 1
        else:
            if self.right_encoder_pass == True:
                self.right_encoder_pass = False
                self.right_wheel_counter += 1
                      
    # MOTION CONTROL FUNCTIONS
    def forward_dcm(self, dist_cm):
        # Clear counters
        self.left_wheel_counter = 0
        self.right_wheel_counter = 0
        # Start Encoders
        self.tim_left_encoder.callback(self.callback_check_left_encoder)
        self.tim_right_encoder.callback(self.callback_check_right_encoder)
        # START YOUR ENGINES
        self.m_left.throttle(self.left_speed)
        self.m_right.throttle(self.right_speed)
        while 1:
            # 114 ticks = 100 cm +- (0.5 cm)
            if (self.left_wheel_counter >= ((dist_cm/100) * 114)):
                self.brake()
                self.distance_robot = self.left_wheel_counter * (100/114)
                break
            # Terminei
     
    def rotate_degrees(self, degrees):
        self.tim_left_encoder.callback(self.callback_check_left_encoder)
        self.tim_right_encoder.callback(self.callback_check_right_encoder)
        self.m_left.throttle(-self.left_speed)
        self.m_right.throttle(self.right_speed)
        while 1:
            # 93 ticks = 360
             if(self.left_wheel_counter >= ((degrees/360) * 95)):
                break
        self.brake()

    def brake(self):
        self.m_left.brake()
        self.m_right.brake() 
        self.tim_left_encoder.callback(None)
        self.tim_right_encoder.callback(None)

    
