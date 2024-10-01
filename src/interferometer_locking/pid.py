class PID:
    """PID controller.

    Args:
        Kp (float): Proportional gain.
        Ki (float): Integral gain.
        Kd (float): Derivative gain.
        setpoint (float): Desired value of the input. 

    Attributes:
        Kp (float): Proportional gain.
        Ki (float): Integral gain.
        Kd (float): Derivative gain.
        setpoint (float): Desired value of the input.
        integral (float): Integral of the error.
        previous_error (float): Error at the previous time step.

    Methods:
        set_gains(Kp, Ki, Kd): Set the gains of the controller.
        set_setpoint(setpoint): Set the setpoint of the controller.
        reset(): Reset the integral and previous error.
        __call__(input_val, dt): Compute the output of the controller   
    """

    def __init__(self, Kp, Ki, Kd, setpoint):
        self.set_gains(Kp, Ki, Kd)
        self.set_setpoint(setpoint)
        self.reset()

    def set_gains(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def reset(self):
        self.integral = 0
        self.previous_error = 0

    def __call__(self, input_val, dt):
        error = self.setpoint - input_val
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        self.previous_error = error

        return (self.Kp * error +
                self.Ki * self.integral +
                self.Kd * derivative)
