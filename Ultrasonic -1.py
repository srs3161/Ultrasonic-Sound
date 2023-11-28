import pineworkslabs.RPi as GPIO
from time import sleep, time

# Constants
DEBUG=False
SETTLE_TIME =2             # seconds to let the sensor settle
CALIBRATIONS =5              # number of calibration measurements to take
CALIBRATIONS_DELAY=1
TRIGGER_TIME=0.00001
SPEED_OF_SOUND=343

# Now set the naming convention a.k.a mode
GPIO.setmode(GPIO.LE_POTATO_LOOKUP)

# GPIO pins
trig=18                      # the sensor's TRIG pin
echo=27                      # the sensor's ECHO pin
GPIO.setup(TRIG,GPIO.OUT)     # TRIG is an output
GPIO.setup(ECHO,GPIO.IN)      # ECHO is an input


def calibrate():
    print("Calibrating...")
    print("-Place the sensor a measured distance away from an object.")
    known_distance=float(input("-What is the measured distance (cm)? "))

    
    print("-Getting calibration measurements...")
    distance_avg=0

    for i in range(CALIBRATIONS):
        distance=get_distance()
        if DEBUG:
            print("--Got {distance}cm")

        
        distance_avg+=distance
        sleep(CALIBRATIONS_DELAY)

    distance_avg/=CALIBRATIONS
    if DEBUG:
        print("--Average is {distance_avg}")

    # Calculate the correction factor
    correction_factor=known_distance/distance_avg
    if DEBUG:
        print("--Correction factor is {correction_factor}")

    print("Done.")
    print()
    return correction_factor


def get_distance():
    # Trigger the sensor by setting it high for a short time and then setting it low
    GPIO.output(trig, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(trig, GPIO.LOW)

    # Wait for the ECHO pin to read high
    # Once the ECHO pin is high, the start time is set
    # Once the ECHO pin is low again, the end time is set
    
    while(GPIO.input(echo) == GPIO.LOW):
        start = time()

    while(GPIO.input(echo) == GPIO.HIGH):
        stop = time()

    

    # Calculate the duration that the ECHO pin was high
    # This is how long the pulse took to get from the sensor to the object and back again
    duration=stop-start

    # Calculate the total distance that the pulse traveled by factoring in the speed of sound (m/s)
    distance=duration*SPEED_OF_SOUND

    # Distance from the sensor to the object is half of the total distance traveled
    distance/=2

    # Convert from meters to centimeters
    distance*=100

    return distance


########
# MAIN #

# First, allow the sensor to settle for a bit
print(f"Waiting for sensor to settle ({SETTLE_TIME}s)")
GPIO.output(trig,GPIO.LOW)
sleep(SETTLE_TIME)

# Next, calibrate the sensor
correction_factor=calibrate()

# Then, measure
input("Press enter to begin")
print("Getting measurements")
list = []
while (True):
    # Get the distance to an object and correct it with the correction factor
    print("-Measuring...")
    distance=get_distance()*correction_factor
    sleep(1)
    distance=round(distance, 4)
    print("--Distance measured: {distance}cm")

    # Prompt for another measurement
    i=input("--Get another measurement (Y/n)? ")

    # Stop measuring if desired
    if (not i in ["y", "Y", "yes", "Yes", "YES", "" ]):
        break
        
        
# Finally, clean up the GPIO pins
print("Done.")
print()

print("Unsorted measurements: ")
print(list)
list.sort()
print("sorted measurmnets: ")
print(list)
GPIO.cleanup()

