from coordinator import Coordinator
from generator import TaskGenerator
from logTools import LogLevel, COLOR_CODES
from verificator import Verificator


if __name__ == '__main__':
    generator = TaskGenerator()
    task_results = {}

    for _ in range(len(generator)):
        task = generator.generate_task()
        task_id = task['task_id']
        task_results[task_id] = [task['answer'], "No answer"]

        try:
            coordinator = Coordinator(LogLevel.RELEASE)
            result = coordinator.solve(task['statement'])
            task_results[task_id][1] = result['answer']
        except Exception as e:
            print(f"Coordinator error: {e}")

    success = 0
    status_colors = {
        'CORRECT': COLOR_CODES['green'],
        'EQUIVALENT': COLOR_CODES['yellow'],
        'WRONG': COLOR_CODES['red']
    }
    verificator = Verificator(LogLevel.RELEASE)

    for task_id, (correct, answer) in task_results.items():
        if correct == answer:
            status = 'CORRECT'
        else:
            verification = verificator.verify(correct, answer)
            status = 'EQUIVALENT' if verification['verdict'] == 'EQUIVALENT' else 'WRONG'

        success += status in {'CORRECT', 'EQUIVALENT'}
        print(f'Task {task_id}: expected="{correct}", got="{answer}" → {status_colors[status]}{status}\033[0m')

    total = len(generator)
    print(f'\n{"="*40}')
    print(f'Results: {success}/{total} tasks completed successfully')
    print(f'Success rate: {success/total*100:.1f}%' if total > 0 else 'No tasks')
