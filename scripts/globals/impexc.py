class PackageException(Exception):
    """
    Custom Exception class to handle missing package exceptions.
    """
    def __init__(self, package, suggestion, lnx:bool, pkgmgrs:list[str] = [], *args: object) -> None:
        self.package = package
        self.message = f"You do not have the {package} package installed.\n{suggestion}\n"
        if lnx:
            self.message += '\n'.join(pkgmgrs)
        super().__init__(*args)