from coordinator import Coordinator
from generator import TaskGenerator
from logTools import LogLevel, COLOR_CODES


if __name__ == '__main__':
    generator = TaskGenerator()
    task_results = {}
    
    for _ in range(len(generator)):
        task = generator.generate_task()
        task_id = task['task_id']
        task_results[task_id] = [task['answer'], None]
        
        try:
            coordinator = Coordinator(LogLevel.RELEASE)
            result = coordinator.solve(task['statement'])
            task_results[task_id][1] = result['answer']
        except Exception as e:
            print(e)

    success = 0
    status_colors = {'CORRECT': COLOR_CODES['green'], 'WRONG': COLOR_CODES['red']}

    for task_id, (correct, answer) in task_results.items():
        status = 'CORRECT' if correct == answer else 'WRONG'
        success += status == 'CORRECT'
        print(f'Task {task_id}: expected="{correct}", got="{answer}" → {status_colors[status]}{status}\033[0m')

    total = len(generator)
    print(f'\n{"="*40}')
    print(f'Results: {success}/{total} tasks completed successfully')
    print(f'Success rate: {success/total*100:.1f}%' if total > 0 else 'No tasks')
