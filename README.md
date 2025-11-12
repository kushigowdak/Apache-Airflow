# 🚀 Lab 6: Apache Airflow – Building and Managing Data Workflows


## 🎯 Objective

The main goal of this project is to learn how to use **Apache Airflow** to create and manage **data workflows**.  
This lab focuses on:

- Understanding the core components of Airflow — **DAGs**, **tasks**, and **operators**.  
- Building and running an **ETL pipeline (Extract, Transform, Load)**.  
- Setting up **Apache Airflow on Windows using Docker**.  
- Running and monitoring a **sample workflow** to see how tasks are scheduled and executed.

---

## 🧩 Outcomes

By completing this exercise, you will have:

- Learned how **Apache Airflow** works and how it automates complex data workflows.  
- Understood core components like **DAGs**, **tasks**, **operators**, **scheduler**, and **executor**.  
- Successfully **installed and configured Airflow** using **Docker on Windows**.  
- Created and executed a **sample ETL workflow** demonstrating dependencies and execution order.  
- Gained hands-on experience in **monitoring and managing workflows** using the Airflow **Web UI**.

---

## ⚙️ Materials

### 🖥️ Hardware Requirements
- A personal computer or laptop  
- Minimum **8 GB RAM**  
- Stable internet connection  

### 🧰 Software Requirements
- **Operating System:** Windows 10 / 11  
- **Apache Airflow**  
- **Docker Desktop**  
- **Python (Optional for custom scripts)**  
- **Web Browser** – for accessing the Airflow UI  
- **Command Prompt / Terminal** – for running Docker commands  

---

## 🧱 Tools Used

| Tool | Purpose |
|------|----------|
| **Apache Airflow** | Workflow orchestration and automation |
| **Docker Desktop** | Containerized Airflow deployment |
| **Python** | Used for defining DAGs and ETL tasks |
| **Web Browser** | Accessing Airflow web interface |

---

## 🧪 Lab Procedure

### 1. Install Docker Desktop
- Download and install Docker Desktop from the official website:  
  🔗 [https://docs.docker.com/desktop/](https://docs.docker.com/desktop/)
- Ensure Docker is running properly before proceeding.

---

### 2. Set Up Apache Airflow with Docker

1. Download or create a **Dockerfile** for setting up Apache Airflow.  
2. Open **Command Prompt** and navigate to your project directory.

Run the following commands:

```bash
docker build -t airflowsqlserver -f Dockerfile --no-cache
docker-compose up
````

This will build the Docker image and start all required Airflow services.

---

### 3. Access the Airflow Web Interface

After the containers start successfully, open a web browser and visit:

👉 **[http://localhost:9099/home](http://localhost:9099/home)**

This opens the **Apache Airflow Web UI**.

---

### 4. Create and Configure a DAG

1. Inside your Airflow project folder, create a new Python file for the DAG, e.g.

   ```
   dags/sample_etl_dag.py
   ```

2. Define a sample ETL workflow in the DAG file:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define simple Python functions
def extract():
    print("Extracting data...")

def transform():
    print("Transforming data...")

def load():
    print("Loading data...")

# DAG definition
with DAG(
    dag_id='sample_etl_dag',
    start_date=datetime(2025, 9, 17),
    schedule_interval='@daily',
    catchup=False,
    description='A simple ETL workflow example'
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load
    )

    # Set task dependencies
    extract_task >> transform_task >> load_task
```

---

### 5. Run and Monitor the DAG

1. Open the **Airflow Web UI** → You’ll see `sample_etl_dag` listed.
2. Turn on the DAG toggle and **Trigger** it manually.
3. Navigate to the **Graph View** to see the task flow.
4. Monitor **task execution**, **logs**, and **status** from the UI.

---

## 📊 Understanding Airflow Components

| Component                        | Description                                                             |
| -------------------------------- | ----------------------------------------------------------------------- |
| **DAG (Directed Acyclic Graph)** | A collection of tasks defining a workflow and its dependencies          |
| **Task**                         | A single unit of work in a DAG                                          |
| **Operator**                     | Template defining the type of work (e.g., PythonOperator, BashOperator) |
| **Scheduler**                    | Decides when to run tasks based on the schedule                         |
| **Executor**                     | Runs tasks, often in parallel                                           |
| **Web Server (UI)**              | Allows monitoring and managing DAGs visually                            |

---

## 🧭 Key Learnings

* **Airflow DAGs** define workflows as code, enabling better version control and automation.
* **Operators** make it easy to integrate with different systems.
* Using **Docker**, you can deploy Airflow quickly without manual dependency setup.
* The **Web UI** provides clear visibility into task execution and debugging.
* Airflow enables **reliable, repeatable, and maintainable** data workflows.

---


## 🏁 Conclusion

This lab demonstrates how to **install, configure, and operate Apache Airflow** using **Docker on Windows**.
You learned how to define and manage **ETL workflows** using **DAGs**, how tasks are scheduled and executed, and how to **monitor workflows** via the **Airflow Web UI**.
This foundation is essential for orchestrating **real-world data pipelines** in data engineering environments.


