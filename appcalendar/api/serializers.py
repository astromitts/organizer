from rest_framework import serializers
from appcalendar.models import (
    Day,
    Event,
    Goal,
    Task,
    Month,
    Year,
    Week,
)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = [
            'pk',
            'name',
            'description',
            'status'
        ]


class GoalSerializer(serializers.HyperlinkedModelSerializer):
    todo = TaskSerializer(many=True)
    doing = TaskSerializer(many=True)
    done = TaskSerializer(many=True)

    class Meta:
        model = Goal
        fields = [
            'pk',
            'name',
            'description',
            'todo',
            'doing',
            'done',
            'status',
        ]


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            'pk',
            'name',
            'start_time',
            'end_time',
            'start_time_display',
            'end_time_display'
        ]


class DaySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Day
        fields = [
            'pk',
            'display_date',
            'display_day',
            'date',
        ]


class WeekSerializer(serializers.HyperlinkedModelSerializer):
    goals = GoalSerializer(source='goal_set', many=True)

    class Meta:
        model = Week
        fields = [
            'pk',
            'number',
            'goals',
        ]


class MonthSerializer(serializers.HyperlinkedModelSerializer):
    goals = GoalSerializer(source='goal_set', many=True)

    class Meta:
        model = Month
        fields = [
            'pk',
            'number',
            'name',
            'goals',
        ]


class YearSerializer(serializers.HyperlinkedModelSerializer):
    goals = GoalSerializer(source='goal_set', many=True)

    class Meta:
        model = Year
        fields = [
            'pk',
            'number',
            'goals',
        ]
