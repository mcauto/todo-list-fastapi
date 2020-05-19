from ....core.exceptions import RepositoryException


class UserAlreadyExistException(RepositoryException):
    """ 이미 DB에 존재합니다 """


class UserNotFoundException(RepositoryException):
    """ 해당하는 User를 찾지 못했습니다 """
