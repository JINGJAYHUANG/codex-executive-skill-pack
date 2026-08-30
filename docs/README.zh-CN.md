# Codex Executive Skill Pack 中文说明

这是一个由 20 个独立技能合同组成的公开技能包，覆盖公开信息研究、变化监控、竞争与机会分析、API 和数据管道设计、工作流编译、自动化故障恢复、决策备忘录、实验设计、知识图谱、会议执行和个人运营协调。

## 核心原则

```text
先判断是否真的需要技能
→ 选择最小充分技能
→ 高影响能力只做显式调用建议
→ 工具权限与用户确认另行检查
→ 用可验证输出结束任务
```

本仓库不把 20 个技能合并成一个超长总提示词。每个技能均有：

- 明确触发条件；
- 明确不应触发的边界；
- 权限类别说明；
- 分步工作流；
- 输出合同；
- 上下游路由；
- 正例与反例；
- 证据支持的成熟度标签。

## 九个显式优先技能

以下能力风险较高，普通自然语言只能得到“建议显式调用”，不能直接视为授权：

```text
screen-macro-recorder
desktop-pilot
api-bridge-builder
data-pipeline-fabricator
fileops-guardian
workflow-compiler
mission-control
automation-self-healer
inbox-negotiator
```

推荐显式格式：

```text
$fileops-guardian: 先预览文件重命名计划，不要执行
```

显式调用仍不代表可以绕过操作系统、连接器或平台的权限，也不代表可以自动发送邮件、删除文件、同意价格或作出商业承诺。

## 验证范围

`v0.1.0` 验证的是：

- 20 个技能的结构一致性；
- 9 个显式优先门禁；
- `SKILL.md` 与 `openai.yaml` 的确定性生成；
- 74 条路由与边界用例；
- Python 3.11–3.13；
- 隐私与常见密钥扫描；
- CLI、安装预览与重复构建。

当前没有声称真实桌面、邮箱、API、文件系统和第三方连接已经完成实地集成验证。

## 使用

```bash
python -m pip install --no-deps -e .
cesp validate
cesp list
cesp route "把这些方案做成决策备忘录"
cesp eval
```

安装默认只预览：

```bash
cesp install --target ./local-plugins
```

确认后再复制：

```bash
cesp install --target ./local-plugins --apply
```

## 公共边界

仓库不包含个人画像、聊天记录、私人项目状态、账户配置、Token、Webhook、本机用户路径或真实客户材料。历史本地技能只用于恢复名称和设计经验，公开版本重新编写为通用、可测试、可审计的合同。
