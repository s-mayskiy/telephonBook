MENU_TEXT ="""
Выберите режим работы:
1 - Вывести все данные
2 - Добавить нового пользователя
3 - Поиск по фамилии
4 - Поиск по имени
5 - Поиск по отчеству
6 - Поиск по телефону
7 - Поиск по id
8 - Редактировать запись
9 - Сохранить строку в новый файл
0 - Выход
"""
FIELDS = ["id", "Фамилия", "Имя", "Отчество", "Телефон"]
db_file = "DB.txt"
phone_book = [{"id":-1}]
last_id = 0

def sort_by_surname():
    global phone_book
    phone_book.sort(key=lambda record : ("".join([record[FIELDS[1]],record[FIELDS[2]],record[FIELDS[3]]])))

def insert_single_record(data_list):
    global last_id
    record = dict(zip(FIELDS, data_list))
    phone_book.append(record)      
    if int(record["id"]) > last_id:
        last_id = int(record["id"])

def read_db():         
    with open(db_file, 'r', encoding='utf-8') as reader:
        for line in reader:
            insert_single_record(line[:-1].split(","))
            

def write_db():
    with open(db_file, 'w', encoding='utf-8') as writer:
        for line in phone_book:
            writer.write(",".join(list(line.values()))+"\n")

def output_all():
    sort_by_surname()
    print(FIELDS)
    for line in phone_book:
        print(list(line.values()))


def add_new_record(old_data = [], idx_4_insert=-1 ):
    surname = input("Ведите фамилию" + ( f" (было:{old_data[1]})"  if old_data else "" ) +": ")
    name = input("Введите имя" + ( f" (было:{old_data[2]})"  if old_data else "" ) +": ")
    patronymic = input("Введите отчество" + ( f" (было:{old_data[3]})"  if old_data else "" ) +": ")
    phone_number = input("Ведите телефон" + ( f" (было:{old_data[4]})"  if old_data else "" ) +": ")
    global last_id
    if idx_4_insert == -1:
        last_id += 1
        idx_4_insert = last_id
    insert_single_record([str(idx_4_insert), surname, name, patronymic, phone_number])    


def search_phone_book(field_4_searhc, searching_criteria = ""):    
    res = []    
    for idx, local_dict in enumerate(phone_book):
        if local_dict[FIELDS[field_4_searhc]] == searching_criteria:
            res.append(idx)                        
    return res

def user_search(field_4_searhc):    
    searching_criteria = input(f"Поиск по {FIELDS[field_4_searhc]}, введите критерий поиска: ")        
    found_idx_list = search_phone_book(field_4_searhc, searching_criteria)
    if len(found_idx_list) == 0:
        print("Ничего не было найдено")
    else:
        for found_idx in found_idx_list:
            print(list(phone_book[found_idx].values()))    
    

def edit_record():
    id_4_edit = int(input("Введите id записи для редактирования: "))
    found_idx_list = search_phone_book(0, str(id_4_edit))
    if len(found_idx_list) == 0: 
        print(f"Записи с id {id_4_edit} не существует. Редактирование отменено!")
    else:
        old_data = list(phone_book[found_idx_list[0]].values())
        phone_book.pop(found_idx_list[0])
        add_new_record(old_data, id_4_edit)

def save_in_new_file():
    new_file_name=input("Введите имя файла для сохраннеия: ")
    if new_file_name:
        id_4_copy = input("Введите id строки, которую надо скопировать: ")        
        idx_4_copy_lst = search_phone_book(0,  id_4_copy if id_4_copy else "Пустая строка")        
        if idx_4_copy_lst:
            with open(new_file_name, 'w', encoding='utf-8') as writer:
                writer.write(",".join(list(phone_book[idx_4_copy_lst[0]].values()))+"\n")
        else:
            print("Не найдена строка с id {id_4_copy}")
    else:
        print("Операция отменена!")

def save_adn_or_exit():
    res = False
    choise = input("Выйти с сохранением (д) без сохранения (н), отмена (любой другой ввод)? ")
    if choise == "д":
        res = True
        write_db()
    elif choise == "н":
        res = True
    return res


def main_cycle():
    global db_file
    if phone_book[0]["id"] == -1:
        phone_book.pop(0)
        
        new_db_filename = input(f"Введите им файла. Если ничего не ввести будет использован файл по умлочанию ({db_file})")
        if new_db_filename != "":
            db_file = new_db_filename

        read_db()      

    while True:
        choise = input(MENU_TEXT)
        if choise == '1':
            output_all()
        elif choise == '2':
            add_new_record()
        elif choise == '3':
            user_search(1)
        elif choise == '4':
            user_search(2)
        elif choise == '5':
            user_search(3)
        elif choise == '6':
            user_search(4)
        elif choise == '7':
            user_search(0)                   
        elif choise == '8':
            edit_record()
        elif choise == '9':
            save_in_new_file()            
        elif choise == '0':
            if save_adn_or_exit():
                break
        
        input("нажмите Enter для продолжения")
        

if __name__ == "__main__":
    main_cycle()
