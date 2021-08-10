from django.http import HttpResponse
from django.template import loader
from django.views import View

from appcalendar.models import Day
from common.utils import today


class OrganizerViewBase(View):
    def setup(self, request, *args, **kwargs):
        super(OrganizerViewBase, self).setup(request, *args, **kwargs)
        self.today = today()
        self.day = Day.get_or_create(date=self.today)


class Dashboard(OrganizerViewBase):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('organizer/dashboard.html')
        context = {
            'pageModule': 'dashboardModule',
            'pageController': 'dashboardController',
        }
        return HttpResponse(template.render(context, request))
