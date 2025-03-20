

# Snowflake Guide

Snowflake Data Warehouse Guide

* * *

## What and why

[Snowflake](https://www.snowflake.com/en/) is our Enterprise Data Warehouse (EDW) and is the core technology in our [Enterprise Data Platform](https://handbook.gitlab.com/handbook/enterprise-data/platform/#i-classfas-fa-cubes-fa-fw--text-orangeiour-data-stack).

## What does Snowflake Contain?

Snowflake contains all of our analytical data and [Data Sources](https://handbook.gitlab.com/handbook/enterprise-data/platform/#data-sources) defines the set of original/raw data available.

## Related Content

  * [Access](https://handbook.gitlab.com/handbook/enterprise-data/platform/#warehouse-access)
  * [Support Portal Access](https://handbook.gitlab.com/handbook/enterprise-data/platform/#snowflake-support-portal-access)
  * [Compute Resources](https://handbook.gitlab.com/handbook/enterprise-data/platform/#compute-resources)
  * [Data Masking](https://handbook.gitlab.com/handbook/enterprise-data/platform/#data-masking)
  * [Backups](https://handbook.gitlab.com/handbook/enterprise-data/platform/#backups)



## Logging In

Login to Snowflake from Okta.

## Navigating the UI

The [Snowflake Quick Tour of the Web Interface](https://docs.snowflake.com/user-guide/ui-snowsight-quick-tour) provides comprehensive documentation for the UI.

## Snowflake account configuration

### ABORT_DETACHED_QUERY

[ABORT_DETACHED_QUERY](https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query) parameter is set on account level to `True`.

We often have cases where the connectivity was lost and the query keeps trying to run and still does not complete. It is meaningless for the query to keep running in these cases and adds no value. There is a grace period of 5 minutes. If the connectivity isn’t fixed in 5 minutes, it stops the execution so the warehouses won’t be running unnecessarily.

## Data Freshness

We leverage automatic monitors in `MonteCarlo` for monitoring the freshness of the data.

* * *

#####  [Clustering in Snowflake](https://handbook.gitlab.com/handbook/enterprise-data/platform/snowflake/clustering/)

Guide for correctly and responsibly using Snowflake's clustering

#####  [Snowflake SNS integration for Snowflake SnowPipe and task for failure](https://handbook.gitlab.com/handbook/enterprise-data/platform/snowflake/snowpipe/)

## Overview

Snowpipe can push error notifications to a cloud messaging service when it encounters errors while loading data i.e. through snowpipe or on failure of snowflake task. The notifications describe the errors encountered in each file, enabling further analysis of the data in the files for snowpipe. Task error notifications trigger a notification describing the errors encountered when a task executes SQL code. The notifications describe any errors encountered during task execution.

Last modified January 4, 2025: [Fix incorrect or broken external links (`55741fb9`)](https://gitlab.com/gitlab-com/content-sites/handbook/commit/55741fb9)

[ __View page source](https://gitlab.com/gitlab-com/content-sites/handbook/blob/main/content/handbook/enterprise-data/platform/snowflake/_index.md) \- [ __Edit this page](https://gitlab.com/-/ide/project/gitlab-com/content-sites/handbook/edit/main/-/content/handbook/enterprise-data/platform/snowflake/_index.md) \- please [contribute](https://handbook.gitlab.com/handbook/about/contributing/). [ ![Creative Commons License](../../images/handbook/enterprise-data/platform/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)
