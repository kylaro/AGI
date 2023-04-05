# Goal Completion Bot (GCB) 
## A powerful task management system that leverages GPT (Generative Pre-trained Transformer) to create a multi-layered, tree-structured AI task management system. This system allows you to break down complex tasks into smaller, manageable subtasks, which are executed and verified by multiple GPT instances organized in a tree data structure.

# Repository Structure
## The repository consists of two main files:

### main.py: 
The entry point of the GCB system.

### GPT.py: 
contains the GPTNode class, which represents a GPT instance with tree-like properties.

### GPTNode Class
The GPT.py file contains the GPTNode class, which initializes a text-davinci-002 instance and has similarities to a tree or graph node. These similarities include keeping track of parent and child instances of the same class. The node has a state that tracks the progress of the task to be completed.

### The GPTNode class has the following primary attributes:

parent: A reference to the parent GPTNode instance.
children: A list of child GPTNode instances.
state: The current state of the node, tracking the progress of the task.

# Workflow
## The following is a detailed description of the GCB workflow using the provided example:

### Initialize master node: 
A single master GPTNode is created with a goal, e.g., "create a personal blog with photos of cats and written articles about creating AI and host it locally".
### Task decomposition: 
The master node breaks down the goal into subtasks.
### Spawn executor and verifier nodes: 
The master node creates two new GPTNode instances for each subtask - an executor node and a verifier node. The executor node is given the subtask, while the verifier node is given instructions on how to verify the task is completed. The verifier node is added as a child of the executor node.
### Create the tree: 
The process continues recursively, building a tree of GPTNode instances until all subtasks have been assigned.
### Execute subtasks: 
Leaf nodes begin by writing Python code to solve their tasks. Nodes labeled as executors are executed first.
### Verify subtasks: 
Verifier nodes wait for their executor neighbors to finish before verifying the tasks. If a task is not completed, the verifier node creates debugging tasks and spawns its own subtree to address the issue.
### Result aggregation: 
Once all tasks have been completed and verified, the results are aggregated and returned to the user.