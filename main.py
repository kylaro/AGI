from GPT import GPTNode

def traverse_tree(node):
    results = {}
    node.process()
    if node.state == "executor":
        result = node.execute_task()
        results[node.id] = result
        print(f"Executor {node.id} completed task: {node.task}")
    elif node.state == "verifier":
        task_completed = node.verify_task(node.parent.result)
        if task_completed:
            print(f"Verifier {node.id} verified task: {node.task}")
            node.state = "done"
        else:
            print(f"Verifier {node.id} failed to verify task: {node.task}")
            # Handle task failure or create debugging tasks here

    for child in node.children:
        child_results = traverse_tree(child)
        results.update(child_results)

    return results

if __name__ == "__main__":
    main_task = "Create an ascii art of a cat"
    master_node = GPTNode(task=main_task)

    results = {}
    while master_node.state != "done":
        results = traverse_tree(master_node)

    print("All tasks completed and verified:")
    for task_id, code in results.items():
        print(f"{task_id}: {code}")
