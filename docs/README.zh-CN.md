# Codex Executive Skill Pack 中文说明

这是一个可公开安装和审计的 **20 技能 Agent 工作流包**，覆盖研究、工程执行、决策学习和跨任务协调。

当前版本：

```text
v0.1.0
maturity: instruction-audited
runtime_status: host-dependent
```

这两个标签的含义是：仓库内的指令、元数据、路由案例、权限边界、安装器和打包流程已经通过自动检查；但不能据此声称每个技能已经在所有 ChatGPT、Codex、操作系统、连接器和账户环境中完成生产验证。

## 核心原则

1. **直接完成优先。** 简单任务不需要为了展示 Agent 能力而调用技能。
2. **最小技能集。** 复杂任务也只选择真正必要的技能。
3. **权限不继承。** 一个技能交给另一个技能时，后者必须重新检查范围和审批。
4. **外部写入单独批准。** 发送、发布、提交、改日历、改账户和不可逆操作不能从宽泛目标中推断。
5. **证据与推断分离。** 旧记录、用户陈述、当前核验和模型推断不能混为一谈。
6. **不伪造执行。** 缺少工具、权限或连接器时，只能说明限制，不能声称已经完成。

## 四层结构

| 层级 | 主要工作 | 数量 |
|---|---|---:|
| Intelligence | 公开资料采集、变化监控、竞争与机会研究 | 4 |
| Engineering & Execution | API、数据管道、文件、桌面、工作流和故障恢复 | 6 |
| Decision & Learning | 决策备忘录、实验、知识图谱、技能构建和经验复盘 | 5 |
| Orchestration & Operations | 复杂任务编排、会议、谈判和有限范围运营协调 | 5 |

## 20 个技能

| # | Skill | Layer | Activation | Risk |
|---:|---|---|---|---|
| 01 | [`web-intel-harvester`](../skills/web-intel-harvester/SKILL.md) | intelligence | contextual | low |
| 02 | [`change-sentinel`](../skills/change-sentinel/SKILL.md) | intelligence | contextual | low |
| 03 | [`competitor-radar`](../skills/competitor-radar/SKILL.md) | intelligence | contextual | medium |
| 04 | [`opportunity-radar`](../skills/opportunity-radar/SKILL.md) | intelligence | contextual | medium |
| 05 | [`screen-macro-recorder`](../skills/screen-macro-recorder/SKILL.md) | engineering-execution | explicit-only | high |
| 06 | [`desktop-pilot`](../skills/desktop-pilot/SKILL.md) | engineering-execution | explicit-only | high |
| 07 | [`api-bridge-builder`](../skills/api-bridge-builder/SKILL.md) | engineering-execution | explicit-only | high |
| 08 | [`data-pipeline-fabricator`](../skills/data-pipeline-fabricator/SKILL.md) | engineering-execution | contextual | medium |
| 09 | [`fileops-guardian`](../skills/fileops-guardian/SKILL.md) | engineering-execution | explicit-only | high |
| 10 | [`workflow-compiler`](../skills/workflow-compiler/SKILL.md) | engineering-execution | explicit-only | high |
| 11 | [`mission-control`](../skills/mission-control/SKILL.md) | orchestration-operations | explicit-only | high |
| 12 | [`automation-self-healer`](../skills/automation-self-healer/SKILL.md) | orchestration-operations | explicit-only | high |
| 13 | [`decision-memo-engine`](../skills/decision-memo-engine/SKILL.md) | decision-learning | contextual | medium |
| 14 | [`experiment-autopilot`](../skills/experiment-autopilot/SKILL.md) | decision-learning | contextual | medium |
| 15 | [`knowledge-graph-builder`](../skills/knowledge-graph-builder/SKILL.md) | decision-learning | contextual | medium |
| 16 | [`skillsmith`](../skills/skillsmith/SKILL.md) | decision-learning | contextual | medium |
| 17 | [`experience-replay`](../skills/experience-replay/SKILL.md) | decision-learning | contextual | medium |
| 18 | [`meeting-to-execution`](../skills/meeting-to-execution/SKILL.md) | orchestration-operations | contextual | medium |
| 19 | [`inbox-negotiator`](../skills/inbox-negotiator/SKILL.md) | orchestration-operations | explicit-only | high |
| 20 | [`personal-coo`](../skills/personal-coo/SKILL.md) | orchestration-operations | explicit-only | high |

## 为什么有 9 个 explicit-only 技能

下列技能在 `agents/openai.yaml` 中明确设置：

```yaml
policy:
  allow_implicit_invocation: false
```

```text
screen-macro-recorder
desktop-pilot
api-bridge-builder
fileops-guardian
workflow-compiler
mission-control
automation-self-healer
inbox-negotiator
personal-coo
```

原因是它们涉及桌面控制、账户资料、网络或文件写入、故障修复、跨技能权限继承，或者抽象层级很高。仅凭“帮我处理一下”不能自动扩大到这些能力。

## 安装

### 作为插件源

```bash
codex plugin marketplace add JINGJAYHUANG/codex-executive-skill-pack
```

随后在支持的 Plugins Directory 或 `/plugins` 中安装，并在未立即出现时重启宿主。

### 安装到当前仓库

```bash
python -m pip install --no-deps -e .
cesp install --layout repo-skills --target .
cesp install --layout repo-skills --target . --apply
```

第一次命令只预览，第二次才写入：

```text
$REPO_ROOT/.agents/skills/
```

已有不同文件默认视为冲突，不会静默覆盖。

## 验证

```bash
cesp validate --root . --strict
cesp eval --root .
python scripts/run_release_gate.py
```

路由评估共 74 条，但这是一个确定性的参考测试器，不等于所有模型宿主都会逐字采用相同路由。

## 公开边界

仓库不包含：

- 个人画像和私人记忆；
- 聊天记录、真实收件箱内容和账户数据；
- Token、Cookie、Webhook 或认证文件；
- 本机用户名和真实磁盘路径；
- 私有交易策略、候选结果或业绩；
- 实际 MCP、桌面控制驱动或后台服务；
- 对任何生产环境可靠性的虚假声明。

详细内容见：

- [架构](architecture.md)
- [路由](routing.md)
- [权限模型](permission-model.md)
- [评估](evaluation.md)
- [安装](installation.md)
- [威胁模型](threat-model.md)
