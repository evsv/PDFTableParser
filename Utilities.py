import glob
import os
import tabula as tbl
import pandas as pd
import copy
import LoggingUtilities as logger
from datetime import datetime
from pyPdf import PdfFileReader

def pdfLister(inputDirectory):
    """
    Function which lists the pdfs present in a user defined directory.
    
    Parameters
    ----------
        inputDirectory : str 
            The folder from which the list of PDF files need to be extracted
    
    Returns
    -------
        pdfList : list
            List of names of the pdfs that exist in the input directory
    
    """
    
    matchingString = os.path.join(inputDirectory, "*.pdf")
    pdfList = glob.glob(matchingString)
    
    return pdfList
    

def getNumPages(pdfFile):
    """
    Function which identifies number of pages in a given PDF file.

    Parameters
    ----------
        pdfFile : str 
            The path of the pdf file whose pages are to be determined    
        
    Returns
    -------
        numPages : int
            Number of pages in the PDF file
    
    """
    
    with open(pdfFile,'rb') as file:
        pdf = PdfFileReader(file)
        numberOfPages = pdf.getNumPages()
    
    return numberOfPages
    
def parseFile(filePath, numPages, expectedNumCols, colsToDrop, colRenameMapping, 
              longFormIdCols, longFormValueCols, logFilePath, outputDirectory):

    """
    Function which parses the individual PDF file into the long form CSV 
    required.

    Parameters
    ----------
        filePath : str 
            The path of the pdf file to be parsed
        
        numPages : int
            Number of pages present in the PDF file
        
        colsToDrop : list
            List of column names to be dropped from the table obtained from the 
            PDF file
        
        colRenameMapping : dict
            Dictionary containing the mapping of old column names to the new 
            column names (Refer configuration file for example)
            
        longFormIdCols : dict
            Columns to be retained for identification when converting the table
            from wide form to long form.
            NOTE: THIS WILL NOT CHANGE FOR A GIVEN TABLE
        
        longFormValueCols : dict
            Columns to be converted into the long form from the wide form
            NOTE: THIS WILL NOT CHANGE FOR A GIVEN TABLE
            
        logFilePath : str
            Path of the log file
            
        outputDirectory : str
            Directory where the output files should be stored
        
    Returns
    -------
        None
    
    """
    
    fileConsolidatedTable = pd.DataFrame()

    #SETTING UP ITERATOR TO ITERATE THROUGH EACH PAGE
    for counter in range(0, numPages):   
        try:

            #READING THE RAW TABLE/S ON THE PAGE
            pageNo = counter+1
            pageRawTable = tbl.read_pdf(filePath, pages = pageNo, spreadsheet = True)
            pageRawTable = pageRawTable.replace("\\r", "", regex = True) #TREATING NEW LINE ESCAPE CHARACTERS
            numRows = len(pageRawTable.index)
            numCols = len(pageRawTable.columns)
            
            #TREATING ESCAPE CHARACTER IN COLUMN KHATA/SURVEY
            columnList = pageRawTable.columns
            columnList = [columnName.replace("\r", "") for columnName in columnList]
            pageRawTable.columns = columnList
            
            #HANDLING CONDITION WHERE EXTRA COLUMN MIGHT EXIST DUE TO DATA DISCREPANCIES
            if numCols != expectedNumCols:
                errorMessage = "Expected " + str(expectedNumCols) + " columns, but found " + str(numCols) + " columns"
                logger.logPageError(logFilePath = logFilePath, pdfFile = filePath, 
                                    pageNo = pageNo, errorMessage = errorMessage)
                continue

            #REMOVING THE LAST TWO ROWS, IN CASE THE PAGE IS THE LAST PAGE  
            if pageNo == numPages:
                pageRawTable.drop([numRows-2, numRows-1], inplace = True, axis = 0)

                numRows = len(pageRawTable.index)
                numCols = len(pageRawTable.columns)      
            
            #SETTING UP THE INDICES FOR ROWS WITH APP NO AND ROWS WITH AMT
            appRowIndices = range(0, numRows, 2)
            amtRowIndices = range(1, numRows, 2) #NOTE: WE EXCLUDE THE LAST ROW, AS THE VALUE POSITIONS ARE DIFFERENT IN IT
            lastRowIndex = numRows - 1            
            
            #TREATING DATAFRAME TO REMOVE USER SSPECIFIED COLUMNS
            pageRawTable.iloc[lastRowIndex] = pageRawTable.iloc[lastRowIndex].shift(6, axis = 0) #CORRECTING OFFSET IN LAST ROW
            pageRawTable.drop(colsToDrop, axis = 1, inplace = True)
            longFormIdCols = [colName for colName in longFormIdCols if colName not in colsToDrop]
            
            #SETTING UP DATAFRAMES CONTAINING APP_NO AND AMT
            appNoDataFrame = copy.deepcopy(pageRawTable.iloc[appRowIndices, :])
            appNoDataFrame = appNoDataFrame.reset_index()
            amtDataFrame = copy.deepcopy(pageRawTable.iloc[amtRowIndices, :])
            amtDataFrame = amtDataFrame.reset_index()
            appNoDataFrame.drop("index", axis = 1, inplace = True)
            amtDataFrame.drop("index", axis = 1, inplace = True)        

            amtDataFrame.ix[:,longFormIdCols] = appNoDataFrame.ix[:, longFormIdCols]
            
            #CONVERTING APP_NO DATAFRAME FROM WIDE TO LONG FORMAT
            appNoDataFrame = pd.melt(appNoDataFrame, 
                                     id_vars = longFormIdCols, 
                                     value_vars = longFormValueCols)            


            #RENAMING THE NEW COLUMNS IN APP_NO DATAFRAME
            appNoDataFrame = appNoDataFrame.rename(index = str, columns = {"variable": "year", "value": "app_no"})        
            
            #CONVERTING AMT DATAFRAME FROM WIDE TO LONG FORMAT
            amtDataFrame = pd.melt(amtDataFrame, 
                                     id_vars = longFormIdCols, 
                                     value_vars = longFormValueCols)

            #RENAMING THE NEW COLUMNS IN AMT DATAFRAME
            amtDataFrame = amtDataFrame.rename(index = str, columns = {"variable": "year", "value": "amt"})        
            
            #MERGING THE TWO DATAFRAMES TO GET A CONSOLIDATED FRAME FOR THE PAGE
            joinKeyList = longFormIdCols + ["year"]   
            processedPageTable = appNoDataFrame.merge(amtDataFrame, on = joinKeyList, how = "left")
            
            #RENAMING COLUMNS BEFORE CONVERTING TO WIDE AND LONG FORM
            processedPageTable.rename(colRenameMapping, inplace = True)

            #DROPPING ROWS CORRESPONDING TO YEARS WHERE TAX WASNT PAID
            processedPageTable = processedPageTable.dropna(axis = 0, subset = ["amt", "app_no"])
            #processedPageTable.to_csv(os.path.basename(filePath) + str(pageNo) + ".csv", index = False)
            
            #APPENDING THE PROCESSED DATAFRAME TO THE OVERALL FILE DATAFRAME
            if len(fileConsolidatedTable.index) == 0:
                fileConsolidatedTable = processedPageTable
            else:
                fileConsolidatedTable = fileConsolidatedTable.append(processedPageTable)     

        except Exception as e:
            logger.logPageError(logFilePath = logFilePath, pdfFile = filePath, 
                                pageNo = pageNo, errorMessage = str(e))
            continue
    
    outputFileName = os.path.basename(filePath) + ".csv"
    outputFile = os.path.join(outputDirectory, outputFileName)
    fileConsolidatedTable.to_csv(outputFile, index = False)
    