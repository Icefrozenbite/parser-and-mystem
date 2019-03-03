import os
from pymystem3 import Mystem
import json

root_path = os.path.split(os.path.abspath('File Parser'))[0]


for i in os.walk('plain text'):#Код выполняет mystem
    if len(i[1]) == 0:
        relative_path = i[0]
        date_path = relative_path.split('\\')
        date_path = date_path[1:3]
        date_path = '\\'.join(date_path)

        for file in i[2]:
            path_file = relative_path + '\\' + file
            with open(path_file,'r',encoding='utf-8') as opened_file:
                opened_file = opened_file.read()
                m = Mystem()
                info = m.lemmatize(opened_file)
                lemmas = ''.join(info)
                full_info = json.dumps(m.analyze(opened_file), ensure_ascii=False)
                dir = root_path + '\\' + 'размеченные майстемом тексты' + '\\' + date_path
                file_path = dir + '\\' + file
                print(file)
                try:
                    os.makedirs(dir)
                except:
                    pass
                try:
                    with open(file_path,'a',encoding='utf-8') as file_to_write:
                        file_to_write.write(lemmas)
                        file_to_write.write('\n')
                        file_to_write.write(full_info)
                except:
                    pass











