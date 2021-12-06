class AddressOutputDTO():
    __address, __lat, __long = "", 0.0 , 0.0

    def getAddress(self):
        return self.__address
    
    def getLat(self):
        return self.__lat

    def getLong(self):
        return self.__long

    def setAddress(self, address):
        self.__address = address

    def setLat(self, lat):
        self.__lat = lat

    def setLong(self, long):
        self.__long = long

    def toJSON(self):
        return {
            'Address' : self.__address,
            'Latitude' : self.__lat,
            'Longitude' : self.__long
        }
