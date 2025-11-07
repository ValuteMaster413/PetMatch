from enum import Enum


class ServiceScope(Enum):
    TRANSIENT = 'Transient'
    SINGLETON = 'Singleton'