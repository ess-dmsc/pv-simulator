from p4p import Type

ess_bool_data_type = Type(
    [
        ("value", "?"),  # boolean
        ("alarm", ("S", None, [("severity", "i"), ("status", "i"), ("message", "s"),])),
        (
            "timeStamp",
            (
                "S",
                None,
                [("secondsPastEpoch", "l"), ("nanoseconds", "i"), ("userTag", "i"),],
            ),
        ),
        (
            "display",
            (
                "S",
                None,
                [
                    ("limitLow", "d"),
                    ("limitHigh", "d"),
                    ("description", "s"),
                    ("units", "s"),
                    ("precision", "i"),
                    ("form", ("S", None, [("index", "i"), ("choices", "as"),])),
                ],
            ),
        ),
        (
            "control",
            ("S", None, [("limitLow", "d"), ("limitHigh", "d"), ("minStep", "d"),]),
        ),
        (
            "valueAlarm",
            (
                "S",
                None,
                [
                    ("active", "?"),
                    ("lowAlarmLimit", "d"),
                    ("lowWarningLimit", "d"),
                    ("highWarningLimit", "d"),
                    ("highAlarmLimit", "d"),
                    ("lowAlarmSeverity", "i"),
                    ("lowWarningSeverity", "i"),
                    ("highWarningSeverity", "i"),
                    ("highAlarmSeverity", "i"),
                    ("hysteresis", "B"),
                ],
            ),
        ),
    ],
    id="epics:nt/NTScalar:1.0",
)

ess_i_data_type = Type(
    [
        ("value", "i"),  # integers
        ("alarm", ("S", None, [("severity", "i"), ("status", "i"), ("message", "s"),])),
        (
            "timeStamp",
            (
                "S",
                None,
                [("secondsPastEpoch", "l"), ("nanoseconds", "i"), ("userTag", "i"),],
            ),
        ),
        (
            "display",
            (
                "S",
                None,
                [
                    ("limitLow", "d"),
                    ("limitHigh", "d"),
                    ("description", "s"),
                    ("units", "s"),
                    ("precision", "i"),
                    ("form", ("S", None, [("index", "i"), ("choices", "as"),])),
                ],
            ),
        ),
        (
            "control",
            ("S", None, [("limitLow", "d"), ("limitHigh", "d"), ("minStep", "d"),]),
        ),
        (
            "valueAlarm",
            (
                "S",
                None,
                [
                    ("active", "?"),
                    ("lowAlarmLimit", "d"),
                    ("lowWarningLimit", "d"),
                    ("highWarningLimit", "d"),
                    ("highAlarmLimit", "d"),
                    ("lowAlarmSeverity", "i"),
                    ("lowWarningSeverity", "i"),
                    ("highWarningSeverity", "i"),
                    ("highAlarmSeverity", "i"),
                    ("hysteresis", "B"),
                ],
            ),
        ),
    ],
    id="epics:nt/NTScalar:1.0",
)

ess_d_data_type = Type(
    [
        ("value", "d"),  # double
        ("alarm", ("S", None, [("severity", "i"), ("status", "i"), ("message", "s"),])),
        (
            "timeStamp",
            (
                "S",
                None,
                [("secondsPastEpoch", "l"), ("nanoseconds", "i"), ("userTag", "i"),],
            ),
        ),
        (
            "display",
            (
                "S",
                None,
                [
                    ("limitLow", "d"),
                    ("limitHigh", "d"),
                    ("description", "s"),
                    ("units", "s"),
                    ("precision", "i"),
                    ("form", ("S", None, [("index", "i"), ("choices", "as"),])),
                ],
            ),
        ),
        (
            "control",
            ("S", None, [("limitLow", "d"), ("limitHigh", "d"), ("minStep", "d"),]),
        ),
        (
            "valueAlarm",
            (
                "S",
                None,
                [
                    ("active", "?"),
                    ("lowAlarmLimit", "d"),
                    ("lowWarningLimit", "d"),
                    ("highWarningLimit", "d"),
                    ("highAlarmLimit", "d"),
                    ("lowAlarmSeverity", "i"),
                    ("lowWarningSeverity", "i"),
                    ("highWarningSeverity", "i"),
                    ("highAlarmSeverity", "i"),
                    ("hysteresis", "B"),
                ],
            ),
        ),
    ],
    id="epics:nt/NTScalar:1.0",
)

ess_f_data_type = Type(
    [
        ("value", "d"),  # float
        ("alarm", ("S", None, [("severity", "i"), ("status", "i"), ("message", "s"),])),
        (
            "timeStamp",
            (
                "S",
                None,
                [("secondsPastEpoch", "l"), ("nanoseconds", "i"), ("userTag", "i"),],
            ),
        ),
        (
            "display",
            (
                "S",
                None,
                [
                    ("limitLow", "d"),
                    ("limitHigh", "d"),
                    ("description", "s"),
                    ("units", "s"),
                    ("precision", "i"),
                    ("form", ("S", None, [("index", "i"), ("choices", "as"),])),
                ],
            ),
        ),
        (
            "control",
            ("S", None, [("limitLow", "d"), ("limitHigh", "d"), ("minStep", "d"),]),
        ),
        (
            "valueAlarm",
            (
                "S",
                None,
                [
                    ("active", "?"),
                    ("lowAlarmLimit", "d"),
                    ("lowWarningLimit", "d"),
                    ("highWarningLimit", "d"),
                    ("highAlarmLimit", "d"),
                    ("lowAlarmSeverity", "i"),
                    ("lowWarningSeverity", "i"),
                    ("highWarningSeverity", "i"),
                    ("highAlarmSeverity", "i"),
                    ("hysteresis", "B"),
                ],
            ),
        ),
    ],
    id="epics:nt/NTScalar:1.0",
)


ess_s_data_type = Type(
    [
        ("value", "s"),  # string
        ("alarm", ("S", None, [("severity", "i"), ("status", "i"), ("message", "s"),])),
        (
            "timeStamp",
            (
                "S",
                None,
                [("secondsPastEpoch", "l"), ("nanoseconds", "i"), ("userTag", "i"),],
            ),
        ),
        (
            "display",
            (
                "S",
                None,
                [
                    ("limitLow", "d"),
                    ("limitHigh", "d"),
                    ("description", "s"),
                    ("units", "s"),
                    ("precision", "i"),
                    ("form", ("S", None, [("index", "i"), ("choices", "as"),])),
                ],
            ),
        ),
        (
            "control",
            ("S", None, [("limitLow", "d"), ("limitHigh", "d"), ("minStep", "d"),]),
        ),
        (
            "valueAlarm",
            (
                "S",
                None,
                [
                    ("active", "?"),
                    ("lowAlarmLimit", "d"),
                    ("lowWarningLimit", "d"),
                    ("highWarningLimit", "d"),
                    ("highAlarmLimit", "d"),
                    ("lowAlarmSeverity", "i"),
                    ("lowWarningSeverity", "i"),
                    ("highWarningSeverity", "i"),
                    ("highAlarmSeverity", "i"),
                    ("hysteresis", "B"),
                ],
            ),
        ),
    ],
    id="epics:nt/NTScalar:1.0",
)


DTYPE_MAP = {
    "int": ess_i_data_type,
    "float": ess_f_data_type,
    "double": ess_d_data_type,
    "string": ess_s_data_type,
    "bool": ess_bool_data_type,
}

INITIAL_VALUES = {
    "int": 0,
    "float": 0.0,
    "double": 0.0,
    "string": "",
    "bool": False,
}
