from django.utils.timezone import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from appcalendar.api.serializers import (
    DaySerializer,
    EventSerializer,
    GoalSerializer,
    TaskSerializer,
)

from appcalendar.models import today, Day, Event, Goal, Task


def api_setup(view):
    view.today = today()
    view.day = Day.get_or_create(date=view.today)


class DashboardApi(APIView):

    def get(self, request, *args, **kwargs):
        api_setup(self)
        day = DaySerializer(instance=self.day)
        todo = GoalSerializer(instance=self.day.todo.filter(appuser=request.user.appuser), many=True)
        doing = GoalSerializer(instance=self.day.doing.filter(appuser=request.user.appuser), many=True)
        done = GoalSerializer(instance=self.day.done.filter(appuser=request.user.appuser), many=True)
        events = EventSerializer(
            instance=self.day.event_set.filter(appuser=request.user.appuser).order_by('start_time'),
            many=True
        )

        DAY_START_TIME = 7
        DAY_END_TIME = 7
        MINUTE_STEP = 15

        minute_options = []
        for i in range(0, 59):
            if i % MINUTE_STEP == 0:
                minute_options.append(str(i).zfill(2))

        time_options = []
        for i in range(DAY_START_TIME, 13):
            for minute in minute_options:
                time_options.append("{}:{} AM".format(str(i).zfill(2), minute))

        for i in range(1, DAY_END_TIME + 1):
            for minute in minute_options:
                time_options.append("{}:{} PM".format(str(i).zfill(2), minute))

        result = {
            'day': day.data,
            'goals': {
                'todo': todo.data,
                'doing': doing.data,
                'done': done.data
            },
            'events': events.data,
            'time_options': time_options,
        }
        return Response(result)


class GoalApi(APIView):
    def patch(self, request, *args, **kwargs):
        api_setup(self)
        goal = Goal.objects.get(pk=request.data['pk'], appuser=request.user.appuser)
        goal.status = request.data['status']
        goal.save()
        goal_data = GoalSerializer(instance=goal).data
        return Response({'status': 'ok', 'goal': goal_data})

    def put(self, request, *args, **kwargs):
        api_setup(self)
        object_type = request.data['target']
        goal = Goal(name=request.data['name'], appuser=request.user.appuser)
        if object_type == 'day':
            goal.day = self.day
        elif object_type == 'week':
            goal.week = self.day.week
        elif object_type == 'month':
            goal.month = self.day.month
        elif object_type == 'year':
            goal.year = self.day.month
        goal.save()
        goal_data = GoalSerializer(instance=goal).data
        return Response({'status': 'ok', 'goal': goal_data})

    def delete(self, request, *args, **kwargs):
        api_setup(self)
        goal = Goal.objects.get(pk=kwargs['goal_pk'], appuser=request.user.appuser)
        goal.delete()
        return Response({'status': 'ok'})


class TaskApi(APIView):
    def put(self, request, *args, **kwargs):
        api_setup(self)
        goal = Goal.objects.get(pk=kwargs['goal_pk'], appuser=request.user.appuser)
        new_task = Task(goal=goal, name=request.data['name'])
        new_task.save()
        task_data = TaskSerializer(instance=new_task).data
        return Response({'status': 'ok', 'task': task_data})

    def patch(self, request, *args, **kwargs):
        api_setup(self)
        task = Task.objects.get(pk=request.data['pk'], goal__appuser=request.user.appuser)
        task.status = request.data['status']
        task.save()
        task_data = TaskSerializer(instance=task).data
        return Response({'status': 'ok', 'task': task_data})


class EventApi(APIView):
    def put(self, request, *args, **kwargs):
        api_setup(self)

        start_time = datetime.strptime(request.data['start_time'], '%I:%M %p')
        end_time = datetime.strptime(request.data['end_time'], '%I:%M %p')

        new_event = Event(
            name=request.data['name'],
            start_time=start_time.time(),
            end_time=end_time.time(),
            appuser=request.user.appuser,
            day=self.day
        )
        new_event.save()
        events = EventSerializer(
            instance=self.day.event_set.filter(appuser=request.user.appuser).order_by('start_time'),
            many=True
        )
        return Response({'status': 'ok', 'events': events.data})

    def patch(self, request, *args, **kwargs):
        api_setup(self)
        task = Task.objects.get(pk=request.data['pk'], goal__appuser=request.user.appuser)
        task.status = request.data['status']
        task.save()
        events = EventSerializer(
            instance=self.day.event_set.filter(appuser=request.user.appuser).order_by('start_time'),
            many=True
        )
        return Response({'status': 'ok', 'events': events.data})

    def delete(self, request, *args, **kwargs):
        api_setup(self)
        event = Event.objects.get(pk=kwargs['event_pk'], appuser=request.user.appuser)
        event.delete()
        return Response({'status': 'ok'})
