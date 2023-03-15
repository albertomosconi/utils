import os

def parse_filename(filename: str):
    noext = task_folder.split('.')[0]
    ids, desc = noext.split('_')

    task, imgid = ids.split('-')

    return task, imgid, desc


def gen_ltx(id_task: str, id_img: str, desc: str):
    print("\subsection{}")
    print("\\begin{figure}[h]")
    print("\centering")
    print("\includegraphics[width=\\textwidth]{Figures/t" + id_task + '-' + id_img + '}')
    print(f"t {id_task} i {id_img}")

    print("\end{figure}")

for task_folder in sorted(os.listdir('src')):
    task_id, task_desc = task_folder.split('_')
    print(f'task {task_id}: {task_desc}')
    for subtask in sorted(os.listdir(os.path.join('src', task_folder))):
        print(subtask)
        ids, desc = subtask.split('@')
        print(len(ids.split('_')))
