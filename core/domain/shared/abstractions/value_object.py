#TODO: make it ABS and hash method abstract
class ValueObject:
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return vars(self) == vars(other)
        return False














