from django.db import models
from appuser.models import AppUser
from common.utils import (
    today,
    ModelBase
)

STATUS_CHOICES = [
    ('todo', 'To Do'),
    ('doing', 'Doing'),
    ('done', 'Done'),
    ('archived', 'Archived'),
]


class CalendarBase(ModelBase):
    class Meta:
        abstract = True

    @property
    def todo(self):
        return self.goal_set.filter(status='todo')

    @property
    def doing(self):
        return self.goal_set.filter(status='doing')

    @property
    def done(self):
        return self.goal_set.filter(status='done')


class Year(CalendarBase):
    number = models.IntegerField(default=1912)


class Month(CalendarBase):
    number = models.IntegerField(default=1)
    name = models.CharField(max_length=20)


class Week(CalendarBase):
    number = models.IntegerField(default=1)

    def __str__(self):
        return 'Week: {} <{}>'.format(self.number, self.uuid)


class Day(CalendarBase):
    date = models.DateTimeField(default=today, null=True, editable=False)
    week = models.ForeignKey(Week, null=True, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.week:
            self.week = Week.get_or_create(number=self.date.isocalendar()[1])
        if not self.month:
            self.month = Month.get_or_create(number=self.date.month, name=self.date.strftime('%B'))
        if not self.year:
            self.year = Year.get_or_create(number=self.date.year)
        super(Day, self).save(*args, **kwargs)

    @property
    def display_date(self):
        self.save()
        return self.date.strftime('%B %d, %Y')

    @property
    def display_day(self):
        return self.date.strftime('%A')

    @property
    def display_week(self):
        return self.week.number

    @property
    def display_month(self):
        return self.month.name

    @property
    def display_year(self):
        return self.year.number

    def __str__(self):
        return 'Day: {} <{}>'.format(self.display_date, self.uuid)


class Event(ModelBase):
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    @property
    def start_time_display(self):
        return self.start_time.strftime('%I:%M%p')

    @property
    def end_time_display(self):
        return self.end_time.strftime('%I:%M%p')


class Goal(ModelBase):
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    year = models.ForeignKey(Year, null=True, on_delete=models.SET_NULL)
    month = models.ForeignKey(Month, null=True, on_delete=models.SET_NULL)
    week = models.ForeignKey(Week, null=True, on_delete=models.SET_NULL)
    day = models.ForeignKey(Day, null=True, on_delete=models.SET_NULL)
    rollover_source = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    rolled_over = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    @property
    def todo(self):
        return self.task_set.filter(status='todo')

    @property
    def doing(self):
        return self.task_set.filter(status='doing')

    @property
    def done(self):
        return self.task_set.filter(status='done')


class Task(ModelBase):
    goal = models.ForeignKey(Goal, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )
