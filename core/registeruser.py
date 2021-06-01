from core import db
from resources import invitegen


def new_user(id):
    db.add_tg_id(user_id=id)
    db.set_invite_code(user_invite_code=invitegen.random_password_generator(), user_tg_id=id)
    db.set_limit_code(user_limit_code=2, user_tg_id=id)