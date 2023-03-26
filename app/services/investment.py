from datetime import datetime
from typing import Union, List

from app.models import CharityProject, Donation


def investment_process(
        obj_in: Union[CharityProject, Donation],
        obj_model: List[Union[CharityProject, Donation]]
) -> List[Union[CharityProject, Donation]]:
    """Инвестирование пожертвований в незакрытые проекты."""
    obj_in.invested_amount = obj_in.invested_amount or 0
    count = 0
    for balance in obj_model:
        donation = min(
            balance.full_amount - balance.invested_amount,
            obj_in.full_amount - obj_in.invested_amount
        )
        for project in [balance, obj_in]:
            project.invested_amount += donation
            if project.full_amount == project.invested_amount:
                project.close_date = datetime.now()
                project.fully_invested = True
        count += 1
        if obj_in.fully_invested:
            break
    return obj_model[:count]
