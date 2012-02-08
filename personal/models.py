from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    class meta:
        db_table = 'personal_account'

    name = models.CharField(max_length=25)
    balance = models.DecimalField(max_digits=19, decimal_places=10)

    def process_transaction(self, amount):
        self.balance += amount


class Category(models.Model):
    class meta:
        db_table = 'personal_category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)


class Transaction(models.Model):

    class meta:
        db_table = 'personal_transactions'
        #ordering = ['Transaction', 'name']
        #unique_together = ('Transaction', 'name')
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    from_account = models.ForeignKey(Account)
    date = models.DateTimeField()
    process = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Transaction).save(*args, **kwargs)
        if self.process:
            self.from_account.process_transacton(self.amount)

    @property
    def total(self):
        return self.lines.all().aggregate(Sum('amount'))

    @property
    def reference(self):
        return '\n'.join(self.lines.all().values_list('reference', flat=True))

    @property
    def description(self):
        return '\n'.join(self.lines.all().values_list('description', flat=True))


class TransactionLine(models.Model):

    class meta:
        db_table = 'personal_transactions'

    category = models.ForeignKey(Category,
                                 related_name='transaction_values')
    transaction = models.ForeignKey(Transaction,
                                    related_name='lines')
    date = models.DateTimeField()
    reference = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    process = models.BooleanField(default=True)


class Filter(models.Model):

    class meta:
        db_table = 'personal_filter'

    name = models.CharField(max_length=25)
    reg_ex = models.CharField(max_length=25)
    match = models.CharField(max_length=25)
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)


class Budget(models.Model):

    class meta:
        db_table = 'personal_budget'

    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    value = models.DecimalField(max_digits=8, decimal_places=2)


class TransactionUpload(models.Model):

    class meta:
        db_table = 'personal_transaction_upload'

    user = models.ForeignKey(User)
    upload_file = models.FileField(upload_to="transaction_uploads")
    delimiter = models.CharField(max_length=2)
