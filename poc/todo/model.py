from poc.db import get_db


def get_all():
    db = get_db()
    c = db.cursor()
    rows = c.execute('SELECT * FROM `todo`;')
    db.commit()
    return rows.fetchall()


def get_by_id(id):
    db = get_db()
    c = db.cursor()
    rows = c.execute('SELECT * FROM `todo` WHERE `id`=?', (id, ))
    db.commit()
    return rows.fetchone()
