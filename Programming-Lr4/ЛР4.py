def set_calculator():
    def read_file(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
            elem = []
            for part in text.replace(',', ' ').split():
                elem.append(part.strip())
            return set(elem)
        except:
            print(f'Файл "{file}" не найден')
            return None

    file1 = input('Путь к первому файлу: ').strip()
    file2 = input('Путь ко второму файлу: ').strip()

    a = read_file(file1)
    b = read_file(file2)

    if a is None or b is None:
        print('Не удалось загрузить одно или оба множества')
        return

    print(f'Множество A: {a}')
    print(f'Множество B: {b}')

    while True:
        print('\nВыберите операцию:')
        print('1 - Объединение')
        print('2 - Пересечение')
        print('3 - Разность (A-B или B-A)')
        print('4 - Симметрическая разность')
        print('0 - Выход')

        choice = input('Введите номер операции: ')

        if choice == '0':
            print('Выход из программы')
            break

        if choice == '1':
            print(f'Результат: {a|b}')
        elif choice == '2':
            print(f'Результат: {a&b}')
        elif choice == '3':
            diff = input('Введите необходимую разность (A-B или B-A): ')
            if diff == 'A-B':
                print(f'Результат: {a-b}')
            if diff == 'B-A':
                print(f'Результат: {b-a}')
        elif choice == '4':
            print(f'Результат: {a^b}')
        else:
            print('Неверный ввод')

set_calculator()
