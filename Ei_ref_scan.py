import Reader
import datamaths


class EiRefScan:

    def __init__(self):
        self._key = ""
        self._name = ""
        self._product_name = ""
        self._sample_type = ""
        self._emission_range = ""
        self._qy = ""
        self._lifetime = ""
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
    def emission_range(self):
        return self._emission_range

    @emission_range.setter
    def emission_range(self, er):
        self._emission_range = er

    @property
    def qy(self):
        return self._emission_range

    @qy.setter
    def qy(self, qy):
        self._qy = qy

    @property
    def lifetime(self):
        return self._emission_range

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
        print(self.emission_range)
        print(self.qy)
        print(self.lifetime)
        print(self.spline)
