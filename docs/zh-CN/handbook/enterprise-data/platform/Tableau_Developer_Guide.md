# Tableau 开发者指南

GitLab 的 Tableau 开发者指南

## 快速链接

  * [技巧与窍门](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/tips-and-tricks-for-developers/)
  * [Tableau 样式指南](handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/tableau-style-guide/)

## Tableau 中的数据源类型

在 Tableau 中，您可以使用几种不同类型的数据源，选择哪种数据源可能会影响仪表板的性能和最终用户体验。让我们先定义一些术语：

  * **提取 vs. 实时**：提取的数据源在 Tableau 中有一个数据集的提取。实时数据源每次更改过滤器或导航到新的仪表板选项卡时都会查询底层数据源（如 Snowflake、Google Sheets）。提取几乎总是表现得更快。

  * **本地、嵌入和发布**：在本指南中，“本地”和“嵌入”数据源是相同的。这些连接的数据源“位于”工作簿中或“与”工作簿一起存在。查看或编辑此数据源的唯一方法是打开工作簿。这种连接类型一次只能连接/存在于一个工作簿中。

  * **发布**：发布的数据源与工作簿分开发布。因此，在 Tableau Cloud 中，您可以导航到数据源的链接，以及工作簿的链接。您可以将一个发布的数据源连接到任意多个工作簿，因为它独立于工作簿存在。

工作簿的数据源可以是本地 + 实时、本地 + 提取、发布 + 实时或发布 + 提取。

### 关于连接类型的提示

您可能会发现，在 Tableau Desktop 中使用发布的数据源开发工作簿可能会很慢且笨拙。无论出于何种原因，发布的数据源连接可能会运行缓慢。为了解决这个问题，同时仍然使用发布的数据源，您可以在本地副本上工作。

