# class that stores the low level data, the actual numbers
class Material:

    # has a type
    def __init__(self, t):
        self._spline = None
        self._x_start = None
        self._x_end = None
        self._step = 1  # step size is 1 by default
        self._type = t
        self._date = None

    @property
    def spline(self):
        return self._spline

    @spline.setter
    def spline(self, s):  # when a spline is received the X start and X end are also set, as they are obtained from
        # the spline object
        self._spline = s
        self.x_start = s
        self.x_end = s

    @property
    def x_start(self):
        return self._x_start

    @x_start.setter
    def x_start(self, s):
        self._x_start = s.get_knots()[0]

    @property
    def x_end(self):
        return self._x_end

    @x_end.setter
    def x_end(self, s):
        self._x_end = s.get_knots()[-1]

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, s):
        self._step = s

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, d):
        self._date = d

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t):
        self._type = t

    def print(self):
        print(self.spline)
        print(self.x_start)
        print(self.x_end)
