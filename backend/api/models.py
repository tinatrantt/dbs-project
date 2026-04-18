from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = 'In-Progress'
        COMPLETED = 'Completed'
        INCOMPLETE = 'Incomplete'


    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    project_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=11,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGRESS
    )

    def __str__(self):
        return self.name


class Todo(models.Model):
    class Meta:
        abstract = True
    
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = 'In-Progress'
        COMPLETED = 'Completed'
        LATE = 'Late'
    

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=11,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGRESS
    )

    def __str__(self):
        self.title


class Task(Todo):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)


class Milestone(Todo):
    deadline = models.DateTimeField()


class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    note_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title