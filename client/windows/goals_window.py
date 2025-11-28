"""Goals window for creating and managing financial goals."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from .base_window import MainWindow

class GoalsWindow(MainWindow):
    """Window GUI and functions for creating and managing financial goals."""
    def __init__(self, app):
        super().__init__(app)
        # self.root.title("Goals Window")
        self.root.geometry("950x950")
        self.center_window(900, 900)

        # navigation bar to go back to dashboard
        nav_bar = tk.Frame(self.root)
        nav_bar.pack(fill="x", pady=8)
        tk.Button(nav_bar, text="Back to Dashboard", command=self.return_back).pack(side="left", padx=6)

        create_goal = tk.LabelFrame(self.root, text="CREATE GOAL")
        create_goal.pack(fill="x", padx=16, pady=8)

        self.goal_description = tk.StringVar()
        self.goal_target = tk.StringVar()
        self.goal_current = tk.StringVar()
        self.goal_start_date = tk.StringVar()
        self.goal_end_date = tk.StringVar()

        first_row = tk.Frame(create_goal)
        first_row.pack(fill="x", padx=8, pady=4)
        tk.Label(first_row, text="Description").grid(row=0, column=0, sticky="w")
        tk.Entry(first_row, textvariable=self.goal_description, width=40).grid(row=0, column=1, sticky="we", padx=6)

        second_row = tk.Frame(create_goal)
        second_row.pack(fill="x", padx=8, pady=4)
        tk.Label(second_row, text="Target Amount").grid(row=0, column=0, sticky="w")
        tk.Entry(second_row, textvariable=self.goal_target, width=20).grid(row=0, column=1, sticky="w", padx=6)
        tk.Label(second_row, text="Current Amount").grid(row=0, column=2, sticky="w")
        tk.Entry(second_row, textvariable=self.goal_current, width=20).grid(row=0, column=3, sticky="w", padx=6)

        third_row = tk.Frame(create_goal)
        third_row.pack(fill="x", padx=8, pady=4)
        tk.Label(third_row, text="Start Date (YYYY-MM-DD)").grid(row=0, column=0, sticky="w")
        tk.Entry(third_row, textvariable=self.goal_start_date, width=20).grid(row=0, column=1, sticky="w", padx=6)
        tk.Label(third_row, text="End Date (YYYY-MM-DD)").grid(row=0, column=2, sticky="w", padx=(12, 0))
        tk.Entry(third_row, textvariable=self.goal_end_date, width=20).grid(row=0, column=3, sticky="w", padx=6)

        tk.Button(create_goal, text="Create Goal", command=self.create_goal).pack(pady=6)

        self.current_goals_frame = tk.LabelFrame(self.root, text="CURRENT GOALS")
        self.current_goals_frame.pack(fill="both", expand=True, padx=16, pady=8)
        # frame for the tree view of the list of current goals
        current_goals_tree_frame = tk.Frame(self.current_goals_frame)
        current_goals_tree_frame.pack(fill="both", expand=True, padx=8, pady=8)

        current_scroll_bar = ttk.Scrollbar(current_goals_tree_frame, orient="vertical")
        current_scroll_bar.pack(side="right", fill="y")

        self.current_goals_tree = ttk.Treeview(current_goals_tree_frame, columns=("description", "target_amount", "current_amount", "progress_percentage", "start_date", "end_date"), show="headings", yscrollcommand=current_scroll_bar.set, height=6, selectmode="extended")
        current_scroll_bar.config(command=self.current_goals_tree.yview)
        self.current_goals_tree.heading("description", text="Description")
        self.current_goals_tree.heading("target_amount", text="Target Amount")
        self.current_goals_tree.heading("current_amount", text="Current Amount")
        self.current_goals_tree.heading("progress_percentage", text="Progress %")
        self.current_goals_tree.heading("start_date", text="Start Date")
        self.current_goals_tree.heading("end_date", text="End Date")
        self.current_goals_tree.column("description", width=180)
        self.current_goals_tree.column("target_amount", width=120)
        self.current_goals_tree.column("current_amount", width=120)
        self.current_goals_tree.column("progress_percentage", width=100)
        self.current_goals_tree.column("start_date", width=110)
        self.current_goals_tree.column("end_date", width=110)
        self.current_goals_tree.pack(side="left", fill="both", expand=True)
        self.current_goals_tree.bind("<<TreeviewSelect>>", self.on_current_goal_select)

        # different actions for the current goals
        self.current_goals_actions_frame = tk.Frame(self.current_goals_frame)
        self.current_goals_actions_frame.pack(fill="x", padx=8, pady=(0, 8))
        # entry to add amount to the selected goal
        self.current_amount_entry = tk.StringVar()
        tk.Entry(self.current_goals_actions_frame, textvariable=self.current_amount_entry, width=10).pack(side="left",
                                                                                                          padx=4)
        # button to add the amount that the users wants to add to the selected goal based on the ewntry
        self.current_amount_add_button = tk.Button(self.current_goals_actions_frame, text="Add Amount",
                                                   command=self.add_amount_to_selected_goal, state="disabled")
        self.current_amount_add_button.pack(side="left", padx=4)
        # button to mark the selected goal as completed
        self.complete_goal_button = tk.Button(self.current_goals_actions_frame, text="Complete",
                                              command=self.completes_current_selected_goal, state="disabled")
        self.complete_goal_button.pack(side="left", padx=4)
        # button to deleted the selected goal
        self.current_goal_delete_button = tk.Button(self.current_goals_actions_frame, text="Delete",
                                                    command=self.delete_current_selected_goal, state="disabled")
        self.current_goal_delete_button.pack(side="left", padx=4)

        # completed goals frame
        self.completed_goals_frame = tk.LabelFrame(self.root, text="COMPLETED GOALS")
        self.completed_goals_frame.pack(fill="both", expand=True, padx=16, pady=8)
        # frame for the tree view of the list of completed goals
        completed_goals_tree_frame = tk.Frame(self.completed_goals_frame)
        completed_goals_tree_frame.pack(fill="both", expand=True, padx=8, pady=8)

        completed_scroll_bar = ttk.Scrollbar(completed_goals_tree_frame, orient="vertical")
        completed_scroll_bar.pack(side="right", fill="y")

        self.completed_goals_tree = ttk.Treeview(completed_goals_tree_frame, columns=("description", "target_amount", "current_amount", "progress_percentage", "start_date", "end_date"),show="headings", yscrollcommand=completed_scroll_bar.set, height=6,selectmode="extended")
        completed_scroll_bar.config(command=self.completed_goals_tree.yview)
        self.completed_goals_tree.heading("description", text="Description")
        self.completed_goals_tree.heading("target_amount", text="Target Amount")
        self.completed_goals_tree.heading("current_amount", text="Current Amount")
        self.completed_goals_tree.heading("progress_percentage", text="Progress %")
        self.completed_goals_tree.heading("start_date", text="Start Date")
        self.completed_goals_tree.heading("end_date", text="End Date")
        self.completed_goals_tree.column("description", width=180)
        self.completed_goals_tree.column("target_amount", width=120)
        self.completed_goals_tree.column("current_amount", width=120)
        self.completed_goals_tree.column("progress_percentage", width=100)
        self.completed_goals_tree.column("start_date", width=110)
        self.completed_goals_tree.column("end_date", width=110)
        self.completed_goals_tree.pack(side="left", fill="both", expand=True)
        self.completed_goals_tree.bind("<<TreeviewSelect>>", self.on_completed_goal_select)

        self.completed_goals_actions_frame = tk.Frame(self.completed_goals_frame)
        self.completed_goals_actions_frame.pack(fill="x", padx=8, pady=(0, 8))

        self.completed_goal_reactivate_button = tk.Button(self.completed_goals_actions_frame, text="Reactivate",
                                                          command=self.reactivate_selected_completed_goal,
                                                          state="disabled")
        self.completed_goal_reactivate_button.pack(side="left", padx=4)
        self.completed_goal_delete_button = tk.Button(self.completed_goals_actions_frame, text="Delete",
                                                      command=self.delete_selected_completed_goal, state="disabled")
        self.completed_goal_delete_button.pack(side="left", padx=4)

        self.refresh_lists()
        self.root.mainloop()

    def create_goal(self):
        """Create a new goal for the user based on the details the entered."""
        # get the values that the user entered in the fields
        try:
            description = self.goal_description.get().strip()
            target_str = self.goal_target.get().strip()
            current_str = self.goal_current.get().strip()
            goal_start_date = self.goal_start_date.get().strip()
            goal_end_date = self.goal_end_date.get().strip()
            # check to make sure all the fields are filled before creating the goal
            if not description or not target_str or not current_str or not goal_start_date or not goal_end_date:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                target = float(target_str)
                current = float(current_str)
            except ValueError:
                messagebox.showerror("Error", "Target and current amounts must be valid numbers")
                return

            if target <= 0:
                messagebox.showerror("Error", "Target amount must be greater than 0")
                return
            if current < 0:
                messagebox.showerror("Error", "Current amount must be greater than or equal to 0")
                return
            if current > target:
                messagebox.showerror("Error", "Current amount must be less than or equal to target amount")
                return

            try:
                start_date = datetime.strptime(goal_start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(goal_end_date, "%Y-%m-%d").date()

                if end_date <= start_date:
                    messagebox.showerror("Error", "End date must be later than start date")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                return

            # create the goal for the user and have it belongs to their id
            current_user = self.app.session_manager.current_user
            if not current_user:
                messagebox.showerror("Error", "Need to be logged in to create goals")
                return
            
            user_id = current_user.id
            status, message = self.app.goals.create_goal(user_id, description, target, current, goal_start_date,
                                                         goal_end_date)
            if status:
                messagebox.showinfo("Success", message)
                self.goal_description.set("")
                self.goal_target.set("")
                self.goal_current.set("")
                self.goal_start_date.set("")
                self.goal_end_date.set("")
                self.refresh_lists()
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_lists(self):
        """Refresh the goals lists to show the most updated list of goals."""
        # clear the tree views so there isnt a duplicated list of goals that keep stacking on top of each other
        for item in self.current_goals_tree.get_children():
            self.current_goals_tree.delete(item)
        for item in self.completed_goals_tree.get_children():
            self.completed_goals_tree.delete(item)

        # disable the buttions when the list are refreshed since none of the rows are selected yet so user cant use them
        self.current_amount_add_button.config(state="disabled")
        self.complete_goal_button.config(state="disabled")
        self.current_goal_delete_button.config(state="disabled")
        self.completed_goal_reactivate_button.config(state="disabled")
        self.completed_goal_delete_button.config(state="disabled")

        # get the current and completed goals that are tied to the current user based on their user id
        current_user = self.app.session_manager.current_user
        if not current_user:
            return
        user_id = current_user.id
        current_goals = self.app.goals.get_current_goals(user_id)
        completed_goals = self.app.goals.get_completed_goals(user_id)

        # add the curent goals that belongs to the current user to the tree view
        for goal in current_goals:
            start_date_str = str(goal.start_date)
            end_date_str = str(goal.end_date)

            progress_percentage = self.app.goals.get_goal_progress(user_id, goal.id)

            current_amount_str = f"${goal.current_amount:.2f}"
            target_amount_str = f"${goal.target_amount:.2f}"
            progress_percentage_str = f"{progress_percentage:.1f}%"

            self.current_goals_tree.insert("", "end", values=(
            goal.description, target_amount_str, current_amount_str, progress_percentage_str, start_date_str,
            end_date_str), tags=(str(goal.id),))

        # add the completed goasl to the tree view for the current user to see
        for goal in completed_goals:
            start_date_str = str(goal.start_date)
            end_date_str = str(goal.end_date)

            progress_percentage = self.app.goals.get_goal_progress(user_id, goal.id)

            current_amount_str = f"${goal.current_amount:.2f}"
            target_amount_str = f"${goal.target_amount:.2f}"
            progress_percentage_str = f"{progress_percentage:.1f}%"

            self.completed_goals_tree.insert("", "end", values=(
            goal.description, target_amount_str, current_amount_str, progress_percentage_str, start_date_str,
            end_date_str), tags=(str(goal.id),))

    def on_current_goal_select(self, event):
        """Enable the buttons for the current goals tree and disable the buttons for the completed goals tree if the user selects a goal in the current goals tree."""
        selected_items = self.current_goals_tree.selection()

        # remove any seelction from the completed goals tree to avoid having rows in both tree being selected
        # also disable the buttons for the completed goals tree in case the user try to use them for the current goals tree
        for item in self.completed_goals_tree.selection():
            self.completed_goals_tree.selection_remove(item)
        self.completed_goal_reactivate_button.config(state="disabled")
        self.completed_goal_delete_button.config(state="disabled")

        # if tehre are selected items in the current goals tree then enable the buttons so the user can use them to
        if selected_items:
            self.current_amount_add_button.config(state="normal")
            self.complete_goal_button.config(state="normal")
            self.current_goal_delete_button.config(state="normal")
        else:
            self.current_amount_add_button.config(state="disabled")
            self.complete_goal_button.config(state="disabled")
            self.current_goal_delete_button.config(state="disabled")

    def on_completed_goal_select(self, event):
        """Enable the buttons for the completed goals tree and disable the buttons for the current goals tree if the user selects a goal in the completed goals tree."""
        selected_items = self.completed_goals_tree.selection()

        # remove any seelction from the current goals tree to avoid having rows in both tree being selected
        # also disable the buttons for the current goals tree in case the user try to use them for the completed goals tree
        for item in self.current_goals_tree.selection():
            self.current_goals_tree.selection_remove(item)
        self.current_amount_add_button.config(state="disabled")
        self.complete_goal_button.config(state="disabled")
        self.current_goal_delete_button.config(state="disabled")

        # if tehre are selected items in the completed goals tree then enable the buttons so the user can use them to
        if selected_items:
            self.completed_goal_reactivate_button.config(state="normal")
            self.completed_goal_delete_button.config(state="normal")
        else:
            self.completed_goal_reactivate_button.config(state="disabled")
            self.completed_goal_delete_button.config(state="disabled")

    def get_selected_goal_ids(self, tree):
        """Get the ids of all the selected goals in the tree using their tags."""
        selected_goals = tree.selection()
        goal_ids = []
        for goal in selected_goals:
            tags = tree.item(goal, "tags")
            if tags:
                goal_ids.append(int(tags[0]))
        return goal_ids

    def add_amount_to_selected_goal(self):
        """Add money amount to the selected goals."""
        # get the ids of all the selected goals
        selected_goal_id = self.get_selected_goal_ids(self.current_goals_tree)
        try:
            current_user = self.app.session_manager.current_user
            if not current_user:
                messagebox.showerror("Error", "Need to be logged in to add the amount to thegoals")
                return
            
            # get the amount to add from the entry by the user and chec kif its not a negative numeer
            amount_to_add = float(self.current_amount_entry.get().strip())
            if amount_to_add <= 0:
                messagebox.showerror("Error", "The amount to add must be greater than 0")
                return

            # update the current amount to all of the selected goals and update the progress percentage
            for goal_id in selected_goal_id:
                status, message = self.app.goals.update_goal_progress(goal_id, current_user.id,
                                                                      amount_to_add)
                if not status:
                    messagebox.showerror("Error", message)
                    return
            messagebox.showinfo("Success",
                                f"Successfully added ${amount_to_add:.2f} to {len(selected_goal_id)} selected goals")
            self.refresh_lists()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def completes_current_selected_goal(self):
        """Mark the selected goals in the current goals tree as completed."""
        # get the ids of all the selected goals
        selected_goal_id = self.get_selected_goal_ids(self.current_goals_tree)
        try:
            current_user = self.app.session_manager.current_user
            if not current_user:
                messagebox.showerror("Error", "Need to be logged in to complete goals")
                return
            
            # mark all of the selected goals as completed
            for goal_id in selected_goal_id:
                status, message = self.app.goals.mark_goal_completed(current_user.id, goal_id)
                if not status:
                    messagebox.showerror("Error", message)
            messagebox.showinfo("Success", f"Successfully marked {len(selected_goal_id)} selected goals as completed")
            self.refresh_lists()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected_goals(self, tree):
        """Delete the selected goals from the tree"""
        # get the ids of all the selecvte goals from the tree, either the current or completed goals tree
        selected_goal_id = self.get_selected_goal_ids(tree)
        # delete the goals that are selected from the tree for the user
        try:
            current_user = self.app.session_manager.current_user
            if not current_user:
                messagebox.showerror("Error", "Need to be logged in to delete goals")
                return
            
            for goal_id in selected_goal_id:
                status, message = self.app.goals.delete_user_goal(current_user.id, goal_id)
                if not status:
                    messagebox.showerror("Error", message)
            messagebox.showinfo("Success", f"Successfully deleted {len(selected_goal_id)} selected goals")
            self.refresh_lists()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_current_selected_goal(self):
        """Delete the goals from the current goals tree."""
        self.delete_selected_goals(self.current_goals_tree)

    def delete_selected_completed_goal(self):
        """Delete the goals freom the completed goals tree."""
        self.delete_selected_goals(self.completed_goals_tree)

    def reactivate_selected_completed_goal(self):
        """Reactivate the selected completed goals in the completed goals tree."""
        # get the ids of the selected goals from the complete goal tree that we want to reactiveate
        # Also keep count of how many goals were reactivated and how manyt failed depending on their end date
        selected_goal_id = self.get_selected_goal_ids(self.completed_goals_tree)
        current_user = self.app.session_manager.current_user
        if not current_user:
            messagebox.showerror("Error", "Need to be logged in to reactivate goals")
            return
        user_id = current_user.id
        reactivated_count = 0
        skipped_count = 0

        try:
            for goal_id in selected_goal_id:
                # Get the goal based on its id to check its end date to see if it passed already
                goal = self.app.goals.get_goal_by_id(user_id, goal_id)
                if not goal:
                    messagebox.showerror("Error", f"Goal with ID {goal_id} not found")
                    continue

                # Check to see if the end date for the goal the user want to reactivate has already passed
                if goal.end_date < date.today():
                    skipped_count += 1
                    messagebox.showerror("Error",
                                         f"Cannot reactivate goal '{goal.description}' since the end date ({goal.end_date}) has already passed")
                    continue

                # if the cuurrent date is still before the end date then the goal can be reactivated
                status, message = self.app.goals.mark_goal_current(user_id, goal_id)
                if not status:
                    messagebox.showerror("Error", message)
                else:
                    reactivated_count += 1

            if reactivated_count > 0:
                message = f"Successfully reactivated {reactivated_count} selected goal(s)"
                if skipped_count > 0:
                    message += f". {skipped_count} goal(s) were skipped because their end date has passed."
                messagebox.showinfo("Success", message)
            elif skipped_count > 0:
                pass
            else:
                messagebox.showinfo("Info", "No goals were reactivated")

            self.refresh_lists()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_back(self):
        """Return to the dashboard window."""
        from .dashboard_window import DashboardWindow
        
        self.root.destroy()
        DashboardWindow(self.app)

