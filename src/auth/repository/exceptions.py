from ...exceptions import RepositoryException


class UserAlreadyExistException(RepositoryException):
    """ 이미 DB에 존재합니다 """
