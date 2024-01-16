import datetime

class Input:

    @staticmethod
    def get_time_str(prefix, time: datetime.datetime=None):
        """Returns a string like: prefix-240101-185316-770263"""
        if time is None:
            time = datetime.datetime.now(datetime.timezone.utc)
        return f"{prefix}-{time.strftime("%y%m%d-%H%M%S-%f")}"