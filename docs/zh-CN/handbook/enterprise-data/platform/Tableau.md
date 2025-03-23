# Tableau

## GitLab 的 Tableau

快速链接 | 开发者资源 | 通信
---|---|---  
[Tableau Cloud - GitLab](https://10az.online.tableau.com/#/site/gitlab/home) | [GitLab Tableau 开发者指南](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/) | [内部 Slack 频道](https://app.slack.com/client/T02592416/C03RMCEHVCP)  
[Tableau 在线学习门户](https://elearning.tableau.com) | [Tableau 风格指南](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/tableau-style-guide/) | [外部 Slack 频道](https://app.slack.com/client/T02592416/C031QE95QJU)  
[Tableau 客户门户](https://customer-portal.tableau.com/s/) | [开发者技巧和窍门](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/tips-and-tricks-for-developers/) |   
[Tableau 状态页面](https://trust.salesforce.com/) | [Tableau 嵌入到手册](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/embed-demo/) |   

## Tableau 简介

Tableau 是我们的企业级商业智能工具。它是商业智能领域的[领导者](https://www.tableau.com/asset/gartner-magic-quadrant-2024)。我们正在应用 [Tableau Blueprint](https://help.tableau.com/current/blueprint/en-us/bp_overview.htm) 来启动我们的 Tableau 生产环境。Tableau Blueprint 概述了来自数千家 Tableau 客户的最佳实践和流程。我们将根据 GitLab 的 TeamOps 和文化来应用这些流程和最佳实践。

**Tableau 术语和定义**

* **连接：** Tableau 用于与数据源通信的方法。
  * **直接连接：** 当 Tableau 使用内置连接器与数据源（如 Snowflake 或 Google Drive）通信时。
  * **虚拟连接：** 由管理团队设置的数据源通信的精选连接。通常模拟直接连接。
  * **已发布数据源：** 对单个 tableau 的精选连接，是数据建模的结果。存储在 Tableau Cloud 上。
  * **连接文件：** 从系统中的文件获取数据到 Tableau 的方法。包括 Excel 文件、CSV、PDF 等。
  * **连接服务器（云）：** 连接到数据源的方法。包括与任何在线数据源的连接，包括 Tableau Cloud 和 Snowflake。

* **连接凭据：** 用于验证数据源连接的信息。
  * **嵌入式：** 凭据作为连接的一部分保存。
  * **提示用户：** 每次使用连接时必须输入凭据。

* **连接更新频率：** 确定连接与数据源通信的频率。
  * **实时：** 每次需要数据时都会向数据源发送查询。
  * **提取：** 在提示时向数据源发送查询，将结果存储在自定义微型数据库中。
  * **计划提取：** 托管在 Tableau Cloud 上的提取，将以固定频率与数据源通信并更新存储的数据。

* **数据建模：** 将多个数据表组合成单个结果表的方法。
  * **数据仓库：** 组合表的查询存储在数据仓库存储库中，并在数据仓库中实现。
  * **Tableau 数据建模：** 在连接界面中直接在 Tableau 中定义表之间的关系。
  * **Tableau 混合：** 在可视化构建界面中定义数据源之间的关系。
  * **自定义 SQL：** 在连接中使用 SQL 定义表之间的关系。

* **Tableau 对象：** 开发者用来创建可视化的元素。
  * **项目：** Tableau Cloud 中维护的文件夹结构。这是管理内容权限的地方。
  * **数据源：** 连接和数据建模的集合，产生可以发布和作为独立文件的单个结果表。
  * **流程：** 连接和转换步骤的集合，通常会产生一个或多个数据源。流程使用名为 Prep 的 Tableau 应用程序创建，用于执行数据转换。有些人可能会互换使用 Prep 和 Flow 这两个词。在 GitLab，我们更倾向于所有转换都在数据仓库层面通过 DBT 进行。
  * **工作簿：** 创建可视化的基本文件类型。
    * **视图：** 表示图表或其他可视化的元素。
    * **仪表板：** 视图和布局元素的集合。
    * **故事：** 视图和布局元素的集合，其中视图可以设置为特定的筛选器或参数值，并按顺序结构显示。

## 路线图 FY25 Tableau 路线图

在 FY25-Q1 完成 Tableau 迁移后，我们现在专注于改善 Tableau 开发者体验并扩展我们的实施以加强企业报告。

* FY25-Q2 - 建立 Tableau 未来状态的框架，包括职能团队的输入
  * 发布执行层落地页面，引导用户访问关键仪表板
  * 记录促进单一数据源报告的 Tableau 数据源创建方法
  * 记录并实施用户取消配置政策和流程，以便定期释放未使用的许可证
  * 记录缺乏单一数据源的关键 GTM 领域
  * 使用定量和定性措施运行 Tableau 环境评估
    * 数据源（现有数据源数量、自定义 SQL 与基于表的对比、可能表明数据源整合机会的常用表等）
    * 仪表板（现有仪表板数量、使用分布、每个仪表板的平均用户浏览量等）
    * 用户（登录频率等）

* FY25-Q3 - 实现以下目标（具体数字将在 Q2 更新，并将基于 Q2 评估结果）：
  * 记录并实施仪表板/数据源归档政策和流程，以清理环境
  * 记录并实施帮助用户区分认证和未认证仪表板的流程
  * 启动 BI 赋能章程，提供支持 GitLab Tableau 社区的计划和材料
  * 定义、计算和发布可随时查看的 Tableau 健康定量指标，并将其纳入季度数据关键审查
  * 为需要单一数据源的关键领域发布 X 个认证的 Tableau 数据源
  * 支持职能团队重新指向仪表板以利用认证数据源
  * 刷新 Tableau 环境评估

* FY25-Q4 - 实现以下目标（具体数字将在 Q3 更新）：
  * 迭代 BI 赋能章程
  * 在职能分析团队的支持下加速认证数据源创建，发布 X 个额外的认证数据源
  * 重新指向 X 个仪表板以利用认证数据源
  * 归档 X 个未使用的仪表板，并通过将用户浏览量集中在认证仪表板上来增加每个仪表板的平均用户浏览量 Y
  * 刷新 Tableau 环境评估和 Tableau 健康定量指标

## 治理模型

治理是控制、角色和可重复流程的组合，用于建立对数据和分析的信任和信心。项目团队中的 IT 和业务利益相关者共同负责定义数据和内容治理。在成功的自助服务环境中，适当的治理级别为 GitLab 用户创建问责制，并实现（而不是限制）对可信内容的访问。治理是一个连续体，不同类型的数据和内容需要不同类型的治理。这不是一次性的努力，因为技能和期望会不断发展。定期评估治理流程将使我们能够随着新的分析技能和用例的发展而发展和委派更多责任。

我们在 GitLab 使用自我治理模型。在自我治理模型中，IT 和业务用户之间有强有力的协作。认证内容和数据源可用，创作者和探索者定期创建一次性内容。查看者理解认证、一次性和沙箱内容状态之间的区别。验证、推广和认证流程由所有技能水平的用户明确定义和理解。随着组织分析技能的不断提高，现代分析工作流程中角色之间的界限是流动的，因为用户从消费转向创建再到推广具有适当权限级别的内容。

## BIOps

我们的 Tableau 自我治理模型在 [GitLab Tableau 项目](https://gitlab.com/gitlab-data/tableau) 中使用 BIOps 进行管理和执行。BIOps 方法将利用 GitLab 的仓库、维护者和代码审查功能来管理治理模型。Tableau 目前没有 Git 集成，所以我们的 BIOps 不是完全自动化的，有一些限制。README 文件即将发布，将描述 BIOps 工作流程。我们将在 Q1 和 Q2 期间与 GTM 和财务团队一起迭代这种方法，并根据需要进行调整和适应。

### Tableau 项目架构

Tableau Cloud 中的项目架构在 GitLab Tableau 项目中复制和管理。更多详情请参见 [GitLab Tableau 项目](https://gitlab.com/gitlab-data/tableau)。以下是项目文件夹的描述和 Tableau Cloud 中的项目架构示例。

我们的 Tableau 项目中的顶级文件夹及其相应的治理级别包括：

* `Development`：此文件夹中的内容故意不包含治理，以使用户能够快速原型设计。因此，它应该被视为沙箱内容。
* `Production`：Tableau 生产文件夹环境是一个指定区域，用于发布经过验证的高质量内容，供最终用户用于业务关键报告。此文件夹中的内容已由项目负责人审查和批准。
* `Resources`：此文件夹中的内容包括工作簿模板和可在工作簿开发中使用的认证数据源

**项目和子项目文件夹描述**

* **顶级项目文件夹：** **顶级项目提供工作簿的用途。** 有三个顶级项目：Production、Development 和 Resources。这是 Tableau 用户登陆的最高文件夹级别。这些文件夹引导用户要么通过 Production 路径查看认证内容，要么通过 development 路径查看沙箱内容，要么通过 resources 路径访问工作簿模板和认证数据源以用于工作簿开发。

* **二级子项目文件夹：** **二级项目提供工作簿的主要所有者。** 此级别的架构包含每个部门和跨职能业务动作（如 Go To Market Motion）的子项目。每个部门和跨职能业务动作都有自己的子项目。这使我们能够根据特定部门和业务动作需求在子项目级别创建不同类型的安全性。

* **三级子项目文件夹：** **三级项目提供关于谁可以查看工作簿的安全性。** 我们的 SAFE 数据计划应用在此级别的架构上。这使我们能够灵活地在未来按部门应用更多安全控制，包括增强的 SAFE 数据计划控制、行和列级别安全性以及机密信息的安全性。在此级别应用安全性将允许按部门和业务动作进行定制和可扩展的安全计划。

**项目架构**

1. **Resources**
   1. **General**
      1. **Admin Insights**
         1. Admin Insights Starter
      2. **Templates**
         1. Workbook Template
      3. Data Source Name
   2. **SAFE**
      1. Data Source Name
2. **Development** (Sandbox Environment) 
   1. **Customer Success**
      1. **General**
         1. Data Source Name
         2. Workbook Name
      2. **SAFE**
         1. Data Source Name
         2. Workbook Name
      3. Workbook Name
   2. **Data Team**
   3. **Engineering**
   4. **Finance**
   5. **Go To Market**
   6. **Marketing**
   7. **People**
   8. **Product**
   9. **Sales**
   10. **Security**
3. **Production** (Maps to our [Trusted Data Development Process](https://handbook.gitlab.com/handbook/enterprise-data/data-development/#trusted-data-development)
   1. **Customer Success**
      1. **General**
         1. Data Source Name
         2. Workbook Name
      2. **SAFE**
         1. Data Source Name
         2. Workbook Name
   2. **Data Team**
   3. **Engineering**
   4. **Finance**
   5. **Go To Market**
   6. **Marketing**
   7. **People**
   8. **Product**
   9. **Sales**
   10. **Security**

**BIOps 角色和职责**

请参见 [project-permission-structure](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/#project-permission-structure) 部分了解 BIOps 角色的权限详情。

1. **Tableau 管理员/维护者职责：** 这些负责人负责发布在子项目中的内容，这些子项目汇总到顶级项目，并负责维护 GitLab Tableau 项目。此角色不特别包括 Tableau Cloud 站点管理职责，尽管几位顶级项目负责人也是 [Tableau Cloud 站点管理员](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/#tableau-online-admins)。

2. **项目负责人/代码所有者职责：** 项目负责人来自职能部门和团队。这些负责人负责审查和批准其部门文件夹和跨职能子项目文件夹（如 Go To Market 文件夹）中作为代码所有者的内容发布。完整的项目负责人列表可以在[这里](https://10az.online.tableau.com/#/site/gitlab/workbooks/2730535/views)找到。

## Tableau 内容发布

Tableau 工作簿和数据源可以发布到两个文件夹环境：Development 和 Production。以下详细说明了每个文件夹环境的发布流程。

### 发布到开发文件夹

所有 Tableau 内容开发都从开发项目文件夹开始。开发文件夹是一个沙箱环境，Tableau 开发者可以自由实验和迭代内容，并与团队成员共享以进行初始同行审查。Tableau 开发者可以使用[集合](https://help.tableau.com/current/pro/desktop/en-us/collections.htm)来组织他们的沙箱工作，以便于访问和共享。Tableau 创建者在开发文件夹中处理敏感 SAFE/PII/MNPI 数据时应遵循 [SAFE 开发工作流程指南](https://handbook.gitlab.com/handbook/enterprise-data/platform/safe-data/#tableau)。

### 发布到生产环境的要求

生产文件夹是一个独立的环境，Tableau 用户可以在其中找到经过同行审查和测试的仪表板，这些仪表板由各自职能领域的项目负责人审查。生产文件夹中的内容满足以下要求：

1. **文档**
   * **创建问题：** 发布内容需要一个问题，该问题会自动标记以便分类和搜索。
   * **手册中的文档：** 在 GitLab 手册中创建文档，并在 Tableau 内容描述中链接，并在仪表板上列出

2. **验证审批**
   * **Tableau 项目负责人（业务部门所有者）审批：** Tableau 项目负责人必须批准推广。
   * **技术所有者（数据管理员）签字：** 项目负责人可以请求技术所有者对数据和内容的有效性进行签字。
   * **跨部门开发：** 跨部门内容需要多个业务所有者审查。跨部门内容包括 GTM 等。

3. **数据安全**
   * **数据安全：** 对于 SAFE 或受限数据，必须应用适当的文件夹和/或数据源访问权限控制。对于一般访问数据，需要确认未使用受限（SAFE）数据。

4. **唯一性**
   * **内容唯一性：** 内容是生产环境独有的

5. **工作簿格式要求**
   * **工作簿格式：** 工作簿必须包含 GitLab 标志。
   * **内容描述：** 工作簿和数据源应该有 1-2 个简洁的描述，说明内容的用途。

### 发布到生产环境的程序

![Tableau Publication to Production](../../images/handbook/enterprise-data/platform/publication_to_production.png)

#### 首次推广到生产环境

1. **开发者发布到开发环境：** 开发者将内容发布到 Tableau 开发文件夹。这是准备审查和最终推广的初始步骤。

2. **开发者创建问题：** 开发者创建一个 [GitLab 问题](https://gitlab.com/gitlab-data/tableau/-/issues/new)，该问题将记录推广到生产环境的过程。使用 `Tableau 发布工作簿或数据源到生产环境` 模板，该模板列出了所有必要的请求文档和要求。

3. **开发者确认内容有效性：** 开发者确保内容满足问题中记录的推广标准要求。然后开发者将问题分配给相关的[部门项目负责人](https://10az.online.tableau.com/#/site/gitlab/workbooks/2730535/views)进行审批，表明内容已准备好审查。

4. **审查流程：** 项目负责人将审查问题和内容。他们将检查是否符合生产环境要求并评估内容的准备情况。如果需要，审批人将提出内容更正或更新建议。开发者需要在继续之前解决这些问题。

5. **最终推广：** 一旦满足所有要求并获得批准，项目负责人将内容从开发环境移动到生产环境。此步骤正式使内容可用于业务使用。

#### 编辑和更新生产环境中的内容

有两种选项可以编辑或更新生产环境中的内容：

1. **更新并覆盖原始内容：** 这适用于工作簿或数据源的任何重大更改。更改包括替换或编辑数据源、更改或添加逻辑、自定义 sql 或计算字段。这是首选选项，开发者编辑工作簿或数据源并保存到开发文件夹。然后进行审查和检查。获得批准后，项目负责人将覆盖到生产环境。

2. **允许开发者在生产环境中编辑：** 允许我 48 小时编辑/更新访问权限以在生产环境中修改内容。这仅适用于小更改，如外观改进、拼写更正、小筛选器更改或紧急问题。

### Tableau 风格指南

有关设计最佳实践和资源的更多指导，请参阅我们的 [Tableau 风格指南](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/tableau-style-guide/) 手册页面。

### Tableau 发布服务级别目标 (SLOs)

**生产环境发布 SLO**

项目负责人负责其各自的部门文件夹。他们为推广内容到生产环境的请求提供审查和审批。

**开发环境发布 SLO**

个别 Tableau 开发者可以按需将开发内容发布到其部门的开发子项目。

## 部署

Tableau Cloud 利用 GitLab 的现有技术投资并集成到我们的 IT 基础设施中，为用户提供自助服务、现代分析平台。

### Tableau 未使用内容归档政策和流程

为了维护高效、整洁和用户友好的 Tableau 环境，已实施自动化归档流程。本政策概述了在我们的 Tableau GitLab Cloud 环境中归档未使用和不活跃内容的程序。Tableau GitLab Public 和 Sandbox 不受此政策约束。

归档范围：

90 天以上未使用的工作簿和数据源将被归档，并通过搜索或直接链接无法访问。归档的项目可以根据请求从 BI 团队检索。归档流程是自动化的，每月 15 日通过将内容移动到 `Admin Archive` 文件夹进行。

归档排除：

1. 发布到 Tableau GitLab Public 的工作簿和依赖数据源。
2. 所有者已请求保留的项目，由 Tableau 标签 `Do NOT Archive` 指示。
3. 存储在个人文件夹中的内容不会被归档，因为它仅对所有者可见且不会使环境混乱。

归档联系人：有关归档内容的问题或请求，请联系 BI 团队。点击[这里](.../handbook/enterprise-data/platform/tableau/tableau-admin-guide/#stale-and-unsued-content-management)查看管理归档文档。

### 部署流程

1. **初始设置**
   * 在 Tableau Cloud 中创建项目结构
   * 设置权限和访问控制
   * 配置数据源连接

2. **内容迁移**
   * 将现有仪表板迁移到新环境
   * 验证数据连接和更新
   * 测试所有功能

3. **用户培训**
   * 提供用户培训材料
   * 举办培训会议
   * 建立支持渠道

4. **监控和维护**
   * 定期检查系统性能
   * 更新安全设置
   * 管理用户访问权限

### 最佳实践

1. **数据管理**
   * 使用单一数据源
   * 定期更新数据
   * 维护数据质量

2. **仪表板设计**
   * 遵循风格指南
   * 确保响应式设计
   * 优化性能

3. **用户管理**
   * 定期审查用户权限
   * 及时移除未使用的访问权限
   * 保持用户文档更新

4. **安全措施**
   * 实施数据加密
   * 定期安全审计
   * 遵守数据保护法规

### 支持

如果您需要帮助或有任何问题，请：

1. 查看 [Tableau 开发者指南](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/)
2. 联系您的部门 Tableau 管理员
3. 在 Slack 频道中寻求帮助
4. 提交支持请求 