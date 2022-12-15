import io

import sh


class AlreadyExistsException(Exception):
    """Item already exists."""


class NotFoundException(Exception):
    """Item not found."""


class Storage:
    def __init__(self, service: str):
        self.service = service

    def get_password(self, account: str) -> str:
        out = io.StringIO()
        try:
            sh.security(
                "find-generic-password",
                "-w",
                s=self.service,
                a=account,
                _out=out,
            )
        except sh.ErrorReturnCode_44:
            raise NotFoundException

        output = out.getvalue()
        return output[:-1]

    def save_password(self, account: str, password: str) -> None:
        try:
            sh.security(
                "add-generic-password",
                s=self.service,
                a=account,
                w=password,
            )
        except sh.ErrorReturnCode_45:
            raise AlreadyExistsException

    def delete(self, account: str) -> None:
        try:
            sh.security(
                "delete-generic-password",
                s=self.service,
                a=account,
            )
        except sh.ErrorReturnCode_44:
            raise NotFoundException

    def item_exists(self, account: str) -> bool:
        try:
            self.get_password(account)
        except NotFoundException:
            return False
        return True
