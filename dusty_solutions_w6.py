from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Task abstract base class
class Task(ABC):
    def __init__(self, description, deadline):
        self.description = description
        self.deadline = deadline
        self.status = "Pending"

    @abstractmethod
    def display_details(self):
        pass

# PersonalTask subclass
class PersonalTask(Task):
    def __init__(self, description, deadline):
        super().__init__(description, deadline)
        self.type = "Personal"

    def display_details(self):
        return f"Type: {self.type}, Description: {self.description}, Deadline: {self.deadline}, Status: {self.status}"

# WorkTask subclass
class WorkTask(Task):
    def __init__(self, description, deadline):
        super().__init__(description, deadline)
        self.type = "Work"

    def display_details(self):
        return f"Type: {self.type}, Description: {self.description}, Deadline: {self.deadline}, Status: {self.status}"

# TaskManagement class
class TaskManagement:
    def __init__(self):
        self.task_list = []

    def add_task(self, task):
        self.task_list.append(task)

    def display_tasks(self):
        for task in self.task_list:
            print(task.display_details())

# Special Keywords Dictionary
SPECIAL_KEYWORDS = {
    "today": datetime.now().date(),
    "tomorrow": datetime.now().date() + timedelta(days=1),
    "next week": datetime.now().date() + timedelta(weeks=1)
}

def create_task(task_type, description, deadline):
    if task_type.lower() == "personal":
        return PersonalTask(description, deadline)
    elif task_type.lower() == "work":
        return WorkTask(description, deadline)
    else:
        raise ValueError("Invalid task type")

def parse_deadline(deadline_str):
    if deadline_str.lower() in SPECIAL_KEYWORDS:
        return SPECIAL_KEYWORDS[deadline_str.lower()]
    else:
        # Assume the input is in format "YYYY-MM-DD"
        return datetime.strptime(deadline_str, "%Y-%m-%d").date()

# Main function
def main():
    task_manager = TaskManagement()

    # Example usage
    task1 = create_task("personal", "Go for a run", "tomorrow")
    task2 = create_task("work", "Finish report", "2024-03-15")

    task_manager.add_task(task1)
    task_manager.add_task(task2)

    task_manager.display_tasks()

if __name__ == "__main__":
    main()
