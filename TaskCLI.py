import pandas as pd
import datetime
import os 

Tasks = pd.DataFrame(columns=['name', 'description', 'status', 'created_at', 'updated_at'])

# Get path 
script_dir = os.path.dirname(os.path.abspath(__file__))  
File_name = 'Tasks.json'
File_path = os.path.join(script_dir, File_name)

# Base functions
def load_tasks():
    global Tasks
    
    if not os.path.exists(File_path) or os.path.getsize(File_path) == 0:
        print('JSON file not found or empty, creating a new DataFrame')
        Tasks = pd.DataFrame(columns=['name', 'description', 'status', 'created_at', 'updated_at'])
        return Tasks
    
    try:
        loaded_tasks = pd.read_json(File_path, orient='records')
        
        if loaded_tasks.empty:
            print('JSON file is empty, creating a new DataFrame')
            Tasks = pd.DataFrame(columns=['name', 'description', 'status', 'created_at', 'updated_at'])
        
        Tasks = loaded_tasks
        Tasks.reset_index(drop=True, inplace=True)
        return Tasks
    except ValueError:
        print("Error parsing the JSON! The file might be corrupted.")
        Tasks =  pd.DataFrame(columns=['name', 'description', 'status', 'created_at', 'updated_at'])
        return Tasks

def save_file():
        Tasks.to_json(File_path, orient='records', indent=4, date_format="iso")

def create_task(name, description):
    global Tasks  
    new_task = {
        'name': name,
        'description': description,
        'status': 'to do',
        'created_at': datetime.datetime.now(),
        'updated_at': 'not updated'
    }
    Tasks = pd.concat([Tasks, pd.DataFrame([new_task])], ignore_index=True)
    save_file()  
    print(f'Task: [{name}] created successfully.')

def update_status(idx, status):
    if idx in Tasks.index:
        statuses = ['to do', 'started', 'in progress','finished']
        if status in statuses:
            Tasks.loc[idx, 'status'] = status
            Tasks.loc[idx, 'updated_at'] = datetime.datetime.now()
            print('Status updated')
            save_file()
            return Tasks
        else: 
            print(f'Error: please enter a valid status from: {statuses}')
    else:
        print('Error: please enter a valid index')

def remove_task(idx):
    if idx in Tasks.index:
        Task_name = Tasks.iloc[idx]['name']
        Tasks.drop(index=idx, inplace=True)
        Tasks.reset_index(drop=True, inplace=True)
        save_file()
        print(f"Task: [{Task_name}] successfully removed.")
    else:
        print(f'Error: please enter a valid index')
    
def visualize_status(status):
    statuses = ['to do', 'started', 'in progress','finished']
    if status in statuses:
        filtered_Tasks = Tasks[Tasks['status'] == status]
        if filtered_Tasks.empty:
            print(f'There are no tasks with the status {status}')
        else:
            print(filtered_Tasks)
        return
    else:
        print(f'Error: please enter a valid status from: {statuses}')
    
def info():
    commands = {
        'create(name,description)': 'creates a new task',
        'update(idx,status)' : 'update status of a task',
        'remove(idx)' : 'deletes task',
        'visualize_status' : 'uses status to sort tasks',
        'visualize': "displays the entire dataset",
        'reset': 'resets the DataFrame'
    }
    for k,v in commands.items():
        print(f'{k} --> {v}')

def visualize():
    if Tasks.empty:
        print('Empty dataset, please create a task')
    else:
        print(Tasks)

def reset():
    global Tasks
    Tasks.drop(Tasks.index, inplace=True)
    save_file()
    print('Reset completed')
    return Tasks

# Pre-CLI function calls
load_tasks()

if not Tasks.empty:
    print('Here is the dataset with its latest update:')
    visualize()

print('Type "info" to get the available commands')

# CLI functions
def interactive_mode():
    while True:
        command = input("Enter a command: ").strip().lower()
        
        if command == 'exit':
            print("Exiting the program...")
            break
        
        elif command.startswith('create'):
            try:
                _, name, description = command.split(maxsplit=2)
                create_task(name, description)
            except ValueError:
                print("Error: 'create' requires 2 arguments: name and description.")
        
        elif command.startswith('remove'):
            try:
                _, idx = command.split()
                idx = int(idx)
                remove_task(idx)
            except ValueError:
                print("Error: index must be an integer.")
        
        elif command.startswith('update'):
            try:
                _, idx, status = command.split()
                idx = int(idx)
                update_status(idx, status)
            except ValueError:
                print("Error: index must be an integer.")
        
        elif command.startswith('visualize_status'):
            try:
                _, status = command.split()
                visualize_status(status)
            except ValueError:
                print("Error: 'visualize_status' requires 1 argument (status).")
        
        elif command == 'visualize':
            visualize()
        
        elif command == 'reset':
            reset()
        
        elif command == 'info':
            info()
        
        else:
            print(f"Command '{command}' not recognized. Type 'info' to see the list of commands.")

if __name__ == '__main__':
    interactive_mode()
