from GPT import GPTNode

def traverse_tree(node):
    results = {}
    for child in node.children:
        if child.role == "executor":
            result = child.process()
            if result is not None:
                results[child.id] = result
                print(f"Executor {child.id} completed task: {child.task}")

        if child.role == "verifier":
            task_completed = child.process()
            if task_completed is not None:
                print(f"Verifier {child.id} verified task: {child.parent.task}")
            else:
                print(f"Verifier {child.id} failed to verify task: {child.parent.task}")
                # Handle task failure or create debugging tasks here

        child_results = traverse_tree(child)
        results.update(child_results)

    return results

if __name__ == "__main__":
    main_task = "Create a personal blog with photos of cats and written articles about creating AI and host it locally"
    master_node = GPTNode(task=main_task)

    subtasks = master_node.decompose_task()
    for subtask in subtasks:
        executor = master_node.create_child(task=subtask, role="executor")
        verifier = executor.create_child(task=f"Verify {subtask}", role="verifier")

    results = traverse_tree(master_node)
    print("All tasks completed and verified:")
    for task_id, code in results.items():
        print(f"{task_id}: {code}")
