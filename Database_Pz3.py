import mysql.connector
from mysql.connector import Error


class SQLTable:
    def __init__(self, db_config, table_name):
        self.db_config = db_config
        self.table_name = table_name
        self.columns = []
        self.connection = None
        self.cursor = None
        self._connect()
        if self._check_table_exists():
            self._update_column_names()

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Ошибка подключения: {e}")
            self.connection = None
            self.cursor = None

    def _ensure_connection(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self._connect()
            return self.connection is not None
        except:
            self._connect()
            return self.connection is not None

    def _check_table_exists(self):
        if not self._ensure_connection():
            return False
        query = f"SHOW TABLES LIKE '{self.table_name}'"
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    def _update_column_names(self):
        if not self._ensure_connection():
            return
        query = f"SHOW COLUMNS FROM {self.table_name}"
        self.cursor.execute(query)
        self.columns = [row[0] for row in self.cursor.fetchall()]

    def create_table(self, columns):
        if not self._ensure_connection():
            return
        column_definition = ', '.join(f"`{name}` {type}" for name, type in columns.items())
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            {column_definition}
        )
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print(f"Таблица '{self.table_name}' успешно создана")
        except Error as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            cursor.close()
        self._update_column_names()

    def insert_row(self, data):
        if not self._ensure_connection():
            print("Нет подключения к БД")
            return None

        columns = ', '.join(f"`{k}`" for k in data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
            inserted_id = cursor.lastrowid
            print(f"Данные успешно вставлены. : {inserted_id}")
            return inserted_id
        except Error as e:
            print(f"Ошибка при вставке: {e}")
            return None
        finally:
            cursor.close()

    def get_all(self):
        if not self._ensure_connection():
            return []

        query = f"SELECT * FROM {self.table_name}"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"Получено записей: {len(results)}")
            return results
        except Error as e:
            print(f"Ошибка при получении данных: {e}")
            return []
        finally:
            cursor.close()

    def find(self, conditions, limit=None):
        if not self._ensure_connection():
            return []

        where_clauses = [f"`{k}` = %s" for k in conditions.keys()]
        where_string = " AND ".join(where_clauses)
        values = tuple(conditions.values())

        query = f"SELECT * FROM {self.table_name} WHERE {where_string}"
        if limit:
            query += f" LIMIT {limit}"

        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, values)
            results = cursor.fetchall()
            print(f"Найдено записей по условию: {len(results)}")
            return results
        except Error as e:
            print(f"Ошибка при поиске: {e}")
            return []
        finally:
            cursor.close()

    def delete_all(self):
        if not self._ensure_connection():
            return False

        query = f"TRUNCATE TABLE {self.table_name}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print(f"Все записи из таблицы {self.table_name} удалены")
            return True
        except Error as e:
            print(f"Ошибка при удалении всех записей: {e}")
            return False
        finally:
            cursor.close()

    def count(self):
        if not self._ensure_connection():
            return 0

        query = f"SELECT COUNT(*) as count FROM {self.table_name}"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            return result['count'] if result else 0
        except Error as e:
            print(f"Ошибка при подсчете записей: {e}")
            return 0
        finally:
            cursor.close()

    def is_connected(self):
        return self._ensure_connection()

    def close_connection(self):
        try:
            if hasattr(self, 'cursor') and self.cursor is not None:
                try:
                    self.cursor.close()
                except:
                    pass
                finally:
                    self.cursor = None

            if hasattr(self, 'connection') and self.connection is not None and self.connection.is_connected():
                try:
                    self.connection.close()
                    print(f"Соединение с БД (таблица {self.table_name}) закрыто")
                except:
                    pass
                finally:
                    self.connection = None
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def __del__(self):
        try:
            self.close_connection()
        except:
            pass


db_config = {
    'user': 'j30084097_137',
    'password': 'Gruppa137',
    'host': 'srv221-h-st.jino.ru',
    'database': 'j30084097_137'
}

with SQLTable(db_config, 'nika') as nika_table:

    student = nika_table.insert_row({
        'Name': 'Иван',
        'Age': 20,
        'City': 'Омск'
    })

all_users = nika_table.get_all()
for user in all_users:
    print(f"Имя: {user['Name']}, Возраст: {user['Age']}, Город: {user['City']}")

    moscow_users = nika_table.find({'City': 'Москва'})
    print(f"Найдено пользователей из Москвы: {len(moscow_users)}")

    total = nika_table.count()
    print(f"Всего записей в таблице: {total}")
    