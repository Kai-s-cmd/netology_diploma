import psycopg2


class VkDB:
    """Создает базу данных и записывает пользователей отобранных
     в search_users"""
    with psycopg2.connect(database="sorted_users",
                          user="postgres", password="123456") as conn:

        @staticmethod
        def create_db(conn=conn):
            """Метод создает стол sorted_users в ДБ sorted_users"""

            with conn.cursor() as cur:
                cur.execute('''
                CREATE TABLE IF NOT EXISTS sorted_users(
                    id serial primary key,
                    contacted_id INTEGER,
                    viewed_id INTEGER,
                    name varchar(200)
                );
                ''')
                conn.commit()

        @staticmethod
        def add_client(contacted_id, viewed_id, name, conn=conn):
            """Метод добавляет просмотренного пользователя в ДБ."""

            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO sorted_users(contacted_id, viewed_id, name) 
                    VALUES
                        (%s, %s, %s) RETURNING id;
                ''', (contacted_id, viewed_id, name)
                            )
                conn.commit()
                return 'Пользователь добавлен в базу!'

        @staticmethod
        def find_client(contacted_id, viewed_id, conn=conn):
            """Метод ищет клиента в ДБ sorted_users."""

            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT contacted_id, viewed_id FROM sorted_users
                    WHERE contacted_id = {contacted_id} and viewed_id = {viewed_id};
                """
                            )
                conn.commit()
                return cur.fetchone()
