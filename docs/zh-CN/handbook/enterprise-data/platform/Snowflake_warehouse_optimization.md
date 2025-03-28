# Snowflake 仓库优化

## 快速总结

为特定 dbt 模型选择正确仓库的指南：

  * 用户应该基于查询中扫描的分区数量来初步_估算_仓库大小
  * 通过增加仓库大小并比较"成本"与"查询时间减少"来进行基准测试
  * 在 dbt DAG 消耗的总积分背景下，为最小模型调整仓库大小并不会带来显著的成本降低

## 概述

在我们当前的 dbt 设置中，我们根据模型标签使用 `Large` 和 `X-Large` 仓库的组合来运行生产 dbt 作业。

然而，dbt 提供了在_模型_级别指定仓库大小的能力。

最初，我们考虑为每个模型调整仓库大小，并在[这个问题](https://gitlab.com/gitlab-data/analytics/-/issues/21802#note_2143766668)中进行了基准测试，以查看潜在的成本节省。我们发现，在查看总体积分消耗时，为较小的模型调整仓库大小并不会对消耗的积分产生关键影响。

然而，这并不意味着为模型调整仓库大小是不必要的任务。它只是表明我们应该有选择性地决定为哪些模型调整大小。由于调整每个模型的大小需要时间，应该将时间分配给当前消耗最多积分的模型。

本页面的其余部分将记录：

  1. 仓库效率的关键理论概念：
    * 仓库大小如何影响成本与性能
    * 什么构成我们需求最"高效"的仓库
    * 假设示例
  2. 如何调整仓库大小
    * 所需步骤
    * 实际示例
  3. 何时花时间调整模型大小
  4. 未来步骤

## 第一部分：仓库大小 - 概念

### 概念1：成本与性能

每次将仓库大小增加一个级别时，计算实例的 CPU 和 RAM 都会翻倍。相应地，通过消耗的积分，价格也会翻倍。

虽然_价格翻倍_，但在理想情况下，对于适当的工作负载/查询，由于计算实例资源翻倍，_查询时间会减少一半_。因此，在这种情况下，无论使用哪个仓库，你支付的价格都是相同的，但更大的仓库会将查询的运行时间减半，使其成为更高效的选择。

最终，如果你继续增加仓库大小，你会达到收益递减点，此时查询运行时间可能只会略微减少，而成本却不成比例地增加得更快。这是 select.dev 的[成本与性能图](https://images.app.goo.gl/K3asyxSqhJqP2hM76)说明了这一点[1]。

### 概念2：定义仓库效率

仓库效率有两个维度：成本和性能。注意，"仓库效率"是一个不同于[模型效率](https://handbook.gitlab.com/handbook/enterprise-data/platform/dbt-guide/#model-efficiency)的概念。

因为有两个维度，"仓库效率"没有一个明确的定义；它需要根据你如何权衡"成本"与"性能"来决定。

在我们的情况下，当使用不同的仓库时，我们希望实现以下两个结果之一：

  * _保持_现有运行时间同时降低成本
  * _减少_运行时间，而不会显著增加成本

基于上述要求，我们将仓库效率明确定义如下：

> **当与下一个更小的仓库相比时，如果查询运行时间减少 40% 或更多，则该仓库是高效的。**

解释：如前一节所述，对于下一个更大的仓库要实现收支平衡，它需要运行速度提高 2 倍（查询运行时间减少 **50%**）以补偿其 2 倍的价格增加。

在我们的定义中，我们要求运行时间至少减少 40%，这相当于成本最多增加 20%。我们不要求运行时间减少 50%（实现成本收支平衡）的原因是：

  * 我们需要保持性能接近现有的 dbt 运行时间
  * 我们希望迭代工作，这意味着设定一个更现实的目标，允许一些调整空间，然后在了解更多后调整目标。

旁注：计算运行时间的百分比改进

在这里要说明一个技术细节，查询运行时间的百分比改进可能有点令人困惑，因为当运行时间_减少_时性能会提高 - 这是一个反比关系。

我们将使用传统公式[2]计算运行时间的百分比改进：

$$ \frac{new - old}{old} \times 100% $$

例如，如果我们有值 `new = 5` 和 `old = 10`，计算将是：

$$ \begin{align*} \frac{new - old}{old} \times 100% &= \frac{5 - 10}{10} \times 100% \ &= \frac{-5}{10} \times 100% \ &= -50% \end{align*} $$

这意味着新值比旧值小 50%（更快，因为我们谈论的是响应时间）。

这可能听起来有点模糊，所以这里有一些假设示例：

#### 假设示例

##### 示例1

运行时间减少了 50%，从 1 小时 -> 30 分钟。在这种情况下，增加仓库大小是显而易见的：

仓库大小 | 积分/小时 | 运行时间（小时） | 成本
---|---|---|---
X-small | 1 | 1 | $2
Small | 2 | 0.5 | $2.00
% 增加 |  | -50% | 0%

##### 示例2

运行时间减少了 40%，从 1 小时 -> 36 分钟。同时，成本增加了 20%，从 $2 增加到 $2.40：

仓库大小 | 积分/小时 | 运行时间（小时） | 成本
---|---|---|---
X-small | 1 | 1 | $2.00
Small | 2 | 0.6 | $2.40
% 增加 |  | -40% | 20%

在这种情况下，增加仓库大小不再是一个显而易见的选择。现在这取决于你如何权衡成本与查询运行时间。

如果你只关心成本，你会坚持使用 X-small；如果你只关心速度，你会选择 Small。

在我们的情况下，我们希望在这两者之间找到平衡，所以我们使用之前建立的指南：

> **当与下一个更小的仓库相比时，如果查询运行时间减少 40%，则该仓库是高效的。**

在这种情况下，由于查询运行时间减少了 40%，它正好处于被认为是"高效"的阈值，我们应该选择 'S' 仓库。

##### 示例3

示例3，运行时间减少了 20%，从 1 小时 -> 48 分钟。同时，成本增加了 60%，从 $2 增加到 $3.20：

仓库大小 | 积分/小时 | 运行时间（小时） | 成本
---|---|---|---
X-small | 1 | 1 | $2.00
Small | 2 | 0.8 | $3.20
% 增加 |  | -20% | 60%

在这种情况下，查询将被视为"低效"，因为运行时间只减少了 20%。要被视为"高效"，运行时间需要减少 40% 或更多。因此，应该选择 'XS' 仓库。

## 第二部分：调整仓库大小的步骤

我们已经从理论上讨论了什么是"最优"仓库，但我们如何为每个模型选择正确的仓库？

以下是步骤：

  1. 运行[执行计划](https://docs.snowflake.com/en/sql-reference/sql/explain)以确定表有多少个分区
  2. 基于分区数量，使用 select.dev [分区数量图](https://images.app.goo.gl/KtS6aXsKhRzN7e3f6)来**估算**从哪个仓库开始
  3. 使用上一步估算的仓库在 `dbt` 中运行查询
  4. 检查下面的"基准测试启发式"部分，看看是否可以立即分配仓库；如果不能，继续
  5. 使用这个[Google 表格](https://docs.google.com/spreadsheets/d/1dh7cKTxeV3rUQ2J_k4nxPGbMe7IQFc-D1Rbahjsk5zc/edit?gid=1778011584#gid=1778011584)记录 `查询时间`
  6. 增加仓库大小
    * 现在，使用下一个更大的仓库重新运行查询
    * 再次在 Google 表格中记录结果
    * 当_成本_增加速度超过_性能_时停止

在以下部分中，我们将查看：

  * 为什么基准测试需要在 dbt 中进行
  * 我们将通过以下步骤查看两个调整仓库大小的示例：
    1. 简单查询：`gitlab_dotcom_deployment_todo_dedupe_source`
    2. 更复杂的查询，有更多分区：`prep_ci_stage`

### 为什么基准测试需要在 dbt 环境中进行

在上面的步骤列表中，它说明查询需要在 dbt 中运行。这是因为对于几乎所有模型，至少运行两组 SQL 语句。首先，运行一个 `SELECT` 语句，但此外，在后台还会运行以下两个语句之一：

  * 对于增量模型，运行 [`MERGE`](https://docs.snowflake.com/en/sql-reference/sql/merge) 语句
  * 对于新模型和完全刷新模型，运行 `CREATE TABLE` 语句

这些额外的 SQL 语句可能在计算上很昂贵，需要成为基准测试的一部分。

当使用 `dbt run` 时，这些语句会自动为你运行。因此，最好通过 dbt 运行所有仓库基准测试查询，无论是在本地还是通过 CI 作业。

#### 增量运行的基准测试

当特别对 `incremental` 模型进行基准测试时，"最高效"的仓库将根据是增量运行还是完全刷新运行而不同。

至少，增量运行应该这样进行基准测试：

  1. 相应的表应该完全加载
  2. 删除前一天的数据，然后使用基于分区大小估算的仓库_增量_运行模型

可选：也可以通过 `full_refresh` 运行来对模型进行基准测试。这样，可以根据是 `incremental` 还是 `full_refresh` 运行来配置不同的仓库：

```sql
{% if is_incremental() %}
  {{ config(
      warehouse='smaller_warehouse'  # 对增量运行使用此仓库
  ) }}
{% else %}
  {{ config(
      warehouse='larger_warehouse'  # 对完全刷新运行使用此仓库
  ) }}
{% endif %}

SELECT *
FROM my_table
```

### 实际基准测试示例

以下部分将查看两个如何遵循基准测试步骤的示例。

#### 示例1：gitlab_dotcom_deployment_todo_dedupe_source

第一步是运行执行计划，显示查询有 630 个分区：

```sql
EXPLAIN
SELECT
  *
FROM
  "RAW".tap_postgres.GITLAB_DB_TODOS
QUALIFY ROW_NUMBER() OVER ( PARTITION BY id ORDER BY _uploaded_at DESC) = 1;
```

第二步是根据上图选择基于分区数量的仓库。在这种情况下，有 630 个分区，我们可以从 `XS` 大小的仓库开始。

使用 `XS` 仓库，查询 `01b5ff9d-080a-e214-0000-289d77d4f1e2` 花费了 7m14s，所以我们将这些统计数据添加到 Google 表格模板中

接下来，我们将尝试使用 `M` 仓库。首先，让我们通过运行以下命令移除缓存：

```sql
ALTER SESSION SET USE_CACHED_RESULT = FALSE;
```

使用 `M` 仓库，查询 `01b5ffc3-080a-e214-0000-289d77d57b3e` 花费了 1m45s，所以我们将这些统计数据添加到 Google 表格模板中：

仓库大小 | 积分/小时 | 运行时间分钟部分 | 运行时间秒部分 | 运行时间（小时） | 成本
---|---|---|---|---|---
X-small | 1 | 7 | 14 | 0.12 | $0.24
Medium | 4 | 1 | 45 | 0.03 | $0.23
% 增加 |  |  |  | -76% | -3%

上述显示，使用 `M` 仓库，运行时间减少了 73%，而且成本也减少了 3%，这意味着在这种情况下 'M' 仓库优于 XS 仓库。

由于性能增加速度超过成本，我们可以再次增加到 `L` 仓库，看看是否继续这种趋势。

使用 `L` 仓库，查询 `01b5ffdc-080a-e214-0000-289d77d5c756` 在 1m23s 内完成，将这些数据粘贴到电子表格中：

仓库大小 | 积分/小时 | 运行时间分钟部分 | 运行时间秒部分 | 运行时间（小时） | 成本
---|---|---|---|---|---
X-small | 1 | 7 | 14 | 0.12 | $0.24
Medium | 4 | 1 | 45 | 0.03 | $0.23
Large | 8 | 1 | 23 | 0.02 | $0.37 