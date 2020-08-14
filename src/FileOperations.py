import shutil
from pathlib import Path, PurePath
import os
import zipfile
from ruamel.yaml import YAML


class FileOperations:
    '''
    Extract directory extracts the .csar file
    Param: file name .csar extension
    '''
    def unzip_csar(self,dir_name,temp_Dir):
        try:
            with zipfile.ZipFile(dir_name, "r") as zip_ref:
                zip_ref.extractall(temp_Dir)
        except FileNotFoundError as File_error:
            print("File Not Found....Please Check the file name and File Path")

    '''
    After files has been extracted using extract_dir 
    read_tosca_meta reads the Metadata to find the entry point
    returns: Entry point file name
    '''
    def read_tosca_meta_file(self,temp_Dir):
        lines = open(Path(temp_Dir,"TOSCA-Metadata/TOSCA.meta"), "r").readlines()
        for line in lines:
            search_entry_point = line.split(':')
            if search_entry_point[0] == 'Entry-Definitions':
                return  search_entry_point[1].strip()

    '''
    read_file opens the entry file to make required modifications
    in it
    '''
    def read_file(self,filename):
        mydoc = open(filename, "r")
        yaml = YAML(typ='safe')
        yaml.default_flow_style = False
        return yaml, yaml.load(mydoc)


    '''
    Param:
        yaml-> ruamel.yaml object
        file_content-> content of tosca/yaml file
        file_name-> file_name to write modified data in
    '''
    def write_file(self,yaml, file_content, file_name):
        yaml_file = open(file_name, "w")
        yaml.dump(file_content, yaml_file)
        yaml_file.close()


    def zip_csar(self,dir_name,temp_Dir):
        try:
            count = 0
            modified_dir = './'+dir_name+'_modified'
            fileType = '.csar'
            while Path(modified_dir + fileType).exists():
                count += 1
                modified_dir += '(' + str(count) + ')'
            os.remove(Path(temp_Dir,'root_file'))
            shutil.copytree(temp_Dir, modified_dir + fileType)
            shutil.rmtree(temp_Dir)
        except FileExistsError as File_Exists:
            print('File already Exists....Please delete the modified folder')
