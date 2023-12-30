from django.contrib import admin


class CustomerDataAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "approved", "pending",
                    "rejected", "national_id",
                    "customer_contact", "second_contact", "customer_email",
                    "first_witness_name", "first_witness_contact",
                    "second_witness_name", "second_witness_contact",
                    "customer_location", "nearest_school",
                    "nearest_market_church_hospital", "created_at",
                    "workplace", "employer_or_coleague",
                    "employer_or_coleague_contact", "account_name")

    search_fields = ('customer_name', 'customer_contact', 'national_id')

    list_per_page = 20
