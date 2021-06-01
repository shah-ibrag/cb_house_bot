import string
import random

def random_password_generator():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = 0
    return 'cbhouse_bot_' + ''.join(random.choice(chars) for x in range(size, 20))

