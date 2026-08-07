import os
import threading
import time
from django.apps import AppConfig


class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'

    def ready(self):
        # Prevent running duplicate threads during Django auto-reloader
        if os.environ.get('RUN_MAIN') == 'true' or 'runserver' in os.sys.argv or not os.environ.get('SERVER_SOFTWARE'):
            self._start_reminder_scheduler()

    def _start_reminder_scheduler(self):
        def run_schedule():
            time.sleep(5)  # Brief pause after startup
            while True:
                try:
                    from crm.event_notifications import check_and_send_event_notifications
                    check_and_send_event_notifications()
                except Exception:
                    pass
                time.sleep(60)

        t = threading.Thread(target=run_schedule, daemon=True, name="EventReminderScheduler")
        t.start()
