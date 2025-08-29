<p align="center">
  <img src="Ana-lattex_Logo.png" alt="Ana-LatteX Logo" width="400" height="400"/>
</p>

# Super Café ETL Pipeline

**This repository is for the Super Café Project by Ana-LatteX**  
*Ana-LatteX — Automated ETL & BI*

---

## Summary
Fully automated ETL pipeline (local & AWS): ingest daily branch CSVs, clean and normalize transaction and order data, load into PostgreSQL (local) or Redshift (AWS). Visualize trends and insights with Grafana dashboards for branch and product performance.

---

## Table of Contents
1. [Overview of the Project](#overview-of-the-project)  
2. [Repository Contents](#repository-contents)  
3. [Simplified Explanation for Stakeholders](#simplified-explanation-for-stakeholders)  
4. [System Architecture & Data Flow](#system-architecture--data-flow)  
5. [Pipeline Workflow](#pipeline-workflow)  
6. [Getting Started for Developers](#getting-started-for-developers)  
7. [Deployment Instructions](#deployment-instructions)  
8. [Configuration and Secrets Management](#configuration-and-secrets-management)  
9. [Monitoring & Analytics](#monitoring--analytics)  
10. [Testing & Quality Checks](#testing--quality-checks)  
11. [Future Improvements](#future-improvements)  
12. [Team Contacts](#team-contacts)  

---

## Overview of the Project
This ETL pipeline automates the ingestion, transformation, and storage of daily transaction data from multiple café branches. Key benefits:

- Centralized storage of branch transactions  
- Standardized data format for analytics  
- Real-time business insights via Grafana  
- Scalable architecture supporting AWS deployment and local testing  

---

## Repository Contents

```.
├── AWS/                  # AWS deployment scripts
├── Database/             # Database schema and scripts
├── Sample Data 2/        # Sample CSV files
├── data/                 # Raw CSV files
├── doc/                  # Documentation
├── etl/                  # ETL pipeline code
├── src/                  # Source code
├── test/                 # Unit tests
├── .Ana-lattex_Logo.png  # Team logo
├── .env                  # Environment variables
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation        
└── ana-lattex.md         # Additional documentation
```


---

## Simplified Explanation for Stakeholders
- Each branch produces a daily CSV file.  
- Current reporting is manual and per-branch.  
- The Ana-LatteX ETL pipeline automates ingestion and loading into a central database.  
- Grafana dashboards provide branch- and product-level analytics, enabling faster decision-making.  

**High-level vision:**  
`Daily CSV → Automated ETL → Central Database → Grafana BI Dashboards`


## System Architecture & Data Flow

**ETL Flow Overview:**


| Local ETL Diagram | AWS ETL Diagram |
|-----------------|-----------------|
| <img src="Local etl pipeline architecture.png" width="300px" alt="AWS ETL Diagram"/> | <img src="AWS etl pipeline architecture.png" width="300px" alt="Local ETL Diagram"/> |

**Diagram Descriptions:**

- **Local ETL Diagram:** Shows the local pipeline where branch CSVs → Transformation Script → PostgreSQL Database → Local analytics/reporting.
- **AWS ETL Diagram:** Shows the data flow from branch CSVs → S3 Raw Bucket → Lambda ETL → Cleaned Data in S3 → Grafana dashboards for analytics.

 
**Database Schema:** 

- `branches`  
  - `branch_id` UUID **PK**  
  - `branch_name` TEXT **UNIQUE**  

- `products`  
  - `product_id` UUID **PK**  
  - `product_name` TEXT  
  - `price` NUMERIC  
  - **Constraint:** Unique on (`product_name`, `price`)  

- `orders`  
  - `order_id` UUID **PK**  
  - `datetime` TIMESTAMP  
  - `branch_id` UUID **FK → branches(branch_id)**  
  - `payment_type` TEXT  
  - `total_price` NUMERIC  

- `order_items`  
  - `order_item_id` UUID **PK**  
  - `order_id` UUID **FK → orders(order_id)**  
  - `product_id` UUID **FK → products(product_id)**  
  - `quantity` INTEGER (default 1)  
  - `item_price` NUMERIC (optional: quantity × product price)  

---
---

## Pipeline Workflow

The Ana-LatteX ETL pipeline supports **two independent workflows**: one for **local testing** and another for **AWS/cloud deployment**.  
**High-Level ETL Flow (Separate Pipelines):**  
- **Local:** `Branch CSVs → Local ETL → PostgreSQL → Grafana`  
- **AWS:** `Branch CSVs → S3 → Lambda ETL → Redshift → Grafana`

---

### **A. Local ETL Pipeline**
Processes daily branch CSVs on a local machine and loads data into PostgreSQL.  

1. **File Detection:**  
   - Monitor a local folder for new CSV files.  

2. **Data Extraction:**  
   - Read CSV files using `etl.extract_csv()`.  
   - Validate structure and remove duplicates or corrupt rows.  

3. **Data Transformation:**  
   - Use `etl.transform_row()` to split orders and items.  
   - Generate UUIDs for branches, orders, and products.  
   - Normalize branch and product fields.  
   - Assign default `quantity = 1` if missing.  

4. **Database Preparation:**  
   - Create tables if missing using `sql_utils.create_db_tables()`.  
   - Ensures unique branches and products, and proper foreign key relationships.  

5. **Data Loading:**  
   - Insert unique branches (`branches`).  
   - Upsert unique products (`products`).  
   - Insert orders (`orders`) and link to branches.  
   - Insert order items (`order_items`) linked to orders and products.  

6. **Visualization:**  
   - Grafana dashboards visualize local database insights: sales per branch, top-selling products, daily revenue trends.  

---

### **B. AWS ETL Pipeline**
Processes daily branch CSVs in the cloud and loads data into S3 and Redshift for analytics.  

1. **File Detection / Trigger:**  
   - CSV files uploaded to an **S3 raw bucket** trigger **AWS Lambda** functions.  

2. **Data Extraction & Transformation:**  
   - Lambda extracts CSV data and transforms it using the same rules as local ETL:  
     - Split orders and items  
     - Generate UUIDs  
     - Normalize branch and product data  
     - Assign default `quantity = 1`  

3. **Data Loading:**  
   - Store cleaned data in **S3 processed bucket**.  
   - Load transformed data into **Redshift** for analytics.  

4. **Deployment & Monitoring:**  
   - **CloudFormation** automates Lambda, S3, and IAM setup.  
   - **CloudWatch** logs Lambda executions for monitoring and auditing.  

5. **Visualization:**  
   - Grafana dashboards show real-time insights: sales per branch, top-selling products, daily revenue trends.  

---
## Getting Started for Developers 

### **Pre-requisites**
- **Python 3** – Download from [python.org](https://www.python.org/)
- For local database setup: **Docker Desktop** installed and running

---

### **A.To run Local ETL pipeline  (Beginner-Friendly)**
This mode saves data locally in CSV files. It is suitable for non-technical users and quick testing.  
⚠️ Not recommended for scalability or larger datasets – use a database instead.

1. **Download the project**
   - Clone via Git:  
     ```bash
     git clone https://github.com/DE-X6-LM/ana-lattex-de-x6-generation.git
     ```
   - Or download as `.zip`, extract, and navigate into the directory.

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv

- **Windows (CMD/PowerShell):**  
  ```bash
  .\venv\Scripts\activate

- **MacOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
Once active your command prompt will now show (venv) at the beginning.

3.**Docker setup:**
- Install & start Docker Desktop.
- Run Docker Compose:
  - In VS Code, click ▶️ on the docker-compose.yml file
  - or run:
      ```bash
      docker-compose up -d
      ```
  This starts Postgres + Adminer containers.
- Database credentials: 
  - Stored in .env file.
  - Access Adminer at http://localhost:8081
   (use credentials from .env).


4. **Run the application**
   ```bash
   python3 auto_etl.py
   ```

### B. To run AWS cloud ETL pipeline

#### 0. Configure AWS CLI and log in via VS Code terminal

- **Open VS Code terminal** in your project folder.

- **Install AWS CLI** (if not already installed):  
  - **macOS (using Homebrew):**
  ```bash
  brew install awscli
  ```
  -**Windows (via MSI installer):**
  ```bash
  https://aws.amazon.com/cli/
   ```
- **Configure AWS CLI with your credentials:**
  ```bash
  aws configure
  ```
   - Enter your AWS Access Key ID
   - Enter your AWS Secret Access Key
   - Set your default region (e.g., eu-north-1)
   - Choose default output format (e.g., json)

- **Verify configuration:**
  ```bash
  aws sts get-caller-identity
  ```
  You should see your AWS account ID and user ARN if configured correctly.

- **(Optional) Use environment variables instead of aws configure:**
  ```bash
  export AWS_ACCESS_KEY_ID=<your-access-key>
  export AWS_SECRET_ACCESS_KEY=<your-secret-key>
  export AWS_DEFAULT_REGION=<your-region>
  ```
   On Windows PowerShell, use $env:AWS_ACCESS_KEY_ID = "<your-access-key>" etc.


**1. Deploy the pipeline (if not already deployed):**
If you have the deployment files included in the repo, you can deploy all AWS services using CloudFormation templates:

 **Deploy S3 buckets:**
  ```bash
  aws cloudformation deploy --template-file deployment/s3_buckets.yaml --stack-name supercafe-s3
  ```

 **Deploy Lambda functions:**
  ```bash
  aws cloudformation deploy --template-file deployment/lambda_stack.yaml --stack-name supercafe-lambda
  ```
**2.Log in to AWS Management Console:**
  -Go to [https://aws.amazon.com/console/](https://aws.amazon.com/console/) and log in with your credentials.

**3.Check the S3 Buckets:**
  - Navigate to the **S3** service.
  - Open the raw bucket to see uploaded CSV files.
  -  Open the processed bucket (if applicable) to see transformed files.
    
**4.Check the Lambda Function:**
   - Navigate to the **Lambda** service.
   - Open the ETL Lambda function.
   - Review the **Code** and **Configuration**.
   - You can check **Monitoring → Logs** to see if the Lambda ran successfully.
     
**5.Optional – Trigger the Pipeline:** 
  - You can upload a new CSV file to the raw S3 bucket to trigger the Lambda ETL process.
  -  Check the processed bucket and Lambda logs to confirm successful execution.

  >Note: Make sure you have access to the AWS account where the pipeline is deployed.

## Configuration and Secrets Management

- **Local environment:** use a `.env` file (do not commit to version control).  
- **AWS:** store credentials in **SSM Parameter Store** or **Secrets Manager**.

## Monitoring & Analytics

- **Metrics:** `files_processed`, `rows_parsed`, `rows_loaded`, `errors`.  
- **Logs:** Local logs or **CloudWatch** (AWS).  
- **Dashboards:** Grafana visualizations of KPIs.

## Testing & Quality Checks

- Unit tests for ETL extraction and transformation functions.  
- CI should run tests before deployment.  
- **Common issues:** missing columns, connection issues, malformed CSV rows.

## Future Improvements

- Real-time streaming ingestion (**Kinesis** / **Kafka**).  
- Advanced BI: customer segmentation, forecasting.  
- Data lake / Redshift / Snowflake migration.  

## Team Contacts

**Team Ana-LatteX:**  
- **Developers:** Kimira, Michael, Rahidur, Prajakta  
- **Product Owners:** Jessica, Cindy




*-*-*-In-depth Project background-*-*-*

Our Cafe order application was a success, the client now wants to facilitate their unprecedented growth and expansion to hundreds of outlets.
The client wants to target new and returning customers to understand which of their products are best sellers.

Client requirements:
Current set up - 
*Each branch creates a CSV file of transactions daily at 8pm that are uploaded to software in back-office computers.
*To pull data for reporting, they have to manually collect the data from each location to collate, which is time consuming and it is difficult to colllect meaningful data for the company. 
*They would like a platform that will upload all the data to a centralised online location to allow for easier data manipulation and will help them identify trends to maxise revenue streams.

Consult results:
To resolve this data issue we will build a fully scalable ETL pipeline to handle large volumes of tranactional information.
This pipeline will collect all the transaction data generated by each individual cafe, and place it into a PostSQL database.
This will allow for easy access to relevant data to process, store and analyse.
New set up - 
* Each night a CSV for each branch will be uploaded to the cloud.
* The pipeline will read each file and Extract, Transform and Load the data.
* Data will be stored in a data warehouse.
* Data Analytics software will be used to create Business Intelligence analytics for the client.
* Application monitoring software used to produce operational metrics (i.e. system errors, up-time, etc).

Benefits and uses of each type of each set up:

*-*-File Based-*-*

To run Super cafe in its most basic form a file based version of the pipeline may be ran, this will allow for the pipeline, Extract, Load and transform functions to be saved locally, good for non-technical users and for testing file updates.  
Due to isolation, Debugging will be safer as there is no chance of messing up production/cloud data and Developers can run ETL locally on sample data before deploying.
uses - prototyping, PoC, schema debugging, unit tests, CI/CD pipelines.
However this will not be great for scalability so for larger data sets databases are reccommened.


-*-* local (PostgresSQL) database*-*-

To run the ETL on a local (PostgresSQL) database, this will allow for larger datasets that are still locally stored, free to run as no ongoing cloud costs. 
Low setup and cost - Free to run locally or on a small V, no ongoing cloud infrastructure costs and great for PoC, prototyping, and unit testing.
Postgres is ANSI SQL compliant with tons of extensions, so Easy to experiment with JSON, window functions, or PostGIS locally.
Good for devs iterating on schemas, transformations, or debugging ETL code.
As with file based less chance of messing up production/cloud data and Developers can run ETL locally on sample data before deploying.


-*-*-Cloud based Database (Redshift)-*-*-

Massive scale as it handles terabytes to petabytes of data efficiently.
Parallel processing + columnar storage optimized for analytics. Integration with AWS ecosystem such as  S3, Glue, Lambda, QuickSight, Grafana, etc.
Reliable due to backups, snapshots, scaling, failover handled by AWS.
Uses - production analytics warehouse with large datasets, multiple users, dashboards (Grafana, BI tools).
High concurrency + collaboration - Multiple analysts, dashboards, and apps can query simultaneously.
IAM + Secrets Manager integration for secure multi-user access.
Performance optimizations -Distribution keys, sort keys, materialized views, and workload management.
Auto-suspend (Serverless) saves cost when idle.

Data persistence:
All changes made in the apps menus will be automatically saved to the CSV files in the data directory. Dependant on the connection chosen, this is also handled by the local Postgres database and the AWS Redshift cloud database as it will allow for larger volumes of data to be saved without affecting the app.

How to run any unit tests:

Run unit tests with pytest -
# macOS / Linux

           python -m pytest -v -spython -m pytest -v -s

# Windows PowerShell

           py -m pytest -v -s


Week 1 Sprint:
Scrum master Prajakta 

Week 2 Sprint:
Scrum master Rahidur

Week 3 Sprint:
Scrum master Kimira

Week 4 Sprint:
Scrum master Michael

Week 5 Sprint 
Scrum master Rahidur
