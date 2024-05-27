import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from db.base import METADATA, begin_connection
from config import Config


class SpeedRow(t.Protocol):
    id: int
    speed: float


SpeedTable = sa.Table(
    'work_speed',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('speed', sa.Float),

)


# добавляет запись
async def add_action(time_start: datetime) -> None:
    if not Config.debug:
        different = datetime.now () - time_start
        speed = float (f'{different.seconds}.{different.microseconds}')
        async with begin_connection () as conn:
            await conn.execute(
                SpeedTable.insert ().values (
                    speed=speed
                )
            )
