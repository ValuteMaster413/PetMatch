from typing import Optional, Union

from core.domain.shared.errors.error import Error
from core.domain.shared.result import Result


class DomainErrors:
    class Entities:
        class General:
            @staticmethod
            def not_found(entity: str, uid: Optional[str]=None) -> Result:
                return Result.fail(Error.NotFound('entities.general.not.found',
                                                  message=f'Object "{entity}" with identity "{uid or str()} not found"'))
            @staticmethod
            def failure(method: str, entity: str, error: Optional[Union[str, Exception]]) -> Result:
                return Result.fail(Error.NotFound('entities.general.unexpected.failure',
                                                  message=f'Unexpected error "{error or str()}" occur inside {method} of entity {entity} "'))

    class ValueObjects:
        class EntityUID:
            @staticmethod
            def invalid_uid_value(value) -> Result:
                return Result.fail(Error.Validation('entity.uid.invalid.value',
                                                    message=f'Not valid UID "{value}"'))
        class GenerativeEnum:
            @staticmethod
            def invalid_value(value) -> Result:
                return Result.fail(Error.Validation(code='generative.enum.from.value.error',
                                                    message=f"No enum member with value '{value}'"))

        class GasVolumeQuantity:
            @staticmethod
            def invalid_value(value) -> Result:
                return Result.fail(Error.Validation(code='gas.volume.quantity.value.error',
                                                    message=f"Gas volume can't be negative. Provided: [{value}]"))
        class WeightQuantity:
            @staticmethod
            def invalid_value(value) -> Result:
                return Result.fail(Error.Validation(code='weight.quantity.value.error',
                                                    message=f"Weight quantity can't be negative. Provided: [{value}]"))

        class GasVolumeCapacity:
            @staticmethod
            def invalid_value(value) -> Result:
                return Result.fail(Error.Validation('gas.volume.capacity.invalid.value',
                                                    message=f'Capacity cant be negative or None. Provided "{value}"'))
        class MassCapacity:
            @staticmethod
            def invalid_value(value) -> Result:
                return Result.fail(Error.Validation('mass.capacity.invalid.value',
                                                    message=f'Capacity cant be negative or None. Provided "{value}"'))
        class PositiveInteger:
            @staticmethod
            def invalid_value(value) -> Result:
                return Result.fail(Error.Validation('positive.integer.invalid.value',
                                                    message=f'PositiveInteger cant be negative or None. Provided "{value}"'))

        class PositiveFloat:
            @staticmethod
            def invalid_value(value: Optional[float]) -> Result:
                return Result.fail(Error.Validation(code='positive.float.invalid.value',
                                                    message=f'PositiveFloat can not be negative or None. Provided: [{value}]'))
        class BigPercent:
            @staticmethod
            def invalid_value_range(value) -> Result:
                return Result.fail(Error.Validation('big.percent.invalid.value.range',
                                                    message=f'Not valid value "{value}" for BigPercent. Must be between 0 and 100'))
        class Year:
            @staticmethod
            def invalid_value() -> Result:
                return Result.fail(Error.Validation('year.invalid.value',
                                                    message='Year must be between 1950 and 2050'))
        class Utilization:
            @staticmethod
            def invalid_value(value: float) -> Result:
                return Result.fail(Error.Validation(code='capacity.utilization.rate.value.error',
                                                    message=f'Utilization rate must be between 0 and 1. Provided: [{value}]'))
        class Stream:
            @staticmethod
            def incomplete_data_to_create_stream() -> Result:
                return Result.fail(Error.Validation(code='stream.incomplete.data',
                                                    message='Units or Direction can be None only if resource is Emission'))

        class CarbonPolicy:
            @staticmethod
            def missing_benchmark_policy() -> Result:
                return Result.fail(Error.Validation(code='carbon.policy.missing.benchmark.policy',
                                                    message='Benchmark policy must be provided'))
            @staticmethod
            def missing_benchmark() -> Result:
                return Result.fail(Error.Validation(code='carbon.policy.missing.benchmark',
                                                    message='Carbon benchmark must be provided when Benchmark Policy require some benchmark'))

        class Capex:
            @staticmethod
            def incomplete_data() -> Result:
                return Result.fail(Error.Validation(code='__capex.incomplete.data',
                                                    message='To create __capex from technology data ISBL, OSBL, capacity ration and exponents must be provided'))

            @staticmethod
            def target_location_or_index_is_none() -> Result:
                return Result.fail(Error.Validation(code='__capex.target.location.index.not.specified',
                                                    message='Target location and index are required to build Capex from direct value'))

        class BatteryLimit:
            @staticmethod
            def location_error() -> Result:
                return Result.fail(Error.Validation(code='process.battery.limit.location',
                                                    message='Battery Limit Capex location must be 1'))

            @staticmethod
            def exponents_error() -> Result:
                return Result.fail(Error.Validation(code='process.battery.limit.exponents',
                                                    message='Exponents collection must have at least one entry'))

        class YearsBasedList:
            @staticmethod
            def year_based_records() -> Result:
                return Result.fail(Error.Validation('year.based.list.non.year.based.record',
                                                    message='All records should be Year-based: each must have at least one attribute with a Year instance as a value'))
            @staticmethod
            def invalid_value_range() -> Result:
                return Result.fail(Error.Validation('year.based.list.invalid.year.range',
                                                    message='Years must be from 2015 to 2030 range'))
            @staticmethod
            def repeated_years(value) -> Result:
                return Result.fail(Error.Validation('year.based.list.repeated.years',
                                                    message=f'Repeated Year values are prohibited: {value}'))
            @staticmethod
            def number_of_records(target, value) -> Result:
                return Result.fail(Error.Validation('year.based.list.number.of.records',
                                                    message=f'Number of records must be equal to {target}, provided: {value}'))