# Delete AWS Config
<!-- TOC -->
* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
  * [Dependencies](#dependencies)
  * [Configuring](#configuring)
  * [Execution](#execution)
<!-- TOC -->

## Overview
This module is intended to run against an account that is being enrolled under a Control Tower managed Organization.

## Prerequisites
* Python3
* Access to all AWS Config resources

## Usage
**NOTE**
* This section assumes you are in the root of the `delete-aws-config` folder when running these commands.

This will **DELETE** all AWS Config settings that exist (in each supported region) in order for a smooth Control Tower enrollment process.
If AWS Config settings are detected by Control Tower during the enrollment, the enrollment will fail.

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
This section assumes you are in the root of the `delete-aws-config` folder when running these commands.

### Execution
**NOTE**
* This section assumes you have activated your virtual environment. See [Dependencies](#dependencies-) for more information.

**Run**
* Execute `main.py` via terminal
  ```shell
  python main.py
  ```
* This will loop through each region and delete the AWS Config settings for that region.
