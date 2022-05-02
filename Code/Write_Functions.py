import os
import csv

# Function to store processing result file
def write_resultDict(opdir, fName,headers,outcome_dict):
    check_n_create_dir(opdir)

    outcome_fName_wPath = os.path.join(opdir, fName)

    file_exists = os.path.isfile(outcome_fName_wPath)

    with open(outcome_fName_wPath, "a") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',
                                fieldnames=headers)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header

        writer.writerow(outcome_dict)


# Function to create intermediate directory
def check_n_create_dir(dir2check):
    # Make directory if does not exist
    if not os.path.isdir(dir2check):
        os.makedirs(dir2check)

def write_results(result_dict):
    opDir = '../Result'
    fName = 'ConversionAnalysis_Result.csv'
    header = ['File_Processed','Processed_At',
              'Num_of_Rows','Num_of_Unique_Rows',
              'Source_Facebook','Source_Naukri','Source_Other',
              'Converted_Total','Converted_FaceBook',
              'Converted_Naukri','Converted_Other',
              '% Conversion_Total', '% Conversion_FaceBook',
              '% Conversion_Naukri', '% Conversion_Other'
              ]
    write_resultDict(opDir, fName, header,result_dict)




