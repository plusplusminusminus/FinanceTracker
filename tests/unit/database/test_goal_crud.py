"""Test the GoalCrud class."""

import pytest
from database.crud.goal_crud import GoalCrud
from database.models.goal_model import Goal
from datetime import date


class TestGoalCrud:
    """Test GoalCrud datebase crud operations."""

    def test_create_goal(self, test_user, db_session):
        """Test creating a goal."""
        goal_crud = GoalCrud(db_session)
        goal = goal_crud.create_goal(test_user.id, "Test Goal", 100.0, 0.0, date(2025,1,1), date(2025,1,31))
        assert goal is not None
        assert goal.user_id == test_user.id
        assert goal.description == "Test Goal"
        assert goal.target_amount == 100.0
        assert goal.current_amount == 0.0
        assert goal.status == "current"
        assert goal.start_date == date(2025,1,1)
        assert goal.end_date == date(2025,1,31)

    def test_get_goal_by_id(self, test_user, test_goal, goal_crud):
        """Test getting a goal by its ID and user ID."""
        goal = goal_crud.get_goal_by_id(test_goal.id, test_user.id)
        assert goal is not None
        assert goal.id == test_goal.id
        assert goal.user_id == test_user.id
        assert goal.description == "Save for a new car"
        assert goal.target_amount == 10000.0
        assert goal.current_amount == 0.0
        assert goal.status == "current"
        assert goal.start_date == date(2025,1,1)
        assert goal.end_date == date(2025,12,31)

    def test_get_completed_goals_by_user(self, test_user, test_goal, goal_crud):
        """Test getting all the completed goals for the user."""
        goal = goal_crud.get_completed_goals_by_user(test_user.id)
        assert len(goal) == 0
    def test_get_current_goals_by_user(self, test_user, test_goal, goal_crud):
        """Test getting all the current goals for the user."""
        goal = goal_crud.get_current_goals_by_user(test_user.id)
        assert len(goal) == 1

    def test_get_goals_by_user(self, test_user, test_goal, goal_crud):
        """Test getting all the goals for the user."""
        goal = goal_crud.get_goals_by_user(test_user.id)
        assert len(goal) == 1
        assert goal[0].id == test_goal.id
        assert goal[0].user_id == test_user.id
        assert goal[0].description == "Save for a new car"
        assert goal[0].target_amount == 10000.0
        assert goal[0].current_amount == 0.0
        assert goal[0].status == "current"

        #make more goal to see if the get goals by user id works
        goal_crud.create_goal(test_user.id, "Test Goal 2", 200.0, 0.0, date(2025,1,1), date(2025,1,31))
        goal_crud.create_goal(test_user.id, "Test Goal 3", 300.0, 0.0, date(2025,1,1), date(2025,1,31))
        goals = goal_crud.get_goals_by_user(test_user.id)
        assert len(goals) == 3
        for goal in goals:
            assert goal.user_id == test_user.id
            assert goal.description in ["Save for a new car", "Test Goal 2", "Test Goal 3"]
            assert goal.target_amount in [10000.0, 200.0, 300.0]
            assert goal.current_amount == 0.0

    def test_mark_goal_completed(self, test_user, test_goal, goal_crud):
        """Test marking a goal as completed."""
        goal = goal_crud.mark_goal_completed(test_user.id, test_goal.id)
        assert goal is not None
        assert goal.id == test_goal.id
        assert goal.user_id == test_user.id
        assert goal.description == "Save for a new car"
        assert goal.target_amount == 10000.0
        assert goal.current_amount == 0.0
        assert goal.status == "completed"

        current_goals = goal_crud.get_current_goals_by_user(test_user.id)
        assert len(current_goals) == 0

        completed_goals = goal_crud.get_completed_goals_by_user(test_user.id)
        assert len(completed_goals) == 1

    def test_get_nonexistent_goal(self, test_user, goal_crud):
        """Test getting a non-existent goal."""
        goal = goal_crud.get_goal_by_id(999, test_user.id)
        assert goal is None

    def test_update_goal_progress(self, test_user, test_goal, goal_crud):
        """Test updating goal progress by adding amount."""
        initial_amount = test_goal.current_amount
        amount_to_add = 500.0
        
        updated_goal = goal_crud.update_goal_progress(test_user.id, test_goal.id, amount_to_add)
        
        assert updated_goal is not None
        assert updated_goal.id == test_goal.id
        assert updated_goal.current_amount == initial_amount + amount_to_add
        assert updated_goal.current_amount == 500.0
        assert updated_goal.target_amount == 10000.0
        assert updated_goal.status == "current"

    def test_update_goal_progress_increases_amount(self, test_user, goal_crud):
        """Test that updating progress increases the current amount."""
        goal = goal_crud.create_goal(
            user_id=test_user.id,
            goal_description="Small Goal",
            goal_amount=100.0,
            current_amount=50.0,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31)
        )
        
        
        updated_goal = goal_crud.update_goal_progress(test_user.id, goal.id, 50.0)
        
        assert updated_goal is not None
        assert updated_goal.current_amount == 100.0
        assert updated_goal.target_amount == 100.0
        #NOTE: the status is still "current" because sometimes the target amount ofthe goal does not dictate its status,
        #since some goal might be like "spent this much money on takeout" but the user might have gone over the target amount.
        #so the goal is only marked as compelte when the end date is reached or the user manually mark it complete.
        assert updated_goal.status == "current"

    def test_update_goal_progress_nonexistent_goal(self, test_user, goal_crud):
        """Test updating progress for non-existent goal."""
        result = goal_crud.update_goal_progress(test_user.id, 99999, 100.0)
        assert result is None

    def test_delete_goal(self, test_user, test_goal, goal_crud):
        """Test deleting a goal."""
        goal_id = test_goal.id
        
        deleted_goal = goal_crud.delete_goal(test_user.id, goal_id)
        assert deleted_goal is True
        
        retrieved = goal_crud.get_goal_by_id(goal_id, test_user.id)
        assert retrieved is None

    def test_delete_goal_nonexistent(self, test_user, goal_crud):
        """Test deleting a non-existent goal."""
        deleted = goal_crud.delete_goal(test_user.id, 99999)
        assert deleted is False

    def test_get_goal_completion_percentage(self, test_user, test_goal, goal_crud):
        """Test getting goal completion percentage."""
        # the goal current amount is 0 so the progress percentage should be 0 too
        percentage = goal_crud.get_goal_completion_percentage(test_user.id, test_goal.id)
        assert percentage == 0.0

    def test_get_goal_completion_percentage_partial(self, test_user, goal_crud):
        """Test getting completion percentage for partially completed goal."""
        goal = goal_crud.create_goal(
            user_id=test_user.id,
            goal_description="Partially Completed Goal",
            goal_amount=1000.0,
            current_amount=500.0,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31)
        )
        
        percentage = goal_crud.get_goal_completion_percentage(test_user.id, goal.id)
        assert percentage == 50.0  

    def test_get_goal_completion_percentage_complete(self, test_user, goal_crud):
        """Test getting completion percentage for goal with 100% progress"""
        goal = goal_crud.create_goal(
            user_id=test_user.id,
            goal_description="Complete Goal",
            goal_amount=1000.0,
            current_amount=1000.0,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31)
        )
        
        percentage = goal_crud.get_goal_completion_percentage(test_user.id, goal.id)
        assert percentage == 100.0 

    def test_get_goal_completion_percentage_nonexistent(self, test_user, goal_crud):
        """Test getting completion percentage for non-existent goal returns 0.0."""
        percentage = goal_crud.get_goal_completion_percentage(test_user.id, 99999)
        assert percentage == 0.0

    def test_mark_goal_current(self, test_user, goal_crud):
        """Test marking a goal as current."""
        goal = goal_crud.create_goal(
            user_id=test_user.id,
            goal_description="Completed Goal",
            goal_amount=1000.0,
            current_amount=1000.0,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31)
        )
        assert goal.status == "completed"
        
        updated_goal = goal_crud.mark_goal_current(test_user.id, goal.id)
        
        assert updated_goal is not None
        assert updated_goal.id == goal.id
        assert updated_goal.status == "current"

    def test_mark_goal_current_nonexistent(self, test_user, goal_crud):
        """Test marking non-existent goal as current."""
        result = goal_crud.mark_goal_current(test_user.id, 99999)
        assert result is None


