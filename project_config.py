import yaml

class ProjectConfig:
    
    def __init__(self):
        try:
            with open('config.yaml') as f:
                config = yaml.safe_load(f)
            
            self.dbname = config['dbname']
            self.user = config['user']
            self.password = config['password']
            self.host = config['host']
            self.dbtableprefix = config['dbtableprefix']
            
        except FileNotFoundError:
            print("Ошибка: файл config.yaml не найден!")
            print("Создайте файл config.yaml с настройками подключения")
            exit(1)
        except KeyError as e:
            print(f"Ошибка в config.yaml: отсутствует ключ {e}")
            exit(1)