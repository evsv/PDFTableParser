import os
from datetime import datetime

def initializeLogFile(outputDirectory, pdfList):
    """
    Function which creates a log file, and initializes it with the information
    relevant to run.
    
    Information captured are:
    1.Start time of the parser
    2.Files found in the input directory
    
    Parameters
    ----------
        outputDirectory : str 
            The folder into which all the outputs of the PDF Parser are written
    
        pdfList : list
            The list of pdf files that are parsed in the execution of the 
            parser
        
    Returns
    -------
        logFilePath: str
            Path of the log file that's been created. Will be used for all 
            subsequent logging operations.
    
    """
    
    #INITIALIZING VARIABLES FOR LOG CREATION
    startTime = str(datetime.now())
    fileName = "PDFParserLog_" + startTime.replace(":", "_") + "_.txt"
    logFilePath = os.path.join(outputDirectory, fileName)
    
    #CREATING THE LOG FILE IN WRITE MODE
    logFile = open(logFilePath, "w+")
    
    #WRITING INTO THE LOG FILE
    logFile.write("-----------------------BEGIN PARSING-----------------------\n\n")
    logFile.write("Began parsing PDFs at: " + startTime + "\n\n")
    
    logFile.write("The following PDFS were found in the input folder:" + "\n")
    for pdfFile in pdfList:
        logFile.write(os.path.basename(pdfFile))
        logFile.write("\n")
    
    logFile.write("\n-----------------------------------------------------------\n\n")
    
    #CLOSING THE LOG FILE
    logFile.close()
    
    return logFilePath
    
def logFileParseStart(logFilePath, pdfFile, numPages):
    """
    Function which updates the log file with information about the PDF being parsed
    
    Information captured are:
    1.Name of the file being parsed
    2.Number of pages found in the file
    
    Parameters
    ----------
        logFilePath : str 
            The path of the log file to be updated
    
        fileName : str
            The path of the PDF file being parsed
            
        numPages : int
            Number of pages found in the PDF file
        
    Returns
    -------
        None

    """    
    
    logFile = open(logFilePath, "a")    
    fileName = os.path.basename(pdfFile)
    
    logFile.write("Parsing file: " + fileName + "\n")
    logFile.write("Number of pages found: " + str(numPages) + "\n")
    
    logFile.close()

def logPageError(logFilePath, pdfFile, pageNo, errorMessage):
    """
    Function which updates the log file with the info on error faced when 
    parsing a page
    
    Parameters
    ----------
        fileName : str 
            Name of the log file where the error was found
    
        pageNumber : int
            The page on which the error occurred
            
        errorMessage : str
            Message capturing details of the error
        
    Returns
    -------
        None

    """        
    
    logFile = open(logFilePath, "a")    
    fileName = os.path.basename(pdfFile)
    
    logFile.write("Encountered the below error when parsing page " + 
                  str(pageNo) + " of file " + fileName + ":\n")
                  
    logFile.write(errorMessage + "\n\n")
    
    logFile.close()    
    
def logFileParseEnd(logFilePath, pdfFile, fileRunTime):
    """
    Function which updates the log file with information about the PDF being parsed
    
    Information captured are:
    1.Name of the file being parsed
    2.Time taken to parse the file
    
    Parameters
    ----------
        logFilePath : str 
            The path of the log file to be updated
    
        fileRunTime : int
            Time taken to parse the file in seconds
        
    Returns
    -------
        None

    """    
    
    logFile = open(logFilePath, "a")    
    fileName = os.path.basename(pdfFile)
    
    logFile.write("Completed parsing file: " + fileName + "\n")
    logFile.write("Time taken to parse file: " + str(fileRunTime/60) + "\n\n")
    
    logFile.write("-----------------------------------------------------------\n\n")
    
    logFile.close()