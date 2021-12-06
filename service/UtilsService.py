from pyproj import Transformer
from exception.IllegalArgumentException import IllegalArgumentException

class UtilsService():

    def convertToGPS(self, itm_e, itm_n):
        if(itm_e.empty or itm_n.empty or itm_e[0] == 0.0 or itm_n[0] == 0.0):
            raise IllegalArgumentException('Invalid values given for itm_e or itm_n.')
        transformer = Transformer.from_crs("epsg:2157", "epsg:4326")
        latitude, longitude = transformer.transform(itm_e, itm_n)
        return [latitude, longitude]
