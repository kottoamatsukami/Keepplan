import datetime
import os
from core import config as cfg
from core import task_tree


def main():
    # load config
    config = cfg.Config('./config.ini')

    # load tasks
    tasks = task_tree.TaskTree(config['Tree']['save_path'])
    tasks.update()

    # run cycle
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(tasks)

        command = input('>>: ').strip().lower()
        if   command == 'update':
            tasks.update()
        elif command == 'exit':
            exit(0)
        elif command == 'add':
            desc = input("Enter description    : ").strip()
            dead = input("Enter duration       : ").strip()
            if   'day' in dead:
                extra_timesteps = int(dead.replace('day', '').strip())*24*60*60
            elif 'hour' in dead:
                extra_timesteps = int(dead.replace('hour', '').strip())*60*60
            else:
                assert ValueError("Invalid duration format")

            prio = input("Enter priority       : ").strip()
            dead = int(datetime.datetime.today().timestamp()) + extra_timesteps
            tasks.push_task(
                task_tree.Task(
                    task_id   = tasks.tree.t,
                    deadline  = datetime.datetime.fromtimestamp(dead),
                    task_desc = desc,
                    priority  = int(prio)
                )
            )
        elif command == 'complete':
            tasks.complete()


if __name__ == '__main__':
    main()
