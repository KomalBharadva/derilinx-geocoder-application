from pyproj import Transformer

class UtilsService():

    def convertToGPS(self, itm_e, itm_n):
        transformer = Transformer.from_crs("epsg:2157", "epsg:4326")
        latitude, longitude = transformer.transform(itm_e, itm_n)
        return [latitude, longitude]
