"""This module registers the PriceReference model with the admin site."""
from django.contrib import admin


class PriceReferenceAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ("phone", "initial_deposit", "merchant", 'starting_cash_price',
                    'cost_price', 'final_cash_price', 'special_retailer_prices', 'price_added_on',
                    'price_changed_on', 'current_month')
    search_fields = ('phone', 'deposit', 'merchant_price', 'cash_price',
                        'cost_price', 'final_cash_price', 'price_added_on',
                        'price_changed_on', 'current_month')
    list_filter = ('phone', 'price_added_on', 'price_changed_on', 'current_month')

    list_per_page = 20

    def initial_deposit(self, obj):
        """Return the initial deposit amount for the phone"""
        return f"MK{obj.deposit:,}".replace(',', ' ')
    
    def merchant(self, obj):
        """Return the merchant price for the phone"""
        return f"MK{obj.merchant_price:,}".replace(',', ' ')
    
    def starting_cash_price(self, obj):
        """Return the starting cash price for the phone"""
        return f"MK{obj.cash_price:,}".replace(',', ' ')
    
    def cost_price(self, obj):
        """Return the cost price for the phone"""
        return f"MK{obj.cost_price:,}".replace(',', ' ')

    def final_cash_price(self, obj):
        """Return the final cash price for the phone"""
        return f"MK{obj.final_cash_price:,}".replace(',', ' ')
    
    def special_retailer_prices(self, obj):
        """Return the special retailer price for the phone"""
        return f"MK{obj.special_retailer_price:,}".replace(',', ' ')

    def price_added_on(self, obj):
        """Return the date on which the price was added"""
        return obj.price_added_on.strftime("%d %B %Y")

    def price_changed_on(self, obj):
        """Return the date on which the price was changed"""
        return obj.price_changed_on.strftime("%d %B %Y")

    def current_month(self, obj):
        """Return the current month"""
        return obj.current_month