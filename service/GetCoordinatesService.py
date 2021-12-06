import pandas as pd
from Constants import Constants
from dto.addressOutputDTO import AddressOutputDTO
from exception.FileNotFoundException import FileNotFoundException
from exception.NotFoundException import NotFoundException
from service.PrepareDatabaseService import PrepareDatabase

class GetCoordinates():

    prepareDatabase = PrepareDatabase()
    countyDF = pd.DataFrame()
    townlandsDF = pd.DataFrame()

    def __init__(self):
        self.countyDF = self.prepareDatabase.getCountyCoordinates(Constants.COUNTY_FILE_PATH)
        self.townlandsDF = self.prepareDatabase.getTownlandsCoordinates(Constants.TOWNLOADS_FILE_PATH)

    def getCoordinates(self, filePath):
        rawAddressDF = self.__readAddress(filePath)
        finalAddressCoordinates = []
        for index, eachAddress in rawAddressDF.iterrows():
            addressOutputDTO = AddressOutputDTO()
            eachAddressList = self.__getAddressList(eachAddress['Address'])
            tempCoordinates = self.__getAddressCoordinates(eachAddressList)
            eachAddress = pd.Series(eachAddress)
            if not tempCoordinates.empty:
                addressOutputDTO.setAddress(eachAddress['Address'])
                addressOutputDTO.setLat(tempCoordinates['X'].values[0])
                addressOutputDTO.setLong(tempCoordinates['Y'].values[0])
                finalAddressCoordinates.append(addressOutputDTO.toJSON())
        if(len(finalAddressCoordinates) == 0):
            raise NotFoundException('No co-ordinates found for the given address.')
        return finalAddressCoordinates

    def getCoordinatesForAddressString(self, givenAddressString):
        addressOutputDTO = AddressOutputDTO()
        eachAddressList = self.__getAddressList(givenAddressString)
        if(len(eachAddressList) == 0):
            raise NotFoundException('Not a valid address. Please try again with a valid address.')
        tempCoordinates = self.__getAddressCoordinates(eachAddressList)
        if(tempCoordinates.empty):
            raise NotFoundException('No co-ordinates found for the given address.')
        eachAddress = pd.Series(givenAddressString)
        addressOutputDTO.setAddress(eachAddress[0])
        addressOutputDTO.setLat(tempCoordinates['X'].values[0])
        addressOutputDTO.setLong(tempCoordinates['Y'].values[0])
        return addressOutputDTO.toJSON()

    def __readAddress(self, filePath):
        try:
            addressDF = pd.read_csv(filePath)
        except:
            raise FileNotFoundException("File with filePath: '"+filePath+"' is not found")
        return addressDF

    def __getAddressList(self, givenAddressString):
        # Splitting the address by commma, dots and underscore
        givenAddressString = givenAddressString.replace('.', ',').split(',')
        tempAddress = [item.replace("_", "-") for item in givenAddressString]
        tempAddress = [item.replace('None', "") for item in tempAddress]
        # Converts the string to uppercase and removes leading and trailing whitspaces if present
        tempAddress  = [elem.upper().strip() for elem in tempAddress]
        # Removing Co from final_address if present
        if "CO" in tempAddress: tempAddress.remove("CO")
        while '' in tempAddress: tempAddress.remove('')
        if len(tempAddress) > 1 and tempAddress[-1] == tempAddress[-2]: tempAddress.pop()
        return tempAddress

    def __getAddressCoordinates(self, address):
        final_df = pd.DataFrame()
        if len(address) >= 2:
            temp = pd.DataFrame(self.townlandsDF.loc[(self.townlandsDF['English_Name'] == address[-2]) & (self.townlandsDF['County'] == address[-1])])
            if temp.empty & self.townlandsDF.loc[self.townlandsDF['English_Name'] == address[-2]].empty:
                temp = pd.DataFrame(self.countyDF.loc[self.countyDF['County'] == address[-1]])
        elif len(address) == 1:
            temp = pd.DataFrame(self.countyDF.loc[self.countyDF['County'] == address[0]])
        else:
            raise NotFoundException('No co-ordinates found for the given address.')
        final_df = final_df.append(temp, ignore_index=True)
        return final_df
