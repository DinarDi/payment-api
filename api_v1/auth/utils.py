import bcrypt


def hash_password(
        password: str
) -> bytes:
    """
    Function for hash password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    """
    Function to check password
    :param password: str
    :param hashed_password: bytes
    :return: True | False
    """
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
