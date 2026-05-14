---
name: geo-update
description: 從 upstream repository 拉取最新 GEO-SEO 技能更新。比較已安裝檔案與最新版本，顯示變更內容，並就地更新所有技能、代理程式 (agents)、指令碼與 schema 範本。
allowed-tools:
  - Bash
  - Read
  - Write
---

# GEO-SEO 更新技能 (Update Skill)

## 目的

將本機已安裝的 GEO-SEO 技能、代理程式、指令碼與 schema 範本更新到上游儲存庫 (upstream repository) 的最新版本。更新前後都會顯示變更摘要。

---

## 更新工作流程

### Step 1：判斷已安裝位置

GEO-SEO 工具箱會安裝到 `~/.claude/` 底下的這些位置：

| 元件 (Component) | 安裝路徑 |
|-----------|-------------|
| 主技能 (Main skill) | `~/.claude/skills/geo/` |
| 子技能 (Sub-skills) | `~/.claude/skills/geo-*/` |
| 代理程式 (Agents) | `~/.claude/agents/geo-*.md` |
| 指令碼 (Scripts) | `~/.claude/skills/geo/scripts/` |
| Schema 範本 | `~/.claude/skills/geo/schema/` |
| 鉤子 (Hooks) | `~/.claude/skills/geo/hooks/` |

透過檢查 `~/.claude/skills/geo/SKILL.md` 確認安裝存在。若不存在，告知使用者 GEO-SEO 尚未安裝，並建議改執行安裝程式 (installer)。

### Step 2：複製 (Clone) 最新上游版本

```bash
TEMP_DIR=$(mktemp -d)
git clone --depth 1 https://github.com/zubair-trabzada/geo-seo-claude.git "$TEMP_DIR/repo"
```

若 clone 失敗，回報錯誤並停止作業。不要修改任何已安裝檔案。

### Step 3：比較已安裝 vs 最新版本

複製檔案前，先產生差異摘要 (diff summary)，讓使用者知道將變更什麼內容：

1. 對每個元件目錄，使用 `diff --recursive --brief` 比較已安裝檔案與複製的檔案。
2. 將變更分類為：
   - **新檔案 (New files)** — 上游有、本機沒有
   - **已修改檔案 (Modified files)** — 兩邊都有但內容不同
   - **已移除檔案 (Removed files)** — 本機有、上游沒有（這些**不會**自動刪除）
3. 將摘要呈現給使用者。

### Step 4：套用更新

將檔案從複製的儲存庫複製到安裝位置：

```bash
CLAUDE_DIR="${HOME}/.claude"
SOURCE_DIR="$TEMP_DIR/repo"

# 主技能
cp -r "$SOURCE_DIR/geo/"* "$CLAUDE_DIR/skills/geo/"

# 子技能 (Sub-skills)
for skill_dir in "$SOURCE_DIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$CLAUDE_DIR/skills/${skill_name}"
    cp -r "$skill_dir"* "$CLAUDE_DIR/skills/${skill_name}/"
done

# 代理程式 (Agents)
for agent_file in "$SOURCE_DIR/agents/"*.md; do
    cp "$agent_file" "$CLAUDE_DIR/agents/"
done

# 指令碼 (Scripts)
if [ -d "$SOURCE_DIR/scripts" ]; then
    cp -r "$SOURCE_DIR/scripts/"* "$CLAUDE_DIR/skills/geo/scripts/"
    chmod +x "$CLAUDE_DIR/skills/geo/scripts/"*.py 2>/dev/null || true
fi

# Schema 範本
if [ -d "$SOURCE_DIR/schema" ]; then
    cp -r "$SOURCE_DIR/schema/"* "$CLAUDE_DIR/skills/geo/schema/"
fi

# 鉤子 (Hooks)
if [ -d "$SOURCE_DIR/hooks" ] && [ "$(ls -A "$SOURCE_DIR/hooks" 2>/dev/null)" ]; then
    mkdir -p "$CLAUDE_DIR/skills/geo/hooks"
    cp -r "$SOURCE_DIR/hooks/"* "$CLAUDE_DIR/skills/geo/hooks/"
    chmod +x "$CLAUDE_DIR/skills/geo/hooks/"* 2>/dev/null || true
fi
```

### Step 5：更新 Python 相依套件

若上游儲存庫中存在 `requirements.txt` 且與已安裝版本不同：

```bash
python3 -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet
```

回報任何失敗項目，但不要視為致命錯誤。

### Step 6：清理

```bash
rm -rf "$TEMP_DIR"
```

### Step 7：回報結果

呈現摘要：

```
GEO-SEO 更新完成
=======================
新增檔案：      [數量]
已修改檔案：    [數量]
未變更：        [數量]
上游已移除（本機保留）：[數量]

相依套件：[已更新 / 未變更 / 失敗]
```

若上游有已移除檔案，列出它們並建議使用者檢視是否要手動刪除。

---

## 重要備註

- **永遠不要刪除**已安裝但上游不再存在的本機檔案。使用者可能已進行客製化。列出這些檔案，讓使用者自行決定。
- **永遠不要修改 `~/.claude/settings.json` 或 `~/.claude/settings.local.json`** — 這些是使用者設定檔，不屬於 GEO-SEO 工具箱。
- **若已是最新狀態**（沒有差異），回報該結果並略過複製步驟。
- **重啟提醒：** 提醒使用者技能變更會在新的 Claude Code 工作階段生效。要使用更新後的技能，應重新啟動工作階段。
