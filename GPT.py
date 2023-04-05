import openai
import uuid

import API_KEY

openai.api_key = API_KEY.API_KEY

class GPTNode:
    def __init__(self, task=None, parent=None, role="executor"):
        self.id = uuid.uuid4()
        self.parent = parent
        self.children = []
        self.task = task
        self.role = role
        self.state = "idle"

    def decompose_task(self):
        prompt = f"Decompose the following task into smaller subtasks: '{self.task}'"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip().split("\n")

    def execute_task(self):
        prompt = f"Write Python code to accomplish the following task: '{self.task}'"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

    def verify_task(self, code):
        prompt = f"Verify if the following Python code accomplishes the task '{self.task}':\n{code}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip().lower() == "yes"

    def create_child(self, task, role):
        child = GPTNode(task=task, parent=self, role=role)
        self.children.append(child)
        return child

    def process(self):
        if self.role == "executor":
            if self.state == "idle":
                self.state = "executing"
                code = self.execute_task()
                self.state = "completed"
                return code
            else:
                return None
        elif self.role == "verifier":
            if self.state == "idle" and self.parent.state == "completed":
                self.state = "verifying"
                task_completed = self.verify_task(self.parent.result)
                self.state = "verified"
                return task_completed
            else:
                return None
