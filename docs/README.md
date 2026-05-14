# GEO-SEO Claude Code Skill — 文件

`geo-seo-claude` 是一組 Claude Code 技能套件，可對網站執行 GEO（Generative Engine Optimization）與 SEO 稽核。它協調 13 個 sub-skill、5 個平行 subagent，以及一組 Python 工具程式，產生綜合 GEO Score（0–100）與依優先順序排列的行動計畫。

如果你是第一次使用，請從 **Getting Started** 開始。如果你要貢獻，請先快速閱讀 **Architecture** 與 **Skills & Agents**。

## 目錄

| 文件 | 內容 |
|-----|--------------|
| [Getting Started](getting-started.md) | 需求、安裝（macOS/Linux/Windows）、第一次稽核、疑難排解、解除安裝。 |
| [Commands Reference](commands-reference.md) | 每個 `/geo` slash command 的用法、參數、輸出，以及何時使用。 |
| [Architecture](architecture.md) | Repo 結構、稽核流程、平行 subagent dispatch、資料儲存。 |
| [Skills & Agents](skills-and-agents.md) | 每個 sub-skill、subagent、Python script 與 schema template 的參考資料。 |
| [Scoring Methodology](scoring-methodology.md) | 綜合 GEO Score 的計算方式、各類別訊號與注意事項。 |
| [FAQ](faq.md) | 使用者與貢獻者常見問題。 |
| [Contributing](../CONTRIBUTING.md) | 如何回報 bug、提議功能與開 PR。 |

## 快速連結

- 第一次稽核：[Getting Started → Your First Audit](getting-started.md#your-first-audit)
- 完整指令列表：[Commands Reference](commands-reference.md)
- 權重表：[Scoring Methodology](scoring-methodology.md)
- 平行稽核流程：[Architecture → Full Audit Flow](architecture.md)
