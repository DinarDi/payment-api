import bcrypt


def hash_password(
        password: str
) -> bytes:
    """
    Function for hash password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)
