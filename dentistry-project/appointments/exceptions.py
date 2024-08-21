class BusyDayException(BaseException):
    def __init__(self, message: str):
        super().__init__(message)


class DayHaveNecessaryTimeSlotsCount(BaseException):
    pass
