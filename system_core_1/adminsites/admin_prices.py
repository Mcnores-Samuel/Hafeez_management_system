from django.contrib import admin


class AdminYellowPrices(admin.ModelAdmin):
    """This class represents the admin interface for the YellowPrices model.

    Attributes:
      list_display (tuple): The fields to display in the admin interface.
      search_fields (tuple): The fields to search in the admin interface.
      list_filter (tuple): The fields to filter in the admin interface.
      list_per_page (int): The number of items to display per page.
    """
    list_display = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    search_fields = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_filter = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_per_page = 50


class AdminMosesPrices(admin.ModelAdmin):
    """This class represents the admin interface for the MosesPrices model.

    Attributes:
      list_display (tuple): The fields to display in the admin interface.
      search_fields (tuple): The fields to search in the admin interface.
      list_filter (tuple): The fields to filter in the admin interface.
      list_per_page (int): The number of items to display per page.
    """
    list_display = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    search_fields = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_filter = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_per_page = 50

  
class AdminChrisMZPrices(admin.ModelAdmin):
    """This class represents the admin interface for the ChrisMZPrices model.

    Attributes:
      list_display (tuple): The fields to display in the admin interface.
      search_fields (tuple): The fields to search in the admin interface.
      list_filter (tuple): The fields to filter in the admin interface.
      list_per_page (int): The number of items to display per page.
    """
    list_display = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    search_fields = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_filter = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_per_page = 50


class AdminChris25Prices(admin.ModelAdmin):
    """This class represents the admin interface for the Chris25Prices model.

    Attributes:
      list_display (tuple): The fields to display in the admin interface.
      search_fields (tuple): The fields to search in the admin interface.
      list_filter (tuple): The fields to filter in the admin interface.
      list_per_page (int): The number of items to display per page.
    """
    list_display = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    search_fields = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_filter = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_per_page = 50


class AdminBuzzMchinjiPrices(admin.ModelAdmin):
    """This class represents the admin interface for the BuzzMchinjiPrices model.

    Attributes:
      list_display (tuple): The fields to display in the admin interface.
      search_fields (tuple): The fields to search in the admin interface.
      list_filter (tuple): The fields to filter in the admin interface.
      list_per_page (int): The number of items to display per page.
    """
    list_display = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    search_fields = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_filter = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_per_page = 50