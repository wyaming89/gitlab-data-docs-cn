

# Clustering in Snowflake

Guide for correctly and responsibly using Snowflake’s clustering

Snowflake supports [clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions), which is a powerful feature that allows users to optimize query performance by organizing data within micro-partitions. Clustering can significantly improve the efficiency of data retrieval, especially for large tables with frequently accessed columns.

## How Clustering Works

Clustering in Snowflake works by:

  1. Defining one or more columns as clustering keys
  2. Reorganizing data within micro-partitions based on these keys
  3. Maintaining the clustering order as new data is added or modified



This process helps Snowflake’s query optimizer to quickly locate and retrieve relevant data, reducing the amount of data that needs to be scanned.

## Benefits of Clustering

  * Improved query performance
  * Reduced compute costs
  * Better pruning of irrelevant micro-partitions
  * Enhanced data organization



## Costs of Clustering

  * Substantial upfront cost whenever the table is clustered (usually, this happens on full-refresh)
  * Marginal maintenance costs for ongoing updates to maintain the clustering order



## When to Use Clustering

If a model includes the `incremental_backfill_date` variable then it must also be configured to never fully refresh. These models can incur large re-clustering charges since the backfill DAG reprocesses months in random order which leads to an unsorted table. An example of this is `mart_behavior_structured_event`.

Models which can be fully refreshed without additional configuration can be clustered in the normal way as dbt will produce a clustered table.

Consider using clustering when:

  * Your table is large (typically > 1 TB)
  * You frequently query on specific columns
  * Your queries are experiencing performance issues in dbt, Snowsight, or Tableau; clustering the table that your query selects from can improve query performance.
  * You have high cardinality columns that are often used in WHERE clauses or JOINs



## How to Implement Clustering

### dbt syntax
    
    
    cluster_by=['column1','column2'],
    automatic_clustering='true'
    

The cluster key and automatic_clustering configuration setting must be added to the model so that automatic clustering is enabled by default should the model be rebuilt. A full-refresh of an incremental model will be required before the automatic clustering is enabled.

### Manual applying via SQL

Manual clustering of a table can be achieved by executing the following SQL command. However, it’s important to note that this method is not recommended for dbt models. The reason is that if the table is dropped and recreated through dbt, the clustering will not persist. For dbt models, it’s advisable to use the dbt code mentioned earlier to ensure proper and persistent clustering:
    
    
    ALTER TABLE your_table CLUSTER BY (column1, column2, ...);
    

Automatic-clustering needs to be enabled using the `RESUME RECLUSTER` command. For example:
    
    
    ALTER TABLE sales CLUSTER BY (date, region) RESUME RECLUSTER;
    

## Monitoring Clustering

Snowflake provides system functions to monitor clustering:
    
    
    SELECT SYSTEM$CLUSTERING_INFORMATION('your_table');
    

This function returns valuable information about the clustering state of your table. Some examples of how to interpret the information can be found in the [Snowflake docs](https://docs.snowflake.com/en/sql-reference/functions/system_clustering_information#examples).

Ideally, `average_overlaps` would be below 1 and `average_depth` would be ~ 1. A high number indicates the table is not well clustered.

## Best Practices

  1. Choose clustering keys wisely based on your query patterns
  2. Monitor clustering regularly
  3. Reconsider clustering if your table is small or experiences frequent updates
  4. Be aware of the additional storage and maintenance costs associated with clustering
  5. When a table with auto-clustering enabled is cloned, the cloned version will have auto-clustering turned off



By understanding and properly implementing clustering, you can significantly enhance the performance of your Snowflake queries and optimize your data warehouse operations.

Last modified January 15, 2025: [Update guidance on when a model is suitable for clustering (`d9b13aff`)](https://gitlab.com/gitlab-com/content-sites/handbook/commit/d9b13aff)

[ __View page source](https://gitlab.com/gitlab-com/content-sites/handbook/blob/main/content/handbook/enterprise-data/platform/snowflake/clustering/index.md) \- [ __Edit this page](https://gitlab.com/-/ide/project/gitlab-com/content-sites/handbook/edit/main/-/content/handbook/enterprise-data/platform/snowflake/clustering/index.md) \- please [contribute](https://handbook.gitlab.com/handbook/about/contributing/). [ ![Creative Commons License](../../images/handbook/enterprise-data/platform/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)
