import Reader
import datamaths


class EiRefScan:

    def __init__(self):
        self._key = ""
        self._name = ""
        self._product_name = ""
        self._sample_type = ""
        self._ref_emission_range = [0, 0]
        self._qy_emission_range = [0, 0]
        self._qy = 0
        self._lifetime = 0
        self._spline = ""

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, k):
        self._key = k

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, pn):
        self._product_name = pn

    @property
    def sample_type(self):
        return self._sample_type

    @sample_type.setter
    def sample_type(self, st):
        self._sample_type = st

    @property
    def ref_emission_range(self):
        return self._ref_emission_range

    @ref_emission_range.setter
    def ref_emission_range(self, er):
        if er != "-":
            values = er.split()
            self._ref_emission_range[0] = values[0]
            self._ref_emission_range[1] = values[1]
        else:
            self._ref_emission_range[0] = er
            self._ref_emission_range[1] = er

    @property
    def qy_emission_range(self):
        return self._qy_emission_range

    @qy_emission_range.setter
    def qy_emission_range(self, er):
        if er != "-":
            values = er.split()
            self._qy_emission_range[0] = values[0]
            self._qy_emission_range[1] = values[1]
        else:
            self._qy_emission_range[0] = er
            self._qy_emission_range[1] = er

    @property
    def qy(self):
        return self._qy

    @qy.setter
    def qy(self, qy):
        self._qy = qy

    @property
    def lifetime(self):
        return self._lifetime

    @lifetime.setter
    def lifetime(self, lt):
        self._lifetime = lt

    @property
    def spline(self):
        return self._spline

    @spline.setter
    def spline(self, s):
        self._spline = s

    def add_scan(self, filename):
        read = Reader.scan_to_dict(filename)
        self.spline = datamaths.getspline(read)
        print(self.spline)

    def print(self):
        print(self.name)
        print(self.product_name)
        print(self.sample_type)
        print(self.ref_emission_range)
        print(self.qy_emission_range)
        print(self.qy)
        print(self.lifetime)
        print(self.spline)
