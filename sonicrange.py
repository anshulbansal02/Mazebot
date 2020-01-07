import pigpio
import time

class sonicrange:
    def __init__(self, pi, trig, echo):
        self.pi = pi
        self.trig = trig
        self.echo = echo

        self._ping = False
        self._high = None
        self._time = None

        self._triggered = False

        self._trig_mode = pi.get_mode(self._trig)
        self._echo_mode = pi.get_mode(self._echo)

        pi.set_mode(self._trig, pigpio.OUTPUT)
        pi.set_mode(self._echo, pigpio.INPUT)

        self._cb = pi.callback(self._trig, pigpio.EITHER_EDGE, self._cbf)
        self._cb = pi.callback(self._echo, pigpio.EITHER_EDGE, self._cbf)

        self._inited = True

    
    def _cbf(self, gpio, level, tick):
        if gpio == self._trig:
            if level == 0:
                self._triggered = True
                self._high = None

        else:
            if self._triggered:
                if level == 1:
                    self._high = tick
            else:
               if self._high is not None:
                  self._time = tick - self._high
                  self._high = None
                  self._ping = True


    def read(self):
        if self._inited:
            self._ping = False
            self.pi.gpio_trigger(self._trig)
            start = time.time()

            while not self._ping:
                if (time.time()-start) > 5.0:
                    return 20000

                time.sleep(0.001)

            return self._time

        else:
            return None

    def cancel(self):
        if self._inited:
            self._inited = False
            self._cb.cancel()
            self.pi.set_mode(self._trig, self._trig_mode)
            self.pi.set_mode(self._echo, self._echo_mode)

