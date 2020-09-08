import sqlite3

connect = sqlite3.connect("DB.db")
cursor = connect.cursor()

def select_user(id):
    cmd = "SELECT * FROM users WHERE user_id = %d" % id
    cursor.execute(cmd)
    result = cursor.fetchone()
    if result is None:
        return False
    return True

def select_all_from_users(id):
    cmd = "SELECT * FROM users where user_id = %d " % id
    cursor.execute(cmd)
    result = cursor.fetchall()
    return result

def select_where_from_users(id,star, where,what):
    cmd = "SELECT %s FROM users where %s = %s" % (star,where,what)
    cursor.execute(cmd)
    result = cursor.fetchall()
    return result

def insert(id,name,group,room):
        cmd = "INSERT INTO users VALUES (%d,'%s','%s','%s')" % (id,name,group,room)
        cursor.execute(cmd)
        connect.commit()

def set_group(id,group):
    cmd = "UPDATE users SET groups = %s WHERE user_id = %d" % (group, id)
    cursor.execute(cmd)
    connect.commit()

def set_room(id,room):
    cmd = "UPDATE users SET room = %s WHERE user_id = %d" % (room, id)
    cursor.execute(cmd)
    connect.commit()

def none_group(id):
    cmd = "SELECT groups FROM users WHERE user_id = %d" % id
    cursor.execute(cmd)
    result = cursor.fetchone()
    if result[0] == "none":
        return False
    return True


def none_room(id):
    cmd = "SELECT room FROM users WHERE user_id = %d" % id
    cursor.execute(cmd)
    result = cursor.fetchone()
    if result[0] == "none":
        return False
    return True