def main_menu(filename:str):
    """
    This function manages all
    :param filename: path + filename to csv data file
    :return: None
    """
    option = ''
    options = {
        '1': 'Вывести в понятном виде иерархию команд, т.е. департамент и все команды, которые входят в него',
        '2': 'Вывести сводный отчёт по департаментам: название, численность, "вилка" зарплат в виде мин – макс, среднюю зарплату',
        '3': 'Сохранить сводный отчёт из предыдущего пункта в виде csv-файла. При этом необязательно вызывать сначала команду из п.2',
        '4': 'Завершить программу'
    }
    while option != '4':
        show_options(options)
        option = input()

        show_choosen_option(option)
        if option == '1':
            show_hierarchy(filename)
        elif option == '2':
            report = show_report(filename)
            print('Сводный отчет по департаментам:')
            for keys, values in report.items():
                print(
                    f'Название департамента: {keys.upper()}, численность: {values[0]}, вилка зарплат: {values[1]} - {values[2]}, средняя зарплата: {round(values[3] / values[0], 2)} ')
        elif option == '3':
            save_report(filename)

    print('Программа завершена')



def show_options(options_dict: str):
    """
    Print options that can be chosen
    :param options_dict: Disc with options
    :return: None
    """
    print()
    print(f'Выберите одну из возможных опций:')
    for keys, values in options_dict.items():
        print(f'{keys} : {values}')

def show_choosen_option(option: str):
    """
    Print what option has been chosen
    :param option: An option that has been chosen
    :return: None
    """
    print(f'Выбрана опция {option}')

def show_hierarchy(path: str):
    """
    Show hierarchy of departments and teams like:
    В департамент {departments} входят команды: {team1,team2,team3}
    :param path: path + filename to csv data file
    :return: None
    """

    hierarchy = {}
    with open(path) as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        # This skips the first row of the CSV file.
        next(data)
        for row in data:
            #print(row[1], row[2])
            if row[1] in hierarchy:
                val = hierarchy[row[1]]
                if row[2] not in val:
                    val.append(row[2])
            else:
                hierarchy[row[1]] = [row[2]]
            #print(hierarchy)
    print('Иерархия команд:')
    for keys, values in hierarchy.items():
        print(f'В департамент {keys.upper()} входят команды: {", ".join(values)}')


def show_report(path: str):
    """
    Function calculate and return dict with report data.
    Report includes name of department, count of people in department, min, max, average salary in department
    :param part: path + filename to csv data file
    :return: Dict with report data
    """
    report = {}
    with open(path) as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        # This skips the first row of the CSV file.
        next(data)
        for row in data:
            if row[1] not in report:
                report[row[1]] = [1,int(row[5]), int(row[5]), int(row[5])]
            else:
                val = report[row[1]]
                val[0] += 1
                if int(row[5]) <= val[1]:
                    val[1] = int(row[5])
                if int(row[5]) >= val[2]:
                    val[2] = int(row[5])
                val[3] += int(row[5])
                report[row[1]] = val
    return report


def save_report(path: str):
    """
    This function save report that calculated by show_report function fo csv file.
    Path to result is 'report' plus current date and time  plus.csv
    :param path: path + filename to csv data file
    :return: None
    """
    report_data = show_report(path)
    report_filename = 'report'+str(datetime.datetime.now())+'.csv'
    with open(report_filename, 'w') as csvfile:
        report_writer = csv.writer(csvfile, delimiter=';')
        report_writer.writerow(['Название департамента','Численность','Минимальная зарплата','Максимальная зарплата','Средняя зарплата'])
        for keys, values in report_data.items():
            report_writer.writerow([keys,values[0],values[1],values[2],round(values[3]/values[0], 2)])
    print('Отчет сохранен')

if __name__ == '__main__':
    import csv
    import datetime
    path = '/Users/v23/Desktop/aaa/python/Corp_Summary.csv'
    main_menu(path)


