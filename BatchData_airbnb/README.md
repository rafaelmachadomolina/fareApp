<!-- ABOUT THE PROJECT -->
# ETL for batch processing Airbnb data to the application

This section contains the main ETL to process the obtained data from Airbnb. There are two stages:
- Exploratory data analysis using the Jupyter notebook `EDA-airbinb.ipynb`
- ETL to move the data from *csv* files into the database using pySpark `ETL-airbinb.ipynb`

The latter section presents the proposed schema for the solution, inferred from the data but also enriched to better exploit features. In addition, the notebook saves a backup of the schema in a dedicated S3 bucket, backup format is *parquet*.

### Built With

* [Python3](https://www.python.org/downloads/)
* [pySpark](https://spark.apache.org/docs/latest/api/python/)
* [Great Expectations](https://greatexpectations.io)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

A few setups are required to fully run the ETL.

### Prerequisites

An environment with Python3 will suffice up to this point. No additional software is previously required.

### Installation

1. Run the installation script to get Java, Spark and the JDBC driver for PostgreSQL.
  ```sh
  bash init_spark.sh
  ```
2. Install *Great Expectations* on a Python virtual env. This framework is later used to validate data quality.
   ```sh
   pip install great_expectations
   ```
   
<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

Rafael Machado Molina - [@rafaelmachadom](https://twitter.com/rafaelmachadom) - r.machado.molina@gmail.com

Project Link: [https://github.com/rafaelmachadomolina/fareApp](https://github.com/rafaelmachadomolina/fareApp)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Great Expectations](https://github.com/great-expectations/great_expectations)
* [Best README template by othneildrew](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>
