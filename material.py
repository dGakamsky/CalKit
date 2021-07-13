class Lamp_Material:

    # has a type
    def __init__(self, t):
        self._spline = []
        self._x_start = []
        self._x_end = []
        self._step = 1  # step size is 1 by default
        self._type = t
        self._date = None

    @property
    def spline(self):
        return self._spline

    @spline.setter
    #receives a list of splines from the scan reader
    def spline(self, spline):  # when a spline is received the X start and X end are also set, as they are obtained from
        # the spline object
        self._spline = spline
        self.x_start = spline
        self.x_end = spline

    @property
    def x_start(self):
        return self._x_start

    @x_start.setter
    def x_start(self, spline):
        for i in range(len(spline)):
            self._x_start.append(spline[i].get_knots()[0])

    @property
    def x_end(self):
        return self._x_end

    @x_end.setter
    def x_end(self, spline):
        for i in range(len(spline)):
            self._x_end.append(spline[i].get_knots()[-1])

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