[此视频](https://www.youtube.com/watch?v=KcxtXmzS4mk)描述了该过程。这是一个旧视频，因此用户界面有点过时，但创建本地副本的过程是相同的。

书面说明如下：在 Desktop 中打开工作簿并导航到任何工作表。然后右键单击数据源并选择“创建本地副本”。接下来，右键单击原始发布的数据源，并从下拉菜单中选择“替换数据源”。在弹出窗口中，将原始数据源（发布）替换为新数据源（本地副本）。

然后您可以像平常一样进行开发。完成后，您可以将数据源发布回 Tableau Cloud，它将把本地副本转换回发布的数据源连接。最后，发布工作簿。

请注意，不要覆盖其他人现有的数据源，以免更改可能破坏其工作簿的运行。

#### 在发布的数据源中编辑字段

如果您在连接到发布数据源的工作簿（在 Tableau Cloud 或 Desktop 中）中进行开发，则无法对发布的数据源进行任何更改。这意味着：

  1. 如果您想对计算字段进行任何编辑，您将无法做到。您必须创建计算字段的副本。
  2. 如果您使用“[替换引用](https://www.thedataschool.co.uk/gregg-rimmer/tableaus-replace-references-feature/)”功能，它只会替换字段在工作表上独立出现的实例。它不会替换包含在另一个计算字段中的该字段的任何实例（参见第 1 点，您无法在发布的数据源中编辑计算字段）。
  3. 如果您更改工作簿中的任何参数，Tableau 将创建您的参数的重复副本，并在发布版本中用副本替换您的参数。如果利益相关者来找您并说“这个仪表板坏了！下拉菜单不起作用！”，很可能存在两个版本的“坏”参数。
  4. 您无法在预先存在的计算字段上添加表格计算。您必须创建计算字段的副本，然后才能使用表格计算与副本。

如果您发现自己需要执行上述任何操作，这是可能的。有两种选择 - 您可以按照上述部分中的说明创建数据源的本地副本，进行更改，然后重新发布数据源。

或者，您可以导航到 Tableau Cloud 中的发布数据源，以“编辑”模式打开它，进行更改，然后重新发布数据源。

## 数据源方法

通常，我们建议在 Tableau 中创建数据源的方法是在 dbt/Snowflake 中创建所有连接，以物化最终的市场和/或报告表，Tableau 可以直接使用这些表来构建仪表板，而无需在 BI 层中进行进一步的连接、关系或计算。

在 Tableau 实施期间，我们尝试了将事实表和维度表引入 Tableau 并在其中创建连接和关系的方法。然而，我们更喜欢在可能的情况下在 dbt/Snowflake 中创建数据结构，原因如下：

  * 通过将业务逻辑保留在企业数据仓库中作为规则，并简单地发布最终的市场/报告表以供使用，我们避免了在 Tableau 数据源中应用相互矛盾的业务逻辑。
  * 这种方法通过 dbt/git 集成将所有连接和报告逻辑保留在版本控制中。
  * 这种方法使最终的数据源可以使用 SQL 进行查询；这使得分析师更容易将仪表板中的结果与最终数据集与上游表进行比较，并使分析师更容易在仪表板显示意外结果时排查逻辑问题。
  * 这使得相同的数据集可以轻松地用于 Tableau 仪表板以及临时查询、一次性导出/分析，或在需要时拉入另一个下游工具（例如 Jupyter 笔记本）。

出于同样的原因，我们创建计算字段的方法是在可能的情况下在 dbt/Snowflake 中创建它们，而不是在 Tableau 中创建。一个值得注意的例外是比率指标（例如，毛利润百分比将在 Tableau 中计算，以便在应用过滤器时动态加权；但是，分子和分母都应在 dbt/Snowflake 中定义，仅在 Tableau 中进行简单的除法）。

这种方法旨在满足大多数数据源用例，鼓励 Tableau 开发人员首先尝试这种方法，而不是在 Tableau 中创建连接和关系。如果您发现此方法不支持的实例，请提交 MR 以更新此手册指南，以分享替代方法更好的场景。

## 工作簿中的连接类型

当您发布工作簿或数据源时，有几个身份验证选项。默认选项将允许您发布您的工作，但您很快就会收到：

  1. 用户的消息，称 OAuth 令牌已过期，他们无法访问工作簿。
  2. 如果您安排了提取，您将收到提取失败的电子邮件。

确保用户始终可以访问工作簿中的数据的方法是选择非默认的身份验证选项。

**在 Desktop 中**

**从 Desktop 发布数据源**

如果您从 Desktop 发布数据源到 Cloud/Online 以成为 Tableau 发布的数据源，您将看到以下窗口：

![数据窗口](https://handbook.gitlab.com/images/data-window.png)

选择“编辑”按钮，然后选择“身份验证”。它将带您到以下弹出窗口。选择要嵌入的。

![身份验证](../../images/handbook/enterprise-data/platform/authentication.png)

**发布具有本地连接的工作簿**

具有本地连接的工作簿是其数据源位于工作簿内部的工作簿，而不是您可以搜索 Tableau Online 的单独发布的 Tableau 数据源。当您尝试发布具有本地连接的工作簿时，您将看到以下窗口：

![本地窗口](../../images/handbook/enterprise-data/platform/window-local.png)

选择“编辑”，然后选择“数据源”并找到“身份验证”。选择嵌入您的。

![本地身份验证](../../images/handbook/enterprise-data/platform/auth-local.png)

**在 Cloud/Online 中**

**在 Cloud/Online 中发布**

如果您在 Cloud/Tableau Online/您的网络浏览器（都是同一件事）中编辑数据源，为了确保您的凭据已嵌入，请找到“发布为”：

![发布为](../../images/handbook/enterprise-data/platform/publish-as.png)

在以下窗口中，请确保勾选“嵌入凭据”框。

![嵌入凭据](../../images/handbook/enterprise-data/platform/cloud-embed.png)

### 嵌入您的角色名称以避免已发布仪表板中的错误的工作流程

这是确保您的角色名称正确嵌入到已发布仪表板中的过程。这有两个关键步骤，按此顺序执行可以帮助避免以下两个错误：

  1. 用户尝试访问您发布的仪表板，但遇到了要求他们登录 Snowflake 的错误窗口。
  2. 另一位分析师尝试快速检查您的数据源在 Cloud 中的构建方式或自定义 SQL 的构造方式。

您第一次获得嵌入角色名称的选项是在您首次形成与数据源的连接时。它看起来像这样：

![连接](../../images/handbook/enterprise-data/platform/initial_connection_rolename.png)

如果您希望其他人能够访问您的数据源，您需要将其留空。在此步骤中没有理由输入您的角色名称，您将在稍后的步骤中执行此操作，因此正确的工作流程是在此步骤中将其留空。

从这里开始，设置您的数据源并按照您的意愿进行开发。然后，当您准备好时，发布您的工作簿/数据源。这是您将按照[本节开头](https://handbook.gitlab.com/tableau-developer-guide/#connection-types-in-workbooks)的步骤嵌入您的角色名称的地方。

如果您在此步骤中忘记嵌入您的角色名称，那么您的用户将被要求登录 Snowflake 或发送错误消息，而不是让他们访问仪表板。

### 创建允许没有 Snowflake 访问权限的其他人编辑工作簿的连接类型

在您的工作簿中使用发布连接或本地提取连接将使没有 Snowflake 访问权限的其他人能够编辑您的工作簿。如果工作簿是使用本地实时连接发布的，那么任何想要对您的工作簿进行编辑的 Explorer 都需要使用自己的凭据登录 Snowflake。这是尝试编辑具有本地实时连接的工作簿时，编辑者将遇到的屏幕。

在您希望没有 Snowflake 访问权限的 Explorer 能够对您的工作簿进行小编辑的特定用例中，请确保仅使用发布的实时连接或提取数据。

![登录屏幕](../../images/handbook/enterprise-data/platform/singin.png)

## 常见连接错误及其解决方法

您或您的用户之一在尝试访问 Tableau 时是否遇到错误屏幕？查看问题是否在此列表中，以及如何解决。

### 1\. 问题：身份验证

**错误**：

> `“确认您已为此数据源提供了有效的凭据。Tableau 检测到您的 OAuth 刷新令牌已过期。使用新凭据重新进行身份验证。如果您需要帮助，请询问您的 Tableau 管理员”和“此工作表使用位于 Snowflake 数据库上的数据。您需要登录到该服务器”。`

此错误消息可能难以诊断，因为它可能是由多种原因引起的。不幸的是，当此消息出现时，没有简单的方法来诊断哪个可能的原因是您看到此消息的原因。

原因 | 解决方案/预防  
---|---  
开发人员使用了本地实时连接 | [按照这些步骤操作。](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/#creating-connection-types-that-allow-others-without-snowflake-access-to-edit-the-workbook)  
最后发布工作簿/数据源更改的人忘记在发布时嵌入其凭据。 | [在发布时按照这些步骤操作。](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/#workflow-for-embedding-your-rolename-to-avoid-errors-in-published-dashboards)  
凭据确实已过期（已发布数周） | 让数据源所有者按照这些[步骤](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/#snowflake-oauth-data-source-connection-expiration-period)刷新其凭据。

### 2\. 问题：数据访问不足

**错误**：

> `尝试登录查看仪表板时，您收到错误消息“无效的同意请求”。`

![无效的同意嵌入](../../images/handbook/enterprise-data/platform/invalidconsent.png)

这通常是因为您没有访问您尝试查看的内容的权限。这可能是：

  * 视图构建的数据库或表。
  * 开发人员嵌入到工作簿中的凭据。[请参阅此处。](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/tableau-developer-guide/#workflow-for-embedding-your-rolename-to-avoid-errors-in-published-dashboards)

**解决方案：** 如果最后发布数据源/工作簿的人按照上述步骤正确嵌入了其凭据，那么这可能是访问问题。最简单的解决方案是让开发人员将连接发布为发布和提取的数据源。

如果您需要访问权限并且使用提取连接不合适，您可以检查开发人员是否使用了您没有访问权限的“大型”仓库，或者工作簿中是否使用了具有受限访问权限的非标准表。

### 3\. 问题：数据中缺少列

**错误**：

> `“发生了意外错误。如果您继续收到此错误，请联系您的 Tableau 服务器管理员”以及“TableauException: 错误：数据源 'sqlproyx._______' 中的字段 '[name]' 在您的数据库中不存在。它已被修改或删除。您是否要重置视图？”。`

这表明连接正在查找不存在的/损坏的列。它可能在 Snowflake 中被删除或修改，现在这些更改导致 Tableau 中的中断。

**解决方案：** 联系工作簿的所有者以获取帮助。解决此类错误的最简单方法是下载数据源或工作簿的本地副本到 Tableau Desktop，并在那里删除或替换字段。

## 嵌入手册

为了使工作簿中的视图能够嵌入并可在手册中查看（无论是公开还是内部），工作簿及其数据源必须以特定方式准备。要嵌入到公开手册中，工作簿和相关数据源必须从[内部 GitLab Tableau](https://10az.online.tableau.com/#/site/gitlab)站点复制到[公开 GitLab Tableau](https://us-west-2b.online.tableau.com/#/site/gitlabpublic)站点。为了促进嵌入视图的正确查看和内容同步到公开站点，工作簿必须以特定方式设置并赋予特定标签。嵌入到内部站点的视图不需要在特定项目中，但仍应满足设置指南。

有关如何嵌入 Tableau 图表的说明可以在[手册嵌入演示](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/embed-demo/)页面上找到。

### 工作簿设置

对于嵌入到手册中，视图将比仪表板更好地嵌入，因此每个要嵌入的视图都应设计为在没有用户选择输入的情况下运行。过滤器和参数可以在嵌入过程中预设，但查看者无法更改。此外，视图必须满足以下条件：

  * 视图不能隐藏
  * 对于嵌入到公开手册中，每个数据源必须使用数据团队服务帐户的用户名和密码连接到 Snowflake 或使用提取
  * 对于嵌入到公开手册中，每个工作簿必须具有 `Public` 标签

#### 数据源

如果您不使用提取（例如，当您的提取将超过 1000 万行时），您将需要使用数据团队服务帐户的凭据。请联系数据团队以获取这些凭据。

在发布内部或外部视图时，请注意在数据源中嵌入凭据。使用提取并嵌入您的角色将是确保用户始终可以查看数据并且不会遇到授权过期错误的最清晰方式。

确保如果您使用数据团队的凭据发布工作簿，当您对工作簿进行任何更改时，它保留这些凭据。您需要在数据源中嵌入密码以使视图正确显示。此框在您进行更改时可能会未勾选。![需要勾选的框](../../images/handbook/enterprise-data/platform/box-checking.png)

#### 公开标签

如果您的视图是公开的并嵌入到公开手册中（即，人们不需要登录即可查看它），那么它需要位于公开 GitLab Tableau Cloud 站点上，因为查看者许可协议。要为工作簿标记为公开，请单击工作簿。在工作簿的主页上，您可以看到每个视图，在名称旁边有一个“更多设置”选项“...”。选择它，并找到“标签...”。在这里，您可以添加“Public”作为标签。

大约需要一天时间，URL 才会显示在[此列表](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/embed-demo/#views-availble-for-public-embedding)中。一旦显示，复制该 URL 并在嵌入信息中使用它。如果您的视图在一天左右后仍未显示，很可能是因为您的数据源之一未遵循 A) 提取连接或 B) 使用数据团队服务帐户的凭据的指南。

### 工作簿同步

每个具有要嵌入到公开手册中的视图的工作簿必须标记为 `Public` 标签。这将确保工作簿及其数据源被复制到公开 GitLab Tableau 站点。只有可以访问工作簿的创建者和 Explorer 才能标记工作簿，请参阅 Tableau [文档](https://help.tableau.com/current/pro/desktop/en-us/tags.htm#add-tags)以获取更多信息。个人标记必须明确数据是否应公开共享，如果有任何疑问，请与 BI 团队合作检查并应用标签。从工作簿中删除此标签将从公开 GitLab Tableau 站点中删除工作簿，这将导致尝试从该工作簿加载视图的手册页面显示错误。需要注意的是，目前同步的工作簿可能需要长达 48 小时才能显示在[可嵌入视图列表](https://handbook.gitlab.com/handbook/enterprise-data/platform/tableau/embed-demo/#views-availble-for-public-embedding)中。

### 工作簿命名约定

首次将工作簿发布到我们的 Tableau Cloud 站点时，请使用其预期/官方标题命名工作簿，以便生成的 URL 仅捕获此标题（这将允许我们在工作簿发布到生产空间时保持相同的 URL）：

![命名 Tableau 工作簿](../../images/handbook/enterprise-data/platform/naming_tableau_workbook.png)

![工作簿 URL](../../images/handbook/enterprise-data/platform/workbook_url.png)

发布到[开发](https://10az.online.tableau.com/#/site/gitlab/projects/300844)项目：

所有发布到开发项目的工作簿都将附加 _Draft_ 及其部门标签，以指示它们处于开发模式，而不是经过同行评审并旨在作为用例的单一事实来源（SSOT）的工作簿。BI 团队将利用 Tableau Cloud 中可用的标签功能，按部门和发布状态更好地组织工作簿。例如，下面的工作簿被分配了 _Draft_ 和 _Data Team_ 标签：

![标签](../../images/handbook/enterprise-data/platform/tags.png)

要为工作簿添加标签，请选择该工作簿右侧的省略号符号，然后单击 _Tag…_：

![添加标签](../../images/handbook/enterprise-data/platform/to_tag.png)

进入标签窗口后，添加 _Draft_ 和部门标签：

![添加标签](../../images/handbook/enterprise-data/platform/add_tags.png)

## 发布到 Tableau Cloud

有两个发布环境：开发和生产。

  * **开发** 用于测试和迭代仪表板和数据源。此环境允许在内容最终确定之前进行实验和优化。
  * **生产