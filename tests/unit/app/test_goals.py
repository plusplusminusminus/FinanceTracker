"""Testing the Goals class"""

import pytest
from unittest.mock import Mock
from datetime import date
from app.goals import Goals

class TestGoals:
    """Test Goals functions and logic."""

    def test_create_goal_success(self, mock_db, mock_user, mock_user_crud, mock_goal, mock_goal_crud):
        """Test creating a goal successfully."""
        mock_user_crud.get_user_by_id.return_value = mock_user
        mock_goal_crud.create_goal.return_value = mock_goal

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud
        goals._user_crud = mock_user_crud

        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, 0.0, "2025-01-01", "2025-12-31")
        assert valid_goal is True
        assert "created" in message.lower() or "success" in message.lower()
        mock_goal_crud.create_goal.assert_called_once_with(mock_user.id, "Save for vacation trip", 5000, 0.0, date(2025, 1, 1), date(2025, 12, 31))

    def test_create_goal_with_missing_values(self, mock_db, mock_user, mock_user_crud, mock_goal_crud):
        """Test create goal with missing description or amount"""
        mock_user_crud.get_user_by_id.return_value = mock_user
        mock_goal_crud.create_goal.return_value = None

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud
        goals._user_crud = mock_user_crud

        #test with no description 
        valid_goal, message = goals.create_goal(mock_user.id, None, 5000, 0.0, "2025-01-01", "2025-12-31")
        assert valid_goal is False
        assert "Goal description and goal amount are required" in message
        #test with no goal amount
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", None, 0.0, "2025-01-01", "2025-12-31")
        assert valid_goal is False
        assert "Goal description and goal amount are required" in message
        #test with negative current amount
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, -100.0, "2025-01-01", "2025-12-31")
        assert valid_goal is False
        assert "Current amount must be greater than or equal to 0" in message
        #test with no start date
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, 0.0, None, "2025-12-31")
        assert valid_goal is False
        assert "Start date and end date are required" in message
        #test with no end date
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, 0.0, "2025-01-01", None)
        assert valid_goal is False
        assert "Start date and end date are required" in message
        #test with no start date and no end date
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, 0.0, None, None)
        assert valid_goal is False
        assert "Start date and end date are required" in message

    def test_create_goal_with_invalid_values(self, mock_db, mock_user, mock_user_crud, mock_goal_crud):
        """Test create goal with invalid values"""
        mock_user_crud.get_user_by_id.return_value = mock_user
        mock_goal_crud.create_goal.return_value = None

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud
        goals._user_crud = mock_user_crud

        #test with invalid date format 
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, 0.0, "01-01-2025", "2025-12-31")
        assert valid_goal is False
        assert "Invalid date format" in message
        mock_goal_crud.create_goal.assert_not_called()
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, 0.0, "not-a-date", "2025-12-31")
        assert valid_goal is False
        assert "Invalid date format" in message
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", 5000, 0.0, "2025-14-45", "2025-12-31")
        assert valid_goal is False
        assert "Invalid date format" in message

        #test with the goal amount being negative
        valid_goal, message = goals.create_goal(mock_user.id, "Save for vacation trip", -100.0, 0.0, "2025-01-01", "2025-12-31")
        assert valid_goal is False
        assert "Goal amount must be greater than 0" in message

    def test_get_user_goals(self, mock_db, mock_goal_crud):
        """Test getting goals that belongs to the user by their user id"""
        mock_goal1 = Mock()
        mock_goal1.id = 1
        mock_goal1.description = "Goal 1"
        mock_goal2 = Mock()
        mock_goal2.id = 2
        mock_goal2.description = "Goal 2"
        mock_goal_crud.get_goals_by_user.return_value = [mock_goal1, mock_goal2]

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result = goals.get_user_goals(1)
        assert result == [mock_goal1, mock_goal2]
        mock_goal_crud.get_goals_by_user.assert_called_once_with(1)

    def test_get_current_goals(self, mock_db, mock_goal_crud):
        """Test getting current goals that belongs to the user"""
        mock_goal = Mock()
        mock_goal.id = 1
        mock_goal.description = "Current Goal"
        mock_goal.status = "current"
        mock_goal_crud.get_current_goals_by_user.return_value = [mock_goal]

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result = goals.get_current_goals(1)
        assert result == [mock_goal]
        mock_goal_crud.get_current_goals_by_user.assert_called_once_with(1)

    def test_get_completed_goals(self, mock_db, mock_goal_crud):
        """Test getting completed goals that belogns to the user"""
        mock_goal = Mock()
        mock_goal.id = 1
        mock_goal.description = "Completed Goal"
        mock_goal.status = "completed"
        mock_goal_crud.get_completed_goals_by_user.return_value = [mock_goal]

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result = goals.get_completed_goals(1)
        assert result == [mock_goal]
        mock_goal_crud.get_completed_goals_by_user.assert_called_once_with(1)


    def test_update_goal_progress_success(self, mock_db, mock_goal_crud):
        """Test updating goal progress by adding an amount to the goal's current amount successfully"""
        mock_goal = Mock()
        mock_goal.id = 1
        mock_goal.status = "current"
        mock_goal_crud.update_goal_progress.return_value = mock_goal

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.update_goal_progress(1, 1, 70.0)
        assert result is True
        assert "Successfully updated goal progress" in message
        mock_goal_crud.update_goal_progress.assert_called_once_with(1, 1, 70.0)

    def test_update_goal_progress_not_found(self, mock_db, mock_goal_crud):
        """Test updating goal progress when goal not found"""
        mock_goal_crud.update_goal_progress.return_value = None

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.update_goal_progress(1, 1, 100.0)
        assert result is False
        assert "Goal not found" in message

    def test_update_goal_progress_already_completed(self, mock_db, mock_goal_crud):
        """Test updating goal progress when goal is already completed"""
        mock_goal = Mock()
        mock_goal.id = 1
        mock_goal.status = "completed"
        mock_goal_crud.update_goal_progress.return_value = mock_goal

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.update_goal_progress(1, 1, 100.0)
        assert result is False
        assert "Goal already completed" in message


    def test_get_goal_progress(self, mock_db, mock_goal_crud):
        """Test getting goal progress"""
        mock_goal_crud.get_goal_completion_percentage.return_value = 50.0

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result = goals.get_goal_progress(1, 1)
        assert result == 50.0
        mock_goal_crud.get_goal_completion_percentage.assert_called_once_with(1, 1)

    def test_get_goal_by_id_success(self, mock_db, mock_goal_crud):
        """Test getting goal by ID successfully"""
        mock_goal = Mock()
        mock_goal.id = 1
        mock_goal.description = "Test Goal"
        mock_goal_crud.get_goal_by_id.return_value = mock_goal

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result = goals.get_goal_by_id(1, 1)
        assert result == mock_goal
        mock_goal_crud.get_goal_by_id.assert_called_once_with(1, 1)

    def test_get_goal_by_id_not_found(self, mock_db, mock_goal_crud):
        """Test getting goal by ID when not found"""
        mock_goal_crud.get_goal_by_id.return_value = None

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result = goals.get_goal_by_id(1, 1)
        assert result is None

    def test_delete_user_goal_success(self, mock_db, mock_goal_crud):
        """Test deleting user goal successfully"""
        mock_goal_crud.delete_goal.return_value = True

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.delete_user_goal(1, 1)
        assert result is True
        assert "Successfully deleted goal" in message
        mock_goal_crud.delete_goal.assert_called_once_with(1, 1)

    def test_delete_user_goal_not_found(self, mock_db, mock_goal_crud):
        """Test deleting user goal when the goal is not found"""
        mock_goal_crud.delete_goal.return_value = False

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.delete_user_goal(1, 1)
        assert result is False
        assert "Goal not found" in message
 
    def test_mark_goal_completed_success(self, mock_db, mock_goal_crud):
        """Test marking goal as completed successfully"""
        mock_goal = Mock()
        mock_goal.id = 1
        mock_goal_crud.mark_goal_completed.return_value = mock_goal

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.mark_goal_completed(1, 1)
        assert result is True
        assert "Successfully marked goal as completed" in message
        mock_goal_crud.mark_goal_completed.assert_called_once_with(1, 1)

    def test_mark_goal_completed_not_found(self, mock_db, mock_goal_crud):
        """Test marking goal as completed when the goal is not found"""
        mock_goal_crud.mark_goal_completed.return_value = None

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.mark_goal_completed(1, 1)
        assert result is False
        assert "Goal not found" in message

    def test_mark_goal_current_success(self, mock_db, mock_goal_crud):
        """Test marking goal as current successfully"""
        mock_goal = Mock()
        mock_goal.id = 1
        mock_goal_crud.mark_goal_current.return_value = mock_goal

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.mark_goal_current(1, 1)
        assert result is True
        assert "Successfully marked goal as current" in message
        mock_goal_crud.mark_goal_current.assert_called_once_with(1, 1)

    def test_mark_goal_current_not_found(self, mock_db, mock_goal_crud):
        """Test marking goal as current when goal is not found"""
        mock_goal_crud.mark_goal_current.return_value = None

        goals = Goals(mock_db)
        goals._goal_crud = mock_goal_crud

        result, message = goals.mark_goal_current(1, 1)
        assert result is False
        assert "Goal not found" in message



