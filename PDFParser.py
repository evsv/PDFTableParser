#SETTING UP DEPENDENCIES
from datetime import datetime
import time
import Utilities as utils
import LoggingUtilities as logger
import configurations as config

def pdfParserControl():
    
    #OBTAINING LIST OF PDF FILES IN INPUT DIRECTORY
    pdfList = utils.pdfLister(inputDirectory = config.inputDirectory)
    
    #SETTING UP LOG FILE FOR LOGGING
    logFilePath = logger.initializeLogFile(outputDirectory = config.outputDirectory, 
                                           pdfList = pdfList)
                                          
    #BEGINNING ITERATING THROUGH EACH FILE
    for pdfFile in pdfList:
        
        #INITIALIZING THE PARSING OF THE PDF FILE
        numPages = utils.getNumPages(pdfFile = pdfFile)
        logger.logFileParseStart(logFilePath = logFilePath, pdfFile = pdfFile, 
                                 numPages = numPages)
        fileStartTime = time.time()
        
        utils.parseFile(filePath = pdfFile, numPages = numPages, 
                        expectedNumCols = config.expectedNumCols, 
                        colsToDrop = config.colsToDrop, 
                        colRenameMapping = config.columnRenameMapping, 
                        longFormIdCols = config.longFormIdCols, 
                        longFormValueCols = config.longFormValueCols, 
                        logFilePath= logFilePath, 
                        outputDirectory = config.outputDirectory)
                        
        fileEndTime = time.time()
        logger.logFileParseEnd(logFilePath = logFilePath, pdfFile = pdfFile, fileRunTime = fileEndTime - fileStartTime)
        
        