from sqlalchemy.orm import Session
from database.crud.goal_crud import GoalCrud
from datetime import datetime

class Goals:
    def __init__(self, db: Session):
        self._db = db
        self._goal_crud = GoalCrud(db)

    def create_goal(self, user_id: int, goal_description: str, goal_amount: float, current_amount: float = 0.0,
                    start_date: str = "", end_date: str = ""):

        if not goal_description or goal_amount is None:
            return False, "Goal description and goal amount are required"
        if goal_amount <= 0.0:
            return False, "Goal amount must be greater than 0"
        if current_amount is None or current_amount < 0.0:
            return False, "Current amount must be greater than or equal to 0"
        if not start_date or not end_date:
            return False, "Start date and end date are required"
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            goal = self._goal_crud.create_goal(user_id, goal_description, goal_amount, current_amount, start_date,
                                               end_date)
            return True, "Successfully created goal"
        except ValueError:
            return False, "Invalid date format"
        except Exception as e:
            return False, f"Error creating goal: {e}"

    def get_user_goals(self, user_id: int):
        try:
            return self._goal_crud.get_goals_by_user(user_id)
        except Exception as e:
            return False, f"Error getting user goals: {e}"

    def get_current_goals(self, user_id: int):
        try:
            return self._goal_crud.get_current_goals_by_user(user_id)
        except Exception:
            return []

    def get_completed_goals(self, user_id: int):
        try:
            return self._goal_crud.get_completed_goals_by_user(user_id)
        except Exception:
            return []

    def update_goal_progress(self, goal_id: int, user_id: int, amount_to_add: float):
        try:
            goal = self._goal_crud.update_goal_progress(user_id, goal_id, amount_to_add)
            if not goal:
                return False, "Goal not found"
            if goal.status == "completed":
                return False, "Goal already completed"
            return True, "Successfully updated goal progress"
        except Exception as e:
            return False, f"Error updating goal progress: {e}"

    def get_goal_progress(self, user_id: int, goal_id: int):
        return self._goal_crud.get_goal_completion_percentage(user_id, goal_id)

    def get_goal_by_id(self, user_id: int, goal_id: int):
        try:
            goal = self._goal_crud.get_goal_by_id(goal_id, user_id)
            if not goal:
                return None
            return goal
        except Exception as e:
            return None

    def delete_user_goal(self, user_id: int, goal_id: int):
        try:
            deleted = self._goal_crud.delete_goal(user_id, goal_id)
            if not deleted:
                return False, "Goal not found"
            return True, "Successfully deleted goal"
        except Exception as e:
            return False, f"Error deleting goal: {e}"

    # NOTE: I might not implement this since there might not be enough time, to be honest,
    # it's not really needed since the user can just delete and create a new goal again
    def update_goal(self, goal_id: int, user_id: int, description: str = None, goal_amount: float = None,
                    current_amount: float = None, start_date: str = None, end_date: str = None):
        try:
            goal = self._goal_crud.update_goal(goal_id, user_id, description, goal_amount, current_amount, start_date,
                                               end_date)
            if not goal:
                return False, "Goal not found"
            return True, "Successfully updated goal"
        except Exception as e:
            return False, f"Error updating goal: {e}"

    def mark_goal_completed(self, user_id: int, goal_id: int):
        try:
            goal = self._goal_crud.mark_goal_completed(user_id, goal_id)
            if not goal:
                return False, "Goal not found"
            return True, "Successfully marked goal as completed"
        except Exception as e:
            return False, f"Error marking goal as completed: {e}"

    def mark_goal_current(self, user_id: int, goal_id: int):
        try:
            goal = self._goal_crud.mark_goal_current(user_id, goal_id)
            if not goal:
                return False, "Goal not found"
            return True, "Successfully marked goal as current"
        except Exception as e:
            return False, f"Error marking goal as current: {e}"
