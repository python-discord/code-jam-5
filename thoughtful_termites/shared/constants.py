from pathlib import Path

cd = Path(__file__).parent

goal_db_path: Path = cd/'goals.db'
config_path: Path = cd/'config.json'
completed_goals_path: Path = cd/'completed_goals.txt'
