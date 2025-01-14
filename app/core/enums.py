from enum import Enum


class UseUnit(str, Enum):
    gb_mo = "GB/Mo"
    hour = "Hrs"
    hosted_zone = "Hosted Zone"
    keys = "Keys"
    request = "Requests"
    alarm = "Alarms"
    metrics = "Metrics"
