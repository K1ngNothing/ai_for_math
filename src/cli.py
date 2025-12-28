from coordinator import Coordinator
from generator import TaskGenerator

if __name__ == '__main__':
    generator = TaskGenerator()
    coordinator = Coordinator()
    
    success = 0
    for _ in range(len(generator)):
        task = generator.generate_task()
        # if task['task_id'] != 10:
        #     continue
        result = coordinator.solve(task['statement'])
        print(f'Answer for task with id {task['task_id']} is {result}. Correct answer is {task['answer']}')
        if task['answer'] == result:
            success += 1
    print(f'Total number of tasks is {len(generator)}. Correctly solved: {success}. Winrate is {success / len(generator)}')