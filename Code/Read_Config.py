import json
import os

def get_fileNames_wPath(dirPath,fName):
    jsonFile_withPathName = os.path.join(dirPath, fName)
    with open(jsonFile_withPathName, 'r') as inp_file:
        data = json.load(inp_file)

    pymnt_DataFile_wPath = os.path.join(data['inp_related']['Path'],
                                data['inp_related']['PaymentDB_CSVFile'])
    mntlhy_SrcDataFile_wPath = os.path.join(data['inp_related']['Path'],
                                data['inp_related']['Monthly_SourceDataFile'])

    return pymnt_DataFile_wPath, mntlhy_SrcDataFile_wPath

def get_Categorization(dirPath,fName):
    jsonFile_withPathName = os.path.join(dirPath, fName)
    with open(jsonFile_withPathName, 'r') as inp_file:
        data = json.load(inp_file)
    return data
def get_renameDict(dirPath,fName):
    return get_Categorization(dirPath,fName)


def main():
    dirPath = "../ConfigFiles"
    fName = "Input_Config.json"

    mntlhy_SrcDataFile_wPath, pymnt_DataFile_wPath = get_fileNames_wPath(dirPath,fName)
    print (mntlhy_SrcDataFile_wPath)
    print(pymnt_DataFile_wPath)

    fName = "Source_Categorization.json"
    source_category_dict = get_Categorization(dirPath,fName)
    print(source_category_dict)

if __name__ == "__main__":
    main()