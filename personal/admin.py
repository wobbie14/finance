from django.contrib import admin

from porkpy.personal.models import Account, Budget, Category, Filter,\
     Transaction

class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)

class BudgetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Budget, BudgetAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class FilterAdmin(admin.ModelAdmin):
    pass
admin.site.register(Filter, FilterAdmin)

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)