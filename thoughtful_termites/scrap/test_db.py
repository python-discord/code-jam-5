from pathlib import Path
from thoughtful_termites.shared.goal_db import GoalDB
from thoughtful_termites.shared.goal_db import Days
from thoughtful_termites.shared.goal_db import ReminderTime

cd = Path(__file__).parent
db_path: Path = cd / 'goals.db'


if db_path.exists():
    db = GoalDB.load_from(db_path)
else:
    db = GoalDB.create_new(db_path)

# for i in range(10):
#     goal = db.new_goal(f'Goal {i}', f'New goal {i}')
#     for j in range(10):
#         goal.new_reminder(Days.Tuesday, ReminderTime(j, 0))

for reminder in db.get_reminders_on_day(Days.Tuesday):
    print(reminder)

# for reminder in db.get_reminders():
#     print(reminder, reminder.day, reminder.time)
#
# for goal in db.get_goals():
#     print(goal)
#     for reminder in goal.get_reminders():
#         print(reminder)
