from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.

ACCOUNT_CHOICES = (
    ('Credit', (
            ('savings', 'Savings'),
            ('current', 'Current'),
        )
     ),
    ('Debit', (
            ('loan', 'Loan'),
            ('cc', 'Credit Card'),
        )
    ),
)


class Account(models.Model):
    class meta:
        db_table = 'personal_account'

    name = models.CharField(max_length=25,
                            verbose_name=u'Account Name',
                            help_text=u'Name used to identify this Account')
    balance = models.DecimalField(max_digits=19,
                                  decimal_places=10,
                                  verbose_name=u'Account Balance',
                                  help_text=u'Balance of account at certain point')  # at point in timt
    type = models.CharField(max_length=25,
                            verbose_name=u'Account Type',
                            help_text=u'Type of account',
                            choices=ACCOUNT_CHOICES)

    def process_transaction(self, amount):
        self.balance += amount

    # TODO: will need a property to get current balance or always updade
    # balance question of showin balance at time of transaction?


class Category(models.Model):
    class meta:
        db_table = 'personal_category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=25,
                            verbose_name=u'Category Name',
                            help_text=u'Name of category')
    description = models.CharField(max_length=255,
                                   verbose_name=u'Category Description',
                                   help_text=u'Description of category')
    transaction_type = models.CharField(max_length=255,
                                        choices=['EXPENSE', 'INCOME'],
                                        verbose_name=u'Transaction Type',
                                        help_text=u'transaction type')
    parent = models.ForeignKey('self',
                               relation_name='sub_categories',
                               verbose_name=u'Parent Category',
                               help_text=u'Category that this is a subcateogry of')


class Transaction(models.Model):

    class meta:
        db_table = 'personal_transactions'
        #ordering = ['Transaction', 'name']
        #unique_together = ('Transaction', 'name')
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    from_account = models.ForeignKey(Account,
                                     verbose_name=u'From Account',
                                     help_text=u'Account monies transfered from')
    date = models.DateTimeField(verbose_name=u'Transaction Date time',
                                help_text=u'Date and time of transaction')
    reconciled = models.BooleanField(default=True,
                                  verbose_name=u'Transaction Reconciled',
                                  help_text=u'Has the transaction been reconciled against bank statement')
    applied = models.BooleanField(default=True,
                                      verbose_name=u'Transaction Applied',
                                      help_text=u'Has the transaction been applied against account balance')

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
        return '\n'.join(self.lines.all().values_list('description',
                                                      flat=True))


class TransactionLine(models.Model):

    class meta:
        db_table = 'personal_transactions'

    category = models.ForeignKey(Category,
                                 related_name='category_transactions',
                                 verbose_name=u'Tranaction Category',
                                 help_text=u'Category this amount is assigned to')
    transaction = models.ForeignKey(Transaction,
                                    related_name='transaction_lines',
                                    verbose_name=u'Tranaction',
                                    help_text=u'Tranaction in which this line occured')
    reference = models.CharField(max_length=255,
                                 verbose_name=u'Reference',
                                 help_text=u'Reference for this tranaction')
    description = models.CharField(max_length=255,
                                   verbose_name=u'Description',
                                   help_text=u'Reference for this tranaction')
    amount = models.DecimalField(max_digits=8,
                                 decimal_places=2,
                                 verbose_name=u'Amount',
                                 help_text=u'Amount of this part of the tranaction')


class Filter(models.Model):

    class meta:
        db_table = 'personal_filter'

    name = models.CharField(max_length=25,
                            verbose_name=u'Account Name',
                            help_text=u'Name used to identify this Account')
    reg_ex = models.CharField(max_length=25,
                              verbose_name=u'Account Name',
                              help_text=u'Name used to identify this Account')  # ???
    match = models.CharField(max_length=25,
                             verbose_name=u'Account Name',
                             help_text=u'Name used to identify this Account')
    user = models.ForeignKey(User,
                             verbose_name=u'Account Name',
                             help_text=u'Name used to identify this Account')
    category = models.ForeignKey(Category,
                                 verbose_name=u'Account Name',
                                 help_text=u'Name used to identify this Account')


class Budget(models.Model):

    class meta:
        db_table = 'personal_budget'

    user = models.ForeignKey(User,
                             verbose_name=u'Account Name',
                             help_text=u'Name used to identify this Account')
    category = models.ForeignKey(Category,
                                 verbose_name=u'Budget Category',
                                 help_text=u'Category this Budget applies to')
    value = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name=u'Value',
                                help_text=u'Amount bedgeted to spend')
    start_dt = models.DateTimeField(none=True,
                                    blank=True,
                                    verbose_name=u'Start Date',
                                    help_text=u'Start date and time of this Budget')
    end_dt = models.DateTimeField(none=True,
                                  blank=True,
                                  verbose_name=u'End Date',
                                  help_text=u'End date and time of this Budget')


class TransactionUpload(models.Model):

    class meta:
        db_table = 'personal_transaction_upload'

    user = models.ForeignKey(User,
                             verbose_name=u'Account Name',
                             help_text=u'Name used to identify this Account')
    upload_file = models.FileField(upload_to="transaction_uploads",
                                   verbose_name=u'Account Name',
                                   help_text=u'Name used to identify this Account')
    delimiter = models.CharField(max_length=2,
                                 verbose_name=u'Account Name',
                                 help_text=u'Name used to identify this Account')
