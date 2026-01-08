import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.countries_table import *
from tables.movies_table import *

class Main:
    
    def __init__(self):
        self.config = ProjectConfig()
        self.connection = DbConnection(self.config)
        DbTable.dbconn = self.connection
        
        self.selected_country_name = ""
    
    def db_init(self):
        try:
            ct = CountriesTable()
            mt = MoviesTable()
            ct.create()
            mt.create()
            return True
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            return False
    
    def db_drop(self):
        try:
            mt = MoviesTable()
            ct = CountriesTable()
            mt.drop()
            ct.drop()
            return True
        except Exception as e:
            print(f"Ошибка при удалении таблиц: {e}")
            return False
    
    def show_main_menu(self):
        print("\n" + "="*60)
        print(" КАТАЛОГ ФИЛЬМОВ".center(60))
        print("="*60)
        print("Главное меню:")
        print("  1 - Управление странами")
        print("  2 - Пересоздать таблицы (очистить все данные)")
        print("  9 - Выход")
        print("="*60)
    
    def read_next_step(self):
        return input("\nВыберите действие (1-2, 9): ").strip()
    
    def after_main_menu(self, next_step):
        if next_step == "2":
            print("\n  ВНИМАНИЕ: Все данные будут удалены!")
            confirm = input("Продолжить? (да/нет): ").strip().lower()
            if confirm in ['да', 'д', 'y', 'yes']:
                if self.db_drop():
                    if self.db_init():
                        print(" Таблицы успешно пересозданы!")
                    else:
                        print(" Ошибка при создании таблиц!")
                else:
                    print(" Ошибка при удалении таблиц!")
            else:
                print("Операция отменена.")
            return "0"
        elif next_step == "1":
            return "1"
        elif next_step == "9":
            return "9"
        else:
            print(" Неверный выбор! Пожалуйста, выберите 1, 2 или 9.")
            return "0"
    
    def show_countries_menu(self):
        print("\n" + "="*60)
        print(" УПРАВЛЕНИЕ СТРАНАМИ".center(60))
        print("="*60)
        
        ct = CountriesTable()
        countries = ct.all()
        
        if countries:
            print("\nТекущий список стран:")
            print("-" * 40)
            for idx, country in enumerate(countries, 1):
                print(f"  {idx:2}. {country[1]}")
            print("-" * 40)
            print(f"Всего стран: {len(countries)}")
        else:
            print("\n Список стран пуст.")
        
        print("\nДоступные операции:")
        print("  1 - Добавить новую страну")
        print("  2 - Удалить страну")
        print("  3 - Редактировать название страны")
        print("  4 - Просмотреть фильмы страны")
        print("  0 - Вернуться в главное меню")
        print("  9 - Выход")
        print("="*60)
    
    def process_countries_menu(self):
        while True:
            self.show_countries_menu()
            choice = input("\nВыберите операцию (0-4, 9): ").strip()
            
            if choice == "0":
                return "0"
            elif choice == "1":
                self.add_country()
            elif choice == "2":
                self.delete_country()
            elif choice == "3":
                self.edit_country()
            elif choice == "4":
                result = self.show_country_movies()
                if result in ["0", "9"]:
                    return result
            elif choice == "9":
                return "9"
            else:
                print(" Неверный выбор! Пожалуйста, выберите 0-4 или 9.")
    
    def add_country(self):
        print("\n ДОБАВЛЕНИЕ НОВОЙ СТРАНЫ")
        print("-" * 40)
        
        while True:
            name = input("Введите название страны (или '0' для отмены): ").strip()
            
            if name == '0':
                print("Операция отменена.")
                return
            
            if not name:
                print(" Название не может быть пустым!")
                continue
            
            ct = CountriesTable()
            if ct.check_name_exists(name):
                print(f" Страна '{name}' уже существует!")
                continue
            
            try:
                ct.insert_one([name])
                print(f" Страна '{name}' успешно добавлена!")
                break
            except Exception as e:
                print(f" Ошибка при добавлении: {e}")
                retry = input("Попробовать снова? (да/нет): ").strip().lower()
                if retry not in ['да', 'д', 'y', 'yes']:
                    return
    
    def delete_country(self):
        print("\n  УДАЛЕНИЕ СТРАНЫ")
        print("-" * 40)
        
        ct = CountriesTable()
        countries = ct.all()
        
        if not countries:
            print(" Нет стран для удаления.")
            return
        
        print("\nСписок стран:")
        for idx, country in enumerate(countries, 1):
            print(f"  {idx:2}. {country[1]}")
        
        while True:
            choice = input("\nВведите номер или название страны (или '0' для отмены): ").strip()
            
            if choice == '0':
                print("Операция отменена.")
                return
            
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(countries):
                    country_name = countries[num-1][1]
                else:
                    print(f" Номер должен быть от 1 до {len(countries)}!")
                    continue
            else:
                country_name = choice
                if not ct.find_by_name(country_name):
                    print(f" Страна '{country_name}' не найдена!")
                    continue
            
            movies_count = ct.get_country_movies_count(country_name)
            if movies_count > 0:
                print(f"  У страны '{country_name}' есть {movies_count} фильм(ов).")
                print("Все связанные фильмы будут удалены автоматически!")
                confirm = input(f"Удалить страну '{country_name}'? (да/нет): ").strip().lower()
                if confirm not in ['да', 'д', 'y', 'yes']:
                    print("Удаление отменено.")
                    continue
            else:
                confirm = input(f"Удалить страну '{country_name}'? (да/нет): ").strip().lower()
                if confirm not in ['да', 'д', 'y', 'yes']:
                    print("Удаление отменено.")
                    continue
            
            try:
                deleted = ct.delete_by_name(country_name)
                if deleted > 0:
                    print(f" Страна '{country_name}' успешно удалена!")
                    break
                else:
                    print(" Не удалось удалить страну.")
            except Exception as e:
                print(f" Ошибка при удалении: {e}")
            
            retry = input("Попробовать снова? (да/нет): ").strip().lower()
            if retry not in ['да', 'д', 'y', 'yes']:
                return
    
    def edit_country(self):
        print("\n  РЕДАКТИРОВАНИЕ СТРАНЫ")
        print("-" * 40)
        
        ct = CountriesTable()
        countries = ct.all()
        
        if not countries:
            print(" Нет стран для редактирования.")
            return
        
        print("\nСписок стран:")
        for idx, country in enumerate(countries, 1):
            print(f"  {idx:2}. {country[1]}")
        
        while True:
            old_name = input("\nВведите название редактируемой страны (или '0' для отмены): ").strip()
            
            if old_name == '0':
                print("Операция отменена.")
                return
            
            if old_name.isdigit():
                num = int(old_name)
                if 1 <= num <= len(countries):
                    old_name = countries[num-1][1]
                else:
                    print(f" Номер должен быть от 1 до {len(countries)}!")
                    continue
            
            if not ct.find_by_name(old_name):
                print(f" Страна '{old_name}' не найдена!")
                continue
            
            while True:
                new_name = input(f"Введите новое название для '{old_name}' (или '0' для отмены): ").strip()
                
                if new_name == '0':
                    print("Редактирование отменено.")
                    return
                
                if not new_name:
                    print(" Название не может быть пустым!")
                    continue
                
                if new_name.lower() == old_name.lower():
                    print(" Новое название совпадает со старым!")
                    continue
                
                if ct.check_name_exists(new_name):
                    print(f" Страна '{new_name}' уже существует!")
                    continue
                
                try:
                    updated = ct.update_by_name(old_name, new_name)
                    if updated > 0:
                        print(f" Страна успешно переименована: '{old_name}' → '{new_name}'")
                        
                        if self.selected_country_name.lower() == old_name.lower():
                            self.selected_country_name = new_name
                        
                        break
                    else:
                        print(" Не удалось обновить страну.")
                except Exception as e:
                    print(f" Ошибка при обновлении: {e}")
                
                retry = input("Попробовать снова? (да/нет): ").strip().lower()
                if retry not in ['да', 'д', 'y', 'yes']:
                    return
            
            break
    
    def show_country_movies(self):
        print("\n ФИЛЬМЫ СТРАНЫ")
        print("-" * 40)
        
        ct = CountriesTable()
        countries = ct.all()
        
        if not countries:
            print(" Нет стран для просмотра фильмов.")
            return "0"
        
        print("\nВыберите страну:")
        for idx, country in enumerate(countries, 1):
            print(f"  {idx:2}. {country[1]}")
        
        while True:
            choice = input("\nВведите номер или название страны (или '0' для отмены): ").strip()
            
            if choice == '0':
                return "0"
            
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(countries):
                    self.selected_country_name = countries[num-1][1]
                else:
                    print(f" Номер должен быть от 1 до {len(countries)}!")
                    continue
            else:
                self.selected_country_name = choice
                if not ct.find_by_name(self.selected_country_name):
                    print(f" Страна '{self.selected_country_name}' не найдена!")
                    continue
            
            return self.show_movies_menu()
    
    def show_movies_menu(self):
        while True:
            print(f"\n" + "="*60)
            print(f" ФИЛЬМЫ СТРАНЫ: {self.selected_country_name}".center(60))
            print("="*60)
            
            mt = MoviesTable()
            movies = mt.all_by_country_name(self.selected_country_name)
            
            if movies:
                print(f"\nВсего фильмов: {len(movies)}")
                print("-" * 60)
                print(f"{'№':3} {'Название':30} {'Год':6} {'Длит.':7} {'Возраст':8}")
                print("-" * 60)
                for idx, movie in enumerate(movies, 1):
                    print(f"{idx:3} {movie[1]:30} {movie[2]:6} {movie[4]:7} {movie[5]:8}+")
                print("-" * 60)
            else:
                print("\n Фильмов нет.")
            
            print("\nДоступные операции:")
            print("  1 - Добавить фильм")
            print("  2 - Удалить фильм")
            print("  0 - Вернуться к выбору страны")
            print("  9 - Выход из программы")
            print("="*60)
            
            choice = input("\nВыберите операцию (0-2, 9): ").strip()
            
            if choice == "0":
                return "0"
            elif choice == "1":
                self.add_movie()
            elif choice == "2":
                self.delete_movie()
            elif choice == "9":
                return "9"
            else:
                print(" Неверный выбор! Пожалуйста, выберите 0-2 или 9.")
    
    def add_movie(self):
        print(f"\n ДОБАВЛЕНИЕ ФИЛЬМА ДЛЯ СТРАНЫ: {self.selected_country_name}")
        print("-" * 50)
        
        while True:
            try:
                title = input("Название фильма (или '0' для отмены): ").strip()
                if title == '0':
                    print("Операция отменена.")
                    return
                
                if not title:
                    print(" Название не может быть пустым!")
                    continue
                
                year_str = input("Год выпуска: ").strip()
                if not year_str.isdigit():
                    print(" Год должен быть числом!")
                    continue
                
                year = int(year_str)
                
                duration_str = input("Продолжительность (минут): ").strip()
                if not duration_str.isdigit():
                    print(" Продолжительность должна быть числом!")
                    continue
                
                duration = int(duration_str)
                
                min_age_str = input("Минимальный возраст: ").strip()
                if not min_age_str.isdigit():
                    print(" Возраст должен быть числом!")
                    continue
                
                min_age = int(min_age_str)
                
                mt = MoviesTable()
                mt.insert_for_country(title, year, self.selected_country_name, duration, min_age)
                print(f" Фильм '{title}' успешно добавлен!")
                break
                
            except ValueError:
                print(" Ошибка ввода! Убедитесь, что вводите числа для года, продолжительности и возраста.")
            except Exception as e:
                print(f" Ошибка при добавлении фильма: {e}")
                if "не найдена" in str(e):
                    print(" Выбранная страна больше не существует!")
                    print("Вернитесь к выбору страны.")
                    return
            
            retry = input("Попробовать снова? (да/нет): ").strip().lower()
            if retry not in ['да', 'д', 'y', 'yes']:
                return
    
    def delete_movie(self):
        print(f"\n  УДАЛЕНИЕ ФИЛЬМА ИЗ СТРАНЫ: {self.selected_country_name}")
        print("-" * 50)
        
        mt = MoviesTable()
        movies = mt.all_by_country_name(self.selected_country_name)
        
        if not movies:
            print(" Нет фильмов для удаления.")
            return
        
        print("\nСписок фильмов:")
        for idx, movie in enumerate(movies, 1):
            print(f"  {idx:2}. {movie[1]} ({movie[2]})")
        
        while True:
            choice = input("\nВведите номер фильма для удаления (или '0' для отмены): ").strip()
            
            if choice == '0':
                print("Операция отменена.")
                return
            
            if not choice.isdigit():
                print(" Введите число!")
                continue
            
            num = int(choice)
            
            try:
                deleted = mt.delete_by_position_and_country(num, self.selected_country_name)
                if deleted > 0:
                    print(" Фильм успешно удалён!")
                    break
                else:
                    print(" Фильм не найден!")
            except Exception as e:
                print(f" Ошибка при удалении: {e}")
            
            retry = input("Попробовать снова? (да/нет): ").strip().lower()
            if retry not in ['да', 'д', 'y', 'yes']:
                return
    
    def run(self):
        print("\n" + "="*60)
        print(" ЗАПУСК КАТАЛОГА ФИЛЬМОВ".center(60))
        print("="*60)
        print("Проверка подключения к базе данных...")
        
        if not self.connection.test_connection():
            print("Не удалось подключиться к базе данных!")
            print("Проверьте настройки в файле config.yaml")
            return
        
        print("Подключение к базе данных успешно!")
        
        current_menu = "0"
        
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            
            elif current_menu == "1":
                current_menu = self.process_countries_menu()
        
        print("\n" + "="*60)
        print("До свидания! Спасибо за использование каталога фильмов!".center(60))
        print("="*60)

if __name__ == "__main__":
    try:
        app = Main()
        app.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\n Критическая ошибка: {e}")
        print("Проверьте настройки подключения к базе данных.")