# ETL Pipeline: Pandas + Airflow + Power BI

**🚀 Project Goal:**  
Automated data preparation, transformation, and visualization of sales data using Jupyter Notebook, Apache Airflow, and Power BI.

---

## 🔧 Technologies

- **Pandas** – for data cleaning and transformation  
- **Apache Airflow** – for scheduling and automation  
- **Docker + docker-compose** – for environment setup  
- **Power BI** – for dashboard and reporting
---

## 🗂️ Project Structure

```
├── dags/                       # Airflow DAG files
├── data/
│   └── dirty_cafe_sales.csv   # Raw sales data
├── ETL_TEST.ipynb             # Exploratory ETL notebook
├── Dockerfile & docker-compose.yml
├── requirements.txt           
└── README.md                  
```

---

## 1. Data Preparation (Jupyter Notebook)

In the **`ETL_TEST.ipynb`** file, the following steps were performed:
1. Loaded data from `dirty_cafe_sales.csv`
2. Initial data exploration and cleaning using Pandas:
   - removed errors, handled nulls, corrected data types
3. Preliminary analysis: visualizations and descriptive statistics
4. Saved the cleaned data into a CSV file prepared for the Airflow pipeline

---

## 2. ETL in Apache Airflow 

Inside the `dags/` folder, the file `etl_dag.py` defines a DAG with the following logic:

- **Trigger:** Scheduled or manually triggered  
- **Steps:**
  1. *transform* – loading data and further cleaning/aggregation using Pandas
  2. *load* – save final output CSV to a target folder (e.g., `data`)
- The pipeline runs automatically based on a defined schedule (e.g., daily)

**📌 DAG diagram:**  
![image](https://github.com/user-attachments/assets/9b9b593c-f9a6-43c5-8ff9-9c82139d7e2a)


---

## 3. Analysis & Dashboard in Power BI 📊  

The final stage involves loading the cleaned data from Airflow into Power BI, where a dashboard is created with:

- Sales metrics: daily, monthly, seasonal comparisons
- Interactive charts: lines, bars, maps
- Filtering by region, product, category

**📌 Power BI dashboard:**  
![image](https://github.com/user-attachments/assets/6f0aa0b6-82f8-48c7-8b9f-5a7fa9045486)


---

## 🖥️ How to Run the Project

1. ***Initializing Docker Containers***
```
  docker compose up airflow-init   
  docker compose up                
```

2. **Access Airflow UI:**  
   Go to [http://localhost:8080](http://localhost:8080), trigger the DAG, check logs and outputs in the `data` folder.

3. **Load data into Power BI Desktop:**  
   Import the output CSV from `data`, refresh the source, and build your dashboard.

---

## ✅ Summary

- Data was **initially prepared in a Jupyter Notebook**
- A **DAG was then created in Apache Airflow** to automate the ETL process (extract-transform-load)
- Finally, the clean data was **analyzed in Power BI**, resulting in a professional dashboard
