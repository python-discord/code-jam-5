from .constants import goal_db_path


def get_db():
    from .goal_db import GoalDB

    if goal_db_path.exists():
        return GoalDB.load_from(goal_db_path)

    else:
        return GoalDB.create_new(goal_db_path)
