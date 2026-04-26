from logs.models import LogEntry

def create_log(user, action):
    LogEntry.objects.create(user=user, action=action)
