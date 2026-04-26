import psycopg2
from psycopg2.extras import RealDictCursor

db_config = {
    ###############
}

class SQLTable:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            if self.connection is None or self.connection.closed != 0:
                self.connection = psycopg2.connect(**self.config)
                self.connection.autocommit = False
                print('Подключение к базе данных установлено')
        except:
            print('Ошибка подключения')
            raise

    def disconnect(self):
        if self.connection and self.connection.closed == 0:
            self.connection.close()
            print('Соединение отключено')

    def execute_query(self, query, param=None):
        cursor = None
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, param)
            self.connection.commit()
            count = cursor.rowcount
            print(f'Запрос выполнен успешно. Затронуто строк: {count}')
            return count
        except:
            print(f'Ошибка при выполнении запроса')
            self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def filter(self, filters):
        where = []
        values = []
        for key in filters:
            operat = filters[key]['operat']
            znach = filters[key]['znach']
            where.append(f'{key} {operat} %s')
            values.append(znach)
        condition = ' AND '.join(where)
        return condition, values

    def select(self, query, filters=None):
        cursor = None
        try:
            self.connect()
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            param = []
            if filters:
                condition, param = self.filter(filters)
                query = query + ' WHERE ' + condition

            cursor.execute(query, param)

            result = []
            for elem in cursor.fetchall():
                result.append(dict(elem))
            print(f'SELECT выполнен. Получено строк: {len(result)}')
            return result
        except:
            print(f'Ошибка SELECT')
            self.connection.rollback()
            return []
        finally:
            if cursor:
                cursor.close()

    def insert(self, table, data):
        colum = []
        param = []
        for key, val in data.items():
            colum.append(key)
            param.append(val)
        columns_str = ', '.join(colum)
        shablon = ', '.join(['%s'] * len(colum))
        query = f'INSERT INTO {table} ({columns_str}) VALUES ({shablon}) RETURNING id'
        cursor = None
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, param)
            self.connection.commit()
            new_id = cursor.fetchone()[0]
            print(f'Добавлена запись в таблицу {table}. id: {new_id}')
            return new_id
        except:
            print(f'Ошибка INSERT')
            self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def update(self, table, data, filters=None):
        set_str = ''
        set_values = []
        for key in data:
            set_str += f'{key} = %s, '
            set_values.append(data[key])
        set_str = set_str[:-2]

        if filters:
            condition, values = self.filter(filters)
            query = f'UPDATE {table} SET {set_str} WHERE {condition}'
            param = set_values + values
        else:
            print('UPDATE без WHERE обновит все строки')
            query = f'UPDATE {table} SET {set_str}'
            param = set_values
        return self.execute_query(query, param)

    def delete(self, table, filters=None):
        if filters:
            condition, values = self.filter(filters)
            query = f'DELETE FROM {table} WHERE {condition}'
            return self.execute_query(query, values)
        else:
            print('DELETE без WHERE удалит все строки')
            return self.execute_query(f'DELETE FROM {table}')

    def create_table(self, table, columns):
        cursor = None
        try:
            conn = psycopg2.connect(**self.config)
            conn.autocommit = True
            cursor = conn.cursor()
            query = f'CREATE TABLE IF NOT EXISTS {table} ({columns})'
            cursor.execute(query)
            print(f'Таблица {table} создана (или уже существует)')
        except:
            print(f'Не удалось создать таблицу {table}')
        finally:
            if cursor:
                cursor.close()

    def drop_table(self, table):
        cursor = None
        try:
            conn = psycopg2.connect(**self.config)
            conn.autocommit = True
            cursor = conn.cursor()
            query = f'DROP TABLE IF EXISTS {table}'
            cursor.execute(query)
            print(f'Таблица {table} удалена (или не существовала)')
        except :
            print(f'Не удалось удалить таблицу {table}')
        finally:
            if cursor:
                cursor.close()

    def join(self, table1, table2, condition, join_type='', columns='', filters=None):
        query = f'SELECT {columns} FROM {table1} {join_type} JOIN {table2} ON {condition}'
        return self.select(query, filters=filters)

    def union(self, query1, query2, filters1=None, filters2=None, duplicates=False):
        if duplicates:
            union_query = 'UNION ALL'
        else:
            union_query = 'UNION'

        param1 = []
        param2 = []

        if filters1:
            condition1, param1 = self.filter(filters1)
            query1 = query1 + ' WHERE ' + condition1
        if filters2:
            condition2, param2 = self.filter(filters2)
            query2 = query2 + ' WHERE ' + condition2

        query = f'{query1} {union_query} {query2}'
        all_params = param1 + param2

        cursor = None
        try:
            self.connect()
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, all_params)
            result = []
            for elem in cursor.fetchall():
                result.append(dict(elem))
            print(f'UNION выполнен. Получено строк: {len(result)}')
            return result
        except:
            print(f'Ошибка UNION')
        finally:
            if cursor:
                cursor.close()

