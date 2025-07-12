class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")

    def __str__(self):
        status = "✔" if self.completed else "✘"
        return f"[{status}] {self.title}"

class User:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")

    def summary(self):
        lines = [f"Task summary for {self.name}:"]
        if not self.tasks:
            lines.append("No tasks assigned.")
        else:
            for idx, task in enumerate(self.tasks, 1):
                lines.append(f"{idx}. {task}")
        return "\n".join(lines)

    def write_log(self, filename="task_log.txt"):
        with open(filename, "w") as f:
            f.write(self.summary())
        print(f"📝 Log summary written to {filename}")

# Example usage
if __name__ == "__main__":
    user = User("Alice")
    task1 = Task("Finish report")
    task2 = Task("Call Bob")

    user.add_task(task1)
    user.add_task(task2)

    task1.complete()

    # Write summary log to file
    user.write_log()
