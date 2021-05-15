from django.utils.timezone import now
from django.db.models import Model, ForeignKey, DateTimeField, CASCADE, TextField, CharField
from django.contrib.auth import get_user_model


class CreatedTimeMixin(Model):
    created_time = DateTimeField(default=now)

    class Meta:
        abstract = True
        ordering = ('created_time',)


class Calculator(CreatedTimeMixin):
    MODES = (
        ('S', "Standard"),
        ('P', 'Programmer')
    )
    mode = CharField(max_length=1, choices=MODES)
    owner = ForeignKey(get_user_model(), on_delete=CASCADE, related_name='calculators')

    class Meta:
        ordering = ('created_time',)

    def __str__(self):
        return 'Calculator(created by {} at{}).'.format(self.owner, self.created_time)


class History(CreatedTimeMixin):
    calculator = ForeignKey(Calculator, on_delete=CASCADE, related_name='history_items')
    expr = TextField()
    result = TextField()

    def __str__(self):
        return 'History item(created at {} for {}).'.format(self.created_time, self.calculator)
