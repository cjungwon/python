import os
import pandas as pd

class FileInfo:
    def __init__(self, directory):
        self.directory = directory

        self.file_name_list = os.listdir(directory)

        self.file_extension_list = []
        self.file_size_list = []

        for f in self.file_name_list:
            self.file_extension_list.append( f[slice(f.rfind(".") + 1, len(f))] )
            
            file_size_byte = os.path.getsize(self.directory + '/' + f)
            file_size_KB = round(file_size_byte / 1024, 4)
            self.file_size_list.append(str(file_size_KB) + ' KB')

    def file_name(self):       
        return self.file_name_list

    def file_extension(self):
        return self.file_extension_list

    def file_size(self):
        return self.file_size_list
    
    def merge(self):
        merged = []
        cnt = 0
        for n in range(len(self.file_name_list)):
            merged.append( [self.file_name_list[cnt], self.file_extension_list[cnt], self.file_size_list[cnt] ] )
            cnt += 1
        return merged


# directory = 'd:/id_card'
info = FileInfo('d:/id_card')

print(info.merge())