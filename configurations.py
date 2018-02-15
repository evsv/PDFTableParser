#PARSER CONFIGURATION PARAMETERS
expectedNumCols = 17 #HOW MANY COLUMNS ARE EXPECTED IN THE INPUT FILE
columnRenameMapping = {"Sl No": "s_no",                  #HOW SHOULD THE COLUMNS FROM THE IP FILE BE RENAMED
                       "New PID": "new_pid_no",
                       "Old PID": "old_pid_no",
                       "Khata /Survey": "khata_survey",
                       "Owner Name": "owner_name",
                       "Property Address": "address"} 
inputDirectory = "Input Files"                  
outputDirectory = "Output CSVs"
colsToDrop = ["Unnamed: 6"]
longFormIdCols = ["Sl No", "New PID", "Old PID", "Khata /Survey", 
                  "Owner Name", "Property Address"]
longFormValueCols = ["2008-2009", "2009-2010", "2010-2011", "2011-2012", 
                     "2012-2013", "2013-2014", "2014-2015", "2015-2016",
                     "2016-2017", "2017-2018"]
                     