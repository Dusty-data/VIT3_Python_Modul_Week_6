
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Task abstract base class
class Task(ABC):
    def __init__(self, description, deadline, priority):
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = "Pending"

    @abstractmethod
    def display_details(self):
        pass

    def to_dict(self):
        return {
            "description": self.description,
            "deadline": self.deadline,
            "priority": self.priority,
            "status": self.status
        }

# PersonalTask subclass
class PersonalTask(Task):
    def __init__(self, description, deadline, priority):
        super().__init__(description, deadline, priority)
        self.type = "Personal"

    def display_details(self):
        return f"Type: {self.type}, Description: {self.description}, Deadline: {self.deadline}, Priority: {self.priority}, Status: {self.status}"

# WorkTask subclass
class WorkTask(Task):
    def __init__(self, description, deadline, priority):
        super().__init__(description, deadline, priority)
        self.type = "Work"

    def display_details(self):
        return f"Type: {self.type}, Description: {self.description}, Deadline: {self.deadline}, Priority: {self.priority}, Status: {self.status}"

# StudyTask subclass
class StudyTask(Task):
    def __init__(self, description, deadline, priority, subject):
        super().__init__(description, deadline, priority)
        self.type = "Study"
        self.subject = subject

    def display_details(self):
        return f"Type: {self.type}, Description: {self.description}, Subject: {self.subject}, Deadline: {self.deadline}, Priority: {self.priority}, Status: {self.status}"

# TaskManagement class
class TaskManagement:

    SPECIAL_KEYWORDS = {
        "today": datetime.now().date(),
        "tomorrow": datetime.now().date() + timedelta(days=1),
        "next week": datetime.now().date() + timedelta(weeks=1)
    }

    def __init__(self, auto_save=False, auto_load=False, filename="tasks.json"):
        self.task_list = []
        self.auto_save = auto_save
        self.auto_load = auto_load
        self.filename = filename
        if self.auto_load:
            self.load_tasks_from_json()

    def add_task(self, task):
        self.task_list.append(task)
        if self.auto_save:
            self.save_tasks_to_json()

    def display_tasks(self):
        for task in self.task_list:
            print(task.display_details())

    def sort_by_priority(self):
        self.task_list.sort(key=lambda x: x.priority)
        print("Tasks sorted by priority.")
        self.display_tasks()

    def sort_by_deadline(self):
        today = datetime.now().date()
        self.task_list.sort(key=lambda x: (self._get_deadline_date(x.deadline), x.deadline < str(today)))
        print("Tasks sorted by deadline.")
        self.display_tasks()

    def _get_deadline_date(self, deadline):
        if deadline.lower() in self.SPECIAL_KEYWORDS:
            return self.SPECIAL_KEYWORDS[deadline.lower()]
        else:
            return datetime.strptime(deadline, "%Y-%m-%d").date()

    def save_tasks_to_json(self):
        with open(self.filename, 'w') as f:
            task_data = [task.to_dict() for task in self.task_list]
            json.dump(task_data, f, indent=4)

    def load_tasks_from_json(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.task_list = []
                for task_data in data:
                    task_type = task_data.get('type', 'Personal')  # Default to 'Personal' if 'type' is missing
                    if task_type == 'Personal':
                        task = PersonalTask(task_data['description'], task_data['deadline'], task_data['priority'])
                    elif task_type == 'Work':
                        task = WorkTask(task_data['description'], task_data['deadline'], task_data['priority'])
                    elif task_type == 'Study':
                        task = StudyTask(task_data['description'], task_data['deadline'], task_data['priority'], task_data.get('subject'))
                    else:
                        raise ValueError("Invalid task type")
                    task.status = task_data['status']
                    self.task_list.append(task)
        except FileNotFoundError:
            print("No existing tasks file found.")
        except KeyError as e:
            print(f"Missing key in task data: {e}")
        except Exception as e:
            print(f"Error loading tasks from JSON: {e}")

# Task Scheduling Class
class TaskScheduling:
    def __init__(self):
        pass

    def create_task(self, task_type, description, deadline, priority, subject=None):
        if task_type.lower() == "personal":
            return PersonalTask(description, deadline, priority)
        elif task_type.lower() == "work":
            return WorkTask(description, deadline, priority)
        elif task_type.lower() == "study":
            return StudyTask(description, deadline, priority, subject)
        else:
            raise ValueError("Invalid task type")

# Task Editing Class
class TaskEditing:
    def __init__(self):
        pass

    def edit_task(self, task, attribute, value):
        if hasattr(task, attribute):
            setattr(task, attribute, value)
        else:
            raise AttributeError("Task does not have attribute '{}'".format(attribute))

    def add_notes(self, task, notes):
        task.notes = notes

    def change_color(self, task, color):
        task.color = color

# Main function
def main():
    task_manager = TaskManagement(auto_save=True, auto_load=True)  # Automatically save and load tasks
    task_scheduler = TaskScheduling()
    task_editor = TaskEditing()

    while True:
        print("\n1. Add Task")
        print("2. Display Tasks")
        print("3. Sort Tasks by Priority")
        print("4. Sort Tasks by Deadline")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            task_type = input("Enter task type (Personal/Work/Study): ")
            description = input("Enter task description: ")
            deadline = input("Enter task deadline (YYYY-MM-DD or special keyword like 'today', 'tomorrow'): ")
            priority = input("Enter task priority (1-5, where 1 is very important and 5 is not important): ")
            if task_type.lower() == "study":
                subject = input("Enter study subject: ")
                task = task_scheduler.create_task(task_type, description, deadline, priority, subject)
            else:
                task = task_scheduler.create_task(task_type, description, deadline, priority)
            task_manager.add_task(task)
            print("Task added successfully.")
        elif choice == "2":
            task_manager.display_tasks()
        elif choice == "3":
            task_manager.sort_by_priority()
            print("Tasks sorted by priority.")
        elif choice == "4":
            task_manager.sort_by_deadline()
            print("Tasks sorted by deadline.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
