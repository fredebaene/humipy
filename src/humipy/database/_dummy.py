"""
This module defines functionality that pushes dummy data (humidity 
measurements) to the test databae for demonstration purposes.
"""


from humipy.database.connect import _SENSORS
from humipy.database.write import push_measurement
import random
import sqlalchemy


def _push_dummy_measurements(engine: sqlalchemy.engine.base.Engine) -> None:
    """
    This function inserts dummy humidity measurements into the test database.

    Args:
        engine (sqlalchemy.engine.base.Engine): a SQLAlchemy engine object.
    """
    for _ in range(50):
        # sleep(random.normalvariate(1., 0.3))
        push_measurement(
            engine, random.choice(_SENSORS), random.uniform(55., 75.),
        )