'''Проверка работы'''
db = SQLTable(db_config)

# Создание таблиц
db.create_table('people', 'id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, age INT')
db.create_table('orders', 'id SERIAL PRIMARY KEY, people_id INT, product VARCHAR(100)')
print()

# Добавление данных в таблицы
id1 = db.insert('people', {'name': 'Катя', 'age': 18})
id2 = db.insert('people', {'name': 'Иван', 'age': 57})
id3 = db.insert('people', {'name': 'Маша', 'age': 32})
print()

db.insert('orders', {'people_id': id3, 'product': 'Сок'})
db.insert('orders', {'people_id': id2, 'product': 'Бумага'})
db.insert('orders', {'people_id': id1, 'product': 'Книга'})
print()


print('Люди старше 30 лет:')
result = db.select('SELECT * FROM people', filters={'age': {'operat': '>', 'znach': 30}})
for row in result:
    print(f'  id: {row['id']}, имя: {row['name']}, возраст: {row['age']}')
print()


print('UPDATE:')
db.update('people', {'age': 30}, filters={'id': {'operat': '=', 'znach': id2}})
print()


print('INNER JOIN:')
result = db.join('people', 'orders',
    'orders.people_id = people.id', join_type='INNER',
    columns='people.id AS people_id, people.name, people.age, orders.id AS order_id, orders.product')
for row in result:
    print(f'  people_id: {row['people_id']}, имя: {row['name']}, возраст: {row['age']}, order_id: {row['order_id']}, товар: {row['product']}')
print()


print('LEFT JOIN:')
result = db.join('people', 'orders',
    'orders.people_id = people.id', join_type='LEFT',
    columns='people.id AS people_id, people.name, people.age, orders.id AS order_id, orders.product')
for row in result:
    print(f'  people_id: {row['people_id']}, имя: {row['name']}, возраст: {row['age']}, order_id: {row['order_id']}, товар: {row['product']}')
print()


print('RIGHT JOIN:')
result = db.join(
    'people', 'orders',
    'orders.people_id = people.id', join_type='RIGHT',
    columns='people.id AS people_id, people.name, people.age, orders.id AS order_id, orders.product')
for row in result:
    print(f'  people_id: {row['people_id']}, имя: {row['name']}, возраст: {row['age']}, order_id: {row['order_id']}, товар: {row['product']}')
print()


print('FULL JOIN:')
result = db.join(
    'people', 'orders',
    'orders.people_id = people.id', join_type='FULL',
    columns='people.id AS people_id, people.name, people.age, orders.id AS order_id, orders.product')
for row in result:
    print(f'  people_id: {row['people_id']}, имя: {row['name']}, возраст: {row['age']}, order_id: {row['order_id']}, товар: {row['product']}')
print()


print('UNION (моложе 20 или старше 50):')
result = db.union(
    'SELECT * FROM people',
    'SELECT * FROM people',
    filters1={'age': {'operat': '<', 'znach': 20}},
    filters2={'age': {'operat': '>', 'znach': 50}})
for row in result:
    print(f'  id: {row['id']}, имя: {row['name']}, возраст: {row['age']}')
print()


print('DELETE:')
db.delete('people', filters={'id': {'operat': '=', 'znach': id3}})
print()

# Удаление таблицы people
# db.drop_table('people')
# print()

# Удаление таблицы orders
# db.drop_table('orders')
# print()

db.disconnect()
