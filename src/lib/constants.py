from enum import IntEnum


class BetResult(IntEnum):
    """Numeric codes stored in the `result` column of the `bet` and `combined` tables.

    Values match the integers written by the v1.7 database migration in updateDatabase().
    Do NOT change these values without a corresponding DB migration.
    """
    PENDING = 0
    WON = 1
    LOST = 2
    VOID = 3
    HALF_WON = 4
    HALF_LOST = 5
    CASH_OUT = 6
