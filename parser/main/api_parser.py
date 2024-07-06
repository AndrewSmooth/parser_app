import requests
import json 
import os
import shutil   

class HhParser():
    
    def __init__(self):
        self.__employment = {
            'full': 'полная',
            'part': 'частичная',
            'probation': 'стажировка',
            'project': 'проектная работа',
            'volunteer': 'волонтерство',
        }

        self.__experience = {
            'between1And3': 'от 1 года до 3 лет',
            'between3And6': 'от 3 до 6 лет',
            'moreThan6': 'больше 6 лет',
            'noExperience': 'без опыта',
        }
    
    def getEmployment(self):
        return self.__employment
    
    def getExperience(self):
        return self.__experience

    def getAreas(self):
        req = requests.get('https://api.hh.ru/areas')    
        data = req.content.decode()
        req.close()
        jsObj = json.loads(data)
        areas = []
        for k in jsObj:
            for i in range(len(k['areas'])):
                if len(k['areas'][i]['areas']) != 0:                      # Если у зоны есть внутренние зоны
                    for j in range(len(k['areas'][i]['areas'])):
                        areas.append([k['id'], 
                                    k['name'], 
                                    k['areas'][i]['areas'][j]['id'],
                                    k['areas'][i]['areas'][j]['name']])
                else:                                                      # Если у зоны нет внутренних зон
                    areas.append([k['id'], 
                                k['name'], 
                                k['areas'][i]['id'], 
                                k['areas'][i]['name']])
        return areas

    def getProfRoles(self):
        req = requests.get('https://api.hh.ru/professional_roles')    
        data = req.content.decode()
        req.close()
        jsObj = json.loads(data)
        profRolesDict = {}
        for k in jsObj['categories']:
            for r in k['roles']:
                profRolesDict[r['id']] = r['name']
        
        profRoles = {}
        temp = []
        
        for key, val in profRolesDict.items():
        
            if val not in temp:
                temp.append(val)
                profRoles[key] = val

        return profRoles

    def getPagesCount(self, line):
        for el in line.split(','):
            if 'pages' in el:
                return int(el.split(':')[-1])
        return
                
    def parse(self, employment, experience, area, profRole):
        params = {
            'area': area,         
            'per_page': 100,      
            'professional_role': profRole,
            'experience': experience,
            'employment': employment,
        }   

        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode() 
        req.close()

        print(data[-400:-1])

        pagesCount = self.getPagesCount(data[-400:-1])
    
        #delete areas folder
        dir_path = 'areas'

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        for i in range(pagesCount):
            params['page'] = i
            req = requests.get('https://api.hh.ru/vacancies', params, )
            data = req.content.decode()
            req.close()

            jsObj = json.loads(data)

            if not os.path.exists('./areas/'):
                os.makedirs('./areas/')

            nextFileName = './areas/{}.json'.format(str(i))
            f = open(nextFileName, mode='w', encoding='utf8')
            f.write(json.dumps(jsObj, ensure_ascii=False))
            f.close()

        dt = []
        for fl in os.listdir('./areas/'):
            f = open('./areas/{}'.format(fl), encoding='utf8')
            jsonText = f.read()
            f.close()
            jsonObj = json.loads(jsonText)
            if jsonObj['found'] != 0:
                for js in jsonObj['items']:
                    if js['address']:
                        address = js['address']
                        if address['raw']:
                            address = address['raw']
                        elif address['metro']['station_name']:
                            address = address['metro']['station_name']
                    else:
                        address = None
                    
                    salary = js['salary']
                    if salary:
                        if salary['from'] and salary['to']:
                            salary = 'от ' + str(salary['from']) + ' до ' + str(salary['to'])
                        else:
                            if salary['from']:
                                salary = 'от ' + str(salary['from'])
                            else:
                                salary = 'до ' + str(salary['to'])
                        if js['salary']['currency']:
                            salary += ' ' + js['salary']['currency']
                            salary = salary.replace('(', '').replace(')', '')

                    dt.append([
                        js['name'],
                        address,
                        js['employer']['name'],
                        salary,
                        js['employment']['name'],
                        js['experience']['name'],
                        js['area']['name'],
                        js['professional_roles'][0]['name'],
                        ])
        return dt
