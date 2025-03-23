# Snowflake 指南

Snowflake 数据仓库指南

* * *

## 是什么和为什么

[Snowflake](https://www.snowflake.com/en/) 是我们的企业数据仓库（EDW），是我们[企业数据平台](https://handbook.gitlab.com/handbook/enterprise-data/platform/#i-classfas-fa-cubes-fa-fw--text-orangeiour-data-stack)的核心技术。

## Snowflake 包含什么？

Snowflake 包含我们所有的分析数据和[数据源](https://handbook.gitlab.com/handbook/enterprise-data/platform/#data-sources)，定义了可用的原始/原始数据集。

## 相关内容

  * [访问](https://handbook.gitlab.com/handbook/enterprise-data/platform/#warehouse-access)
  * [支持门户访问](https://handbook.gitlab.com/handbook/enterprise-data/platform/#snowflake-support-portal-access)
  * [计算资源](https://handbook.gitlab.com/handbook/enterprise-data/platform/#compute-resources)
  * [数据脱敏](https://handbook.gitlab.com/handbook/enterprise-data/platform/#data-masking)
  * [备份](https://handbook.gitlab.com/handbook/enterprise-data/platform/#backups)

## 登录

从 Okta 登录 Snowflake。

## 导航界面

[Snowflake Web 界面快速导览](https://docs.snowflake.com/user-guide/ui-snowsight-quick-tour)提供了全面的界面文档。

## Snowflake 账户配置

### ABORT_DETACHED_QUERY

[ABORT_DETACHED_QUERY](https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query) 参数在账户级别设置为 `True`。

我们经常遇到连接丢失而查询继续尝试运行且仍未完成的情况。在这些情况下，查询继续运行是没有意义的，也不会带来任何价值。有一个 5 分钟的宽限期。如果连接在 5 分钟内没有修复，它将停止执行，这样仓库就不会不必要地运行。

## 数据新鲜度

我们利用 `MonteCarlo` 中的自动监控器来监控数据的新鲜度。

* * *

#####  [Snowflake 中的聚类](https://handbook.gitlab.com/handbook/enterprise-data/platform/snowflake/clustering/)

正确和负责任地使用 Snowflake 聚类的指南

#####  [Snowflake SNS 集成用于 Snowflake SnowPipe 和任务失败](https://handbook.gitlab.com/handbook/enterprise-data/platform/snowflake/snowpipe/)

## 概述

当 Snowpipe 在加载数据时遇到错误（即通过 snowpipe）或 snowflake 任务失败时，它可以向云消息服务推送错误通知。这些通知描述了每个文件中遇到的错误，使能够进一步分析 snowpipe 文件中的数据。任务错误通知触发一个通知，描述任务执行 SQL 代码时遇到的错误。这些通知描述了任务执行期间遇到的任何错误。

最后修改时间：2025年1月4日：[修复不正确或损坏的外部链接 (`55741fb9`)](https://gitlab.com/gitlab-com/content-sites/handbook/commit/55741fb9) 