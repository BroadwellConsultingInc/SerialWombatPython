import supervisor
import time

millisStart = supervisor.ticks_ms()
def millis():
    return(int((supervisor.ticks_ms() - millisStart)))

def delay(delayMs):
    time.sleep(delayMs / 1000)
    
def delayMicroseconds(delayUs):
    start_time_ns = time.monotonic_ns(); 
    while (time.monotonic_ns() - start_time_ns) < (delayUs * 1000):
    # You can perform other non-blocking tasks here
        pass