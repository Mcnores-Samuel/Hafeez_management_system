"""This module contains all the functions used to
calculate the commission and target
"""
from ...models.commission import Commission
from django.utils import timezone


class CalcCommissions:
    """This class represents the calc commission class."""
    month = timezone.now().date().month
    year = timezone.now().date().year

    def __init__(self, *args, **kwargs):
        pass

    def calc_commission(self, agent, month=month, year=year):
        """This function is used to calculate the commission"""
        commission = Commission.objects.filter(
            agent=agent, month=month,
            year=year).first()
        commission = commission.amount * commission.total_devices_sold
        return commission
    
    def target_progress(self, agent, month=month, year=year):
        """This function is used to calculate the target progress"""
        commission = Commission.objects.filter(
            agent=agent, month=month,
            year=year).first()
        target = int(commission.target)
        if commission.total_devices_sold > 0:
            progress = (commission.total_devices_sold * 100) / commission.target
            progress = round(progress, 2)
        else:
            progress = 0
        return progress, target
    
    def update_commission(self, agent, stock_out, month=month, year=year):
        """This function is used to update the commission"""
        if not stock_out:
            stock_out = 0
        commission = Commission.objects.filter(
            agent=agent, month=month,
            year=year).first()
        if commission:
            commission.total_devices_sold = stock_out
            commission.save()
        else:
            last_month_target = Commission.objects.filter(
                agent=agent, year=year, month=month-1).first()
            target = 0
            if last_month_target:
                target = last_month_target.total_devices_sold
            else:
                target = 50
            commission = Commission.objects.create(
                agent=agent,
                total_devices_sold=0,
                month=month,
                year=year, target=target, paid=False,
                amount=5000
            )
            commission.total_devices_sold = stock_out
            commission.save()