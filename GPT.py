import openai
import uuid
import API_KEY

openai.api_key = API_KEY.API_KEY


class GPTNode:

    id_counter = 0
    def __init__(self, task=None, parent=None):
        self.id = GPTNode.id_counter
        GPTNode.id_counter += 1
        self.parent = parent
        self.children = []
        self.task = task
        self.state = "idle"


        # prompt = f"Do not include file extension. Only use lowercase letters and underscores. Write a filename that is relevant to the following task: {task}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You a file namer. You do not include file extensions. You always format your replies as firstword_secondword"},
                {"role": "user",
                 "content": f"Write a file name to describe the following task.\n'{self.task}'"},
            ],
        )

        self.task_short = response['choices'][0]['message']['content'].strip()
        print(f"{self}: I am born to do {self.task_short}")
        with open(f"{self.__str__()}_task_{self.task_short}.txt", "w") as f:
            f.write(self.task)

    def can_solve_task(self):
        # prompt = f"Answer only yes or no. Can the following task fully and completely be solved using a Python script: '{self.task}'?"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helper that will answer only either yes or no."},
                {"role": "user",
                 "content": f"Can the following task fully and completely be solved using a Python script: '{self.task}'?"},
            ],
        )
        answer = response['choices'][0]['message']['content'].strip().lower()
        print(f"{self}: Solving {self.task_short} via Python={answer} for {self.task[0:20]}")
        return "yes" in answer

    def decompose_task(self):
        # prompt = f"When writing subtasks, include complete context within each subtask. Fully and completely decompose the following task into all necessary subtasks: '{self.task}'"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a task decomposer. You include full context alongside each subtask description."},
                {"role": "user",
                 "content": f"Fully and completely decompose the following task into all necessary subtasks: '{self.task}'"},
            ],
        )
        print(f"{self}: decomposed task" )
        return response['choices'][0]['message']['content'].strip().split("\n")

    def execute_task(self):
        # prompt = f"Only respond with Python code. Write a full, complete, and executable Python script to accomplish the following task: '{self.task}'"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Python code generator. You can only write Python."},
                {"role": "user",
                 "content": f"Write a full, complete, and executable Python script to accomplish the following task: '{self.task}'"},
            ],
        )

        code = response['choices'][0]['message']['content'].strip()
        # prompt = f"Do not include file extension. Only use lowercase letters and underscores. Write a file name that is relevant to the following code:\n{code}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You a file namer. You do not include file extensions. You always format your replies as firstword_secondword"},
                {"role": "user",
                 "content": f"Write a file name to describe the following code.\n'{code}'"},
            ],
        )

        print(f"{self}: wrote a python script")

        file_name = response['choices'][0]['message']['content'].strip()
        with open(f"{self.__str__()}_code_{file_name}.py", "w") as f:
            f.write(code)
        return code

    def verify_task(self, code):
        # prompt = f"Answer only yes or no. Verify if the following Python code accomplishes the task. '{self.task}':\n{code}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code verifier. You always respond with either yes or no."},
                {"role": "user",
                 "content": f"Verify if the following Python code accomplishes the task. '{self.task}':\n{code}"},
            ],
        )
        return response['choices'][0]['message']['content'].strip().lower() == "yes"

    def generate_debug_prompt(self, code):
        # prompt = f"Generate a debug prompt for the following Python code that failed to accomplish the task: '{self.task}'\n code:\n{code}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a debug prompt generator."},
                {"role": "user",
                 "content": f"Generate a debug prompt for the following Python code that failed to accomplish the task: '{self.task}'\n code:\n{code}"},
            ],
        )
        print(f"{self}: verified code??")
        return response['choices'][0]['message']['content'].strip()

    def process(self):
        if self.state == "idle":
            if self.can_solve_task():
                self.state = "executor"
                code = self.execute_task()
                self.state = "verifier"
                task_completed = self.verify_task(code)
                if task_completed:
                    self.state = "done"
                else:
                    debug_prompt = self.generate_debug_prompt(code)
                    debug_node = GPTNode(task=debug_prompt, parent=self)
                    self.children.append(debug_node)
            else:
                self.state = "decomposer"
                subtasks = self.decompose_task()
                for subtask in subtasks:
                    child = GPTNode(task=subtask, parent=self)
                    self.children.append(child)
        elif self.state == "decomposer" and all(child.state == "done" for child in self.children):
            self.state = "verifier"
            # Additional logic for spawning verifier nodes and
            # verification can be implemented here.
            verifier_node = GPTNode(task=f"Verify '{self.task}'", parent=self)
            self.children.append(verifier_node)
            task_completed = verifier_node.process()
            if task_completed:
                self.state = "done"
            else:
                # Handle task failure or create debugging tasks here
                print("Task not completed xxx")
                # In case of failure, reset the node's state to "idle" for reprocessing.
                self.state = "idle"

    def process_all_children(self):
        for child in self.children:
            child.process()
            if child.state not in ["done", "verifier"]:
                child.process_all_children()

    def __str__(self):
        if self.parent is not None and isinstance(self.parent, GPTNode):
            return str(self.parent.id) + "_" + str(self.id)
        else:
            return str(self.id)

    def __repr__(self):
        return self.__str__()