
import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('cb_housebot.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их
        Важно: миграции на такие таблицы вы должны производить самостоятельно!
        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS users')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER UNIQUE,
            invite_code TEXT UNIQUE,
            limit_code  INTEGER,
            invited_users TEXT
        )
    ''')
    # Сохранить изменения
    conn.commit()


@ensure_connection
def add_tg_id(conn, user_id: int):
    c = conn.cursor()
    c.execute('INSERT INTO users (tg_id) VALUES (?)', (user_id, ))
    conn.commit()

@ensure_connection
def set_invite_code(conn, user_invite_code: str, user_tg_id: int):
    c = conn.cursor()
    c.execute('UPDATE users SET invite_code = ? WHERE tg_id = ?', (user_invite_code, user_tg_id))
    conn.commit()


@ensure_connection
def set_limit_code(conn, user_limit_code: int, user_tg_id: int):
    c = conn.cursor()
    c.execute('UPDATE users SET limit_code = ? WHERE tg_id = ?', (user_limit_code, user_tg_id))
    conn.commit()


@ensure_connection
def use_invite_code(conn, user_tg_id: str, user_invite_code: str):
    c = conn.cursor()
    c.execute('SELECT invite_code FROM users')
    inviteCodes = [i[0] for i in c.fetchall()]
    if user_invite_code in inviteCodes:
        c.execute('SELECT limit_code FROM users WHERE invite_code = ?', (user_invite_code, ))
        limit = c.fetchone()[0]
        if limit != 0:
            c.execute('UPDATE users SET limit_code = limit_code-1 WHERE invite_code = ?', (user_invite_code, ))
            c.execute('SELECT invited_users FROM users WHERE invite_code = ?', (user_invite_code, ))
            if c.fetchone()[0] == None:
                c.execute('UPDATE users SET invited_users = ? WHERE invite_code = ?', (user_tg_id, user_invite_code))
            else:
                c.execute('SELECT invited_users FROM users WHERE invite_code = ?', (user_invite_code, ))
                invited_users = ', '.join(i[0] for i in c.fetchall())
                c.execute('UPDATE users SET invited_users = ? WHERE invite_code = ?',
                          (invited_users + ', ' + str(user_tg_id), user_invite_code))
            return True
        else:
            return 'limit = 0'
    else:
        return False # 0 значит не работает


########################################################################################################################

@ensure_connection
def select_invite_code(conn, user_tg_id: int):
    c = conn.cursor()
    c.execute('SELECT invite_code FROM users WHERE tg_id = ?', (user_tg_id, ))
    return c.fetchone()[0]


@ensure_connection
def select_invited_users(conn, user_tg_id: int):
    c = conn.cursor()
    c.execute('SELECT invited_users FROM users WHERE tg_id = ?', (user_tg_id, ))
    return [i[0] for i in c.fetchall()]

@ensure_connection
def print_admin_invite(conn):
    c = conn.cursor()
    c.execute('SELECT invite_code FROM users WHERE tg_id = ?', (123, ))
    return c.fetchone()[0]