import time


class PID:
    """
    This is an implementation of the "Beginner's PID" by Brett Beauregard

    """

    def __init__(self):
        # working variables*/
        self.last_time = time.time()
        self.last_current = 0
        self.output = 0
        self.target = 0
        self.i_out = 0
        self.k_p = 1
        self.k_i = 0
        self.k_d = 0
        self.sample_time = 1  # seconds
        self.out_min = -1
        self.out_max = 1
        self.in_auto = True
        self.output = 0

    def compute(self, current):
        now = time.time()
        if now >= self.last_time + self.sample_time:

            error = self.target - current
            self.i_out += (self.k_i * error)
            if self.i_out > self.out_max:
                self.i_out = self.out_max
            elif self.i_out < self.out_min:
                self.i_out = self.out_min
            d_current = current - self.last_current

            self.output = self.k_p * error + self.i_out - self.k_d * d_current
            if self.output > self.out_max:
                self.output = self.out_max
            elif self.output < self.out_min:
                self.output = self.out_min

            self.last_current = current
            self.last_time = now
        return self.output

    def set_tunings(self, Kp, Ki, Kd):
        self.k_p = Kp
        self.k_i = Ki * self.sample_time
        self.k_d = Kd / self.sample_time

    def set_sample_time(self, new_sample_time):
        if new_sample_time > 0:
            ratio = new_sample_time / self.sample_time
            self.k_i *= ratio
            self.k_d /= ratio
            self.sample_time = new_sample_time

    def set_output_limits(self, min, max):
        self.out_min = min
        self.out_max = max
        if min > max:
            self.out_max = min
            self.out_min = max

        if self.output > self.out_max:
            self.output = self.out_max
        elif self.output < self.out_min:
            self.output = self.out_min

        if self.i_out > self.out_max:
            self.i_out = self.out_max
        elif self.i_out < self.out_min:
            self.i_out = self.out_min

    def set_mode(self, mode):
        self.in_auto = mode
        if mode and not self.in_auto:
            self.i_out = self.output
            if self.i_out > self.out_max:
                self.i_out = self.out_max
            elif self.i_out < self.out_min:
                self.i_out = self.out_min
