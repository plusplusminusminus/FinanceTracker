from sqlalchemy.orm import Session
from database.models.goal_model import Goal

"""Create a new goal for the user"""
def create_goal(db: Session, user_id: int, goal_description: str, goal_amount: float, current_amount: float = 0.0) -> Goal:
    goal = Goal(
        user_id = user_id,
        description = goal_description,
        target_amount = goal_amount,
        current_amount = current_amount,
        status = "current"
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

"""get the goal based on its ID for the user"""
def get_goal_by_id(db: Session, goal_id: int, user_id: int) -> Goal:
    return db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()

"""Get all the goals for the user"""
def get_goals_by_user(db: Session, user_id: int) -> list[Goal]:
    return db.query(Goal).filter(Goal.user_id == user_id).all()

"""Get all the current goals for the user"""
def get_current_goals_by_user(db: Session, user_id: int) -> list[Goal]:
    return db.query(Goal).filter(Goal.user_id == user_id, Goal.status == 'current').all()

"""Get all the completed goals for the user"""
def get_completed_goals_by_user(db: Session, user_id: int) -> list[Goal]:
    return db.query(Goal).filter(Goal.user_id == user_id, Goal.status == 'completed').all()

"""Update the goal's information if the user wants to change it after creating it"""
def update_goal(db: Session, goal_id: int, user_id: int, description: str = None, goal_amount: float = None, current_amount: float = None) -> Goal:
    goal = get_goal_by_id(db, goal_id, user_id)
    if not goal:
        return None
    if description is not None:
        goal.description = description
    if goal_amount is not None:
        goal.target_amount = goal_amount
    if current_amount is not None:
        goal.current_amount = current_amount
        if goal.current_amount >= goal.target_amount:
            goal.status = "completed"
    db.commit()
    db.refresh(goal)
    return goal    

"""Add an amount ot the goal's current amount and update the status of the goal if it is completed"""
def update_goal_progress(db: Session, user_id: int, goal_id: int, amount_to_add: float) -> Goal:
    goal = get_goal_by_id(db, goal_id, user_id)
    if not goal:
        return None
    goal.current_amount += amount_to_add
    if goal.current_amount >= goal.target_amount:
        goal.status = "completed"
    db.commit()
    db.refresh(goal)
    return goal

"""Mark a goal as completed"""
def mark_goal_completed(db: Session, user_id: int, goal_id: int) -> Goal:
    goal = get_goal_by_id(db, goal_id, user_id)
    if not goal:
        return None
    goal.status = "completed"
    db.commit()
    db.refresh(goal)
    return goal

"""Mark a goal as current"""
def mark_goal_current(db: Session, user_id: int, goal_id: int) -> Goal:
    goal = get_goal_by_id(db, goal_id, user_id)
    if not goal:
        return None
    goal.status = "current"
    db.commit()
    db.refresh(goal)
    return goal

"""Delete a goal for the user if they want to remove it"""
def delete_goal(db: Session, user_id: int, goal_id: int) -> bool:
    goal = get_goal_by_id(db, goal_id, user_id)
    if not goal:
        return False
    db.delete(goal)
    db.commit()
    return True

"""Get the completion percentage of a goal for the user"""
def get_goal_completion_percentage(db: Session, user_id: int, goal_id: int) -> float:
    goal = get_goal_by_id(db, goal_id, user_id)
    if not goal:
        return 0.0
    percentage = (goal.current_amount / goal.target_amount) * 100
    return min(percentage, 100.0)
