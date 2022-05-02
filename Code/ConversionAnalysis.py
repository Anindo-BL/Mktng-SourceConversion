
# Importing stand python libraries
from pathlib import Path
from datetime import datetime

# Importing installed python libraries
import pandas as pd

# import custom modules(assumed to be present in same direcory)
import Read_Config as rd
from Write_Functions import write_results

def get_DataFiles():
    dirPath = "../ConfigFiles"
    fName = "Input_Config.json"
    return (rd.get_fileNames_wPath(dirPath, fName))

def get_category_dict():
    dirPath = "../ConfigFiles"
    fName = "Source_Categorization.json"
    return rd.get_Categorization(dirPath, fName)

def renameCols():
    global df
    dirPath = "../ConfigFiles"
    fName = "Rename_Columns.json"
    rename_d = rd.get_renameDict(dirPath, fName)
    df.rename(columns=rename_d, inplace=True)
    print(f"Column names after renaming: {df.columns}")


def check_EmailPresence(email2Check):
    global pymnt_df
    pymnt_email_list = pymnt_df['Email'].tolist()
    if email2Check in pymnt_email_list:
        return True
    else:
        return False


def main():
    global df,pymnt_df
    # Get the data Files along with path
    pymnt_DataFile_wPath, mntlhy_SrcDataFile_wPath = get_DataFiles()

    # Read the Payments Data File in DataFrame
    pymnt_df = pd.read_csv(pymnt_DataFile_wPath)
    print(f"Shape of pmnt df {pymnt_df.shape}")
    #  Read the Monthly Data File in DataFrame
    df = pd.read_csv(mntlhy_SrcDataFile_wPath)
    print(f"Shape of source df {df.shape}")

    rslt_d = {} # All the processed output will be stored here
    rslt_d['File_Processed'] = Path(mntlhy_SrcDataFile_wPath).name
    rslt_d['Processed_At'] = datetime.now().strftime("%b %d,%Y %H:%M:%S")
    rslt_d['Num_of_Rows'] = df.shape[0]

    # Check  Email and Source columns are there correctly or not
    pd.set_option('display.max_columns', None)
    print (f"Column names are {df.columns}")
    print (f" First 5 rows are:")
    print (df.head(5))

    print ("\n\nCheck Email and Source columns are correct are not")
    print (" If it needs to be renamed, change the rename config file ")
    renameFlag = input(" andthen press r ")
    if (renameFlag == 'r'):
        renameCols()

    # Remove rows with duplicate email-IDs and save the unique email ids
    df.drop_duplicates(subset="Email", keep="first",inplace=  True)
    print(f"Shape after removing duplicates {df.shape}")
    rslt_d['Num_of_Unique_Rows'] = df.shape[0]

    # findout different sources through which registration has happened
    print("\nFollowing are the sources in data")
    print (df.Source.unique())
    print ("If needed, please change the source categrization config file")
    input ("Press any key to continue")

    # Replace the source values as category dictionary
    df.replace({"Source": get_category_dict()}, inplace=True)
    # Count the different source categories & save in a dictionary
    rgstrn_ctgrzdSource_dict = df['Source'].value_counts().to_dict()
    print(rgstrn_ctgrzdSource_dict)
    rslt_d['Source_Facebook'] = rgstrn_ctgrzdSource_dict['FaceBook']
    rslt_d['Source_Naukri'] = rgstrn_ctgrzdSource_dict['Naukri']
    rslt_d['Source_Other'] = df.shape[0] -\
                                    (rslt_d['Source_Facebook']+
                                     rslt_d['Source_Naukri'])

    # Check which email-ids are there in payment db list
    df['Present'] = df['Email'].apply(check_EmailPresence)

    rslt_d['Converted_Total'] = df['Present'].sum()
    print(" Total Conversion", rslt_d['Converted_Total'])

    prs_df = df.loc[df['Present'] == True]
    print ("Present_df",prs_df.shape)
    convrtdSource_dict = prs_df['Source'].value_counts().to_dict()
    print (convrtdSource_dict)
    rslt_d['Converted_FaceBook'] = convrtdSource_dict['FaceBook']
    rslt_d['Converted_Naukri'] = convrtdSource_dict['Naukri']
    rslt_d['Converted_Other'] = rslt_d['Converted_Total'] -\
                                     (convrtdSource_dict['FaceBook']+ convrtdSource_dict['Naukri'])

    rslt_d['% Conversion_Total'] = rslt_d['Converted_Total']/rslt_d['Num_of_Unique_Rows'] * 100
    rslt_d['% Conversion_FaceBook'] = rslt_d['Converted_FaceBook']/rslt_d['Source_Facebook'] *100
    rslt_d['% Conversion_Naukri'] = rslt_d['Converted_Naukri']/rslt_d['Source_Naukri'] * 100
    rslt_d['% Conversion_Other'] = rslt_d['Converted_Other']/ rslt_d['Source_Other'] *100

    for k, v in rslt_d.items():
        print(k, v)
    write_results(rslt_d)

if __name__ == "__main__":
    main()