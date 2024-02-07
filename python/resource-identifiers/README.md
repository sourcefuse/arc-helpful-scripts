# Resource Identifiers
<!-- TOC -->
* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
  * [Dependencies](#dependencies)
  * [Configuring](#configuring)
  * [Execution](#execution)
* [AWS Tagger](#aws-tagger)
  * [Installation](#installation)
  * [Usage](#usage-1)
<!-- TOC -->

## Overview
The modules defined in this folder are intended for use in conjunction with [aws-tagger](https://github.com/washingtonpost/aws-tagger.git) to output a CSV with the correct
column names and values used for mass-tagging `map-migrated` resources.
Current AWS services that this module supports:
* DynamoDB
* EC2
* Lambda Functions
* S3 (`aws-tagger` isn't able to update tags for previously-tagged buckets)

## Prerequisites
* Python3
* Access to all AWS resources

## Usage
**NOTE**
* This section assumes you are in the root of the `resource-identifiers` folder when running these commands.

This module is used for gathering the Ids / ARNs of all resources in a supported region. This will output a CSV which
can be used with the [aws-tagger](https://github.com/washingtonpost/aws-tagger.git) CLI.

### Dependencies
* Create your virtual environment
  ```shell
  python3 virtualenv venv
  ```
* Activate your virtual environment
  ```shell
  source venv/bin/activate
  ```
* Install the requirements
  ```shell
  pip install -r requirements.txt
  ```

### Configuring
This section assumes you are in the root of the `resource-identifiers` folder when running these commands.
Open [`main.py`](./main.py) and modify the `Config` class with the tags you want added to your AWS resources.

### Execution
**NOTE**
* This section assumes you are in the root of the `resource-identifiers` folder when running these commands.
* This section assumes you have activated your virtual environment. See [Dependencies](#dependencies-) for more information.

**Run**
* Execute `main.py` via terminal
  ```shell
  python main.py
  ```
* This will output a `tags.csv` for usage with [aws-tagger](https://github.com/washingtonpost/aws-tagger.git)

## AWS Tagger
This CLI is managed by Washington Post.

### Installation
* From your activated virtual environment (see [Dependencies](#dependencies-)), you will run `pip install aws-tagger`

### Usage
**NOTE**
* The `aws-tagger` CLI **WILL** tag all resources defined in the CSV output by our `resource-identifiers` module.

**Run**
* Once you have the `tags.csv` file, you can run the following command:
  ```shell
  aws-tagger --csv tags.csv
  ```
