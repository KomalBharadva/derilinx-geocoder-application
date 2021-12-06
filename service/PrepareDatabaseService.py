import pandas as pd
from exception.FileNotFoundException import FileNotFoundException
from service.UtilsService import UtilsService

class PrepareDatabase():

    utilsService = UtilsService()

    def getCountyCoordinates(self, filePath):
        try:
            tempCountyDF = pd.read_csv(filePath, dtype = object)
        except:
            raise FileNotFoundException("File with filePath: '"+filePath+"' is not found")
        tempCountyDF = tempCountyDF.filter(['County', 'English_Name', 'ITM_E', 'ITM_N'])
        tempCountyDF.drop_duplicates(subset=['County'], keep = 'first', inplace = True)
        tempCountyDF['X'], tempCountyDF['Y'] = self.utilsService.convertToGPS(tempCountyDF['ITM_E'], tempCountyDF['ITM_N'])
        countyDF = tempCountyDF[['County','English_Name', 'X','Y']]
        print('County co-ordinates are setup.')
        return countyDF

    def getTownlandsCoordinates(self, filePath):
        try:
            tempTownlandsDF = pd.read_csv(filePath, dtype = object)
        except:
            raise FileNotFoundException("File with filePath: '"+filePath+"' is not found")
        tempTownlandsDF = tempTownlandsDF.filter(['County', 'English_Name', 'ITM_E', 'ITM_N'])
        tempTownlandsDF.drop_duplicates(subset=['English_Name'], keep = 'first', inplace = True)
        tempTownlandsDF['X'], tempTownlandsDF['Y'] = self.utilsService.convertToGPS(tempTownlandsDF['ITM_E'], tempTownlandsDF['ITM_N'])
        townlandsDF = tempTownlandsDF[['County', 'English_Name', 'X', 'Y']]
        print('Townlands co-ordinates are setup.')
        return townlandsDF
