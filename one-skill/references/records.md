# 最小生产记录

每个内容项目只保留一套当前稿件和记录，必要时用版本历史保留旧稿。下列是信息分类，可复用已有文件或一份记录，不是必须新建四个文件。用户仅要求局部改句时可在对话说明，不强制文件体系。

- brief.md：原始输入、来源、受众、请求范围、锁定原话与事实缺口。
- draft.md：完整正文；多渠道用清楚的平台文件名，记录共同来源和父稿。
- review.md：独立审查的实际结论，缺 reviewer 也如实记录。
- status.md：实际状态、模型、资产路径、同步与投递回执、未完成项。

审查记录字段：scope、source_files、actual_artifacts、reviewer、checks、blockers、majors、rewrite_plan、decision、unverified。checks 逐项记 pass / fail / not_applicable / unverified。accept 仅代表审查范围通过，不代表用户定稿、激活或公开。

投递记录字段：platform、target_account_or_recipient、version、requested_action、authorization_evidence、receipt、public_url、readback、status、remaining。无真实值留空，不生成假 ID。

复盘记录字段：window、source、metrics、goal、valid_leads、first_bottleneck、next_single_experiment、rule_candidate_status。未知指标标 unavailable。
