import streamlit as st

from utils.utils import get_task, save_tasks, Task, TaskStatus

if "tasks" not in st.session_state:
    st.session_state["tasks"] = get_task()

def add_task(title:str, description:str):
    task = Task(
        id=len(st.session_state.tasks)+1,
        title=title,
        description=description
    )

    st.session_state.tasks.append(task.model_dump())
    save_tasks(st.session_state.tasks)

def show_add_form():
    with st.expander("Agregar tarea", expanded=True):
        title = st.text_input("Título")
        description = st.text_area("Descripción")

        if st.button("Agregar"):
            add_task(title, description)

    #st.write(title)
    #st.write(description)

def show_tasks_by_status(status: TaskStatus):
    tasks = [task for task in st.session_state.tasks if task.get("status","") == status.value]

    if status == TaskStatus.PENDING:
        st.warning("Pending", icon="⚠️")
    elif status == TaskStatus.IN_PROGRESS:
        st.warning("In progress", icon="📌")
    else:
        st.warning("Completed", icon="✅")
        
    for task in tasks:
        task_id = task.get("id","")

        with st.expander(task.get("title",""), expanded=False):
            st.markdown(f":green[{task.get('timestamp','')}]")
            st.write(task.get("description",""))

def show_tasks():
    col_pending, col_in_progress, col_completed = st.columns(3)

    with col_pending:
        show_tasks_by_status(TaskStatus.PENDING)
    
    with col_in_progress:
        show_tasks_by_status(TaskStatus.IN_PROGRESS)

    with col_completed:
        show_tasks_by_status(TaskStatus.COMPLETED)

def main():
    st.header("Mi app del Curso GitHub")

    #Leer tarea
    #tasks = get_task()
    #print(tasks)
    
    #Mostrar el formulario
    show_add_form()
    show_tasks()

if __name__ == "__main__":
    main()