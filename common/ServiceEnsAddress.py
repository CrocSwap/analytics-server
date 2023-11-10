from exceptions.InvalidInputException import InvalidInputException

from .ServiceBase import ServiceBase


class ServiceEnsAddress(ServiceBase):
    def get_ens_name_from_address(self, address):
        try:
            ens_name = self.w3.ens.name(address)
        except ValueError as e:
            raise InvalidInputException("address")

        return ens_name if ens_name else None
