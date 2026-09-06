# 🐺 石門國小課照班 狼人殺冠軍賽 · 規則宣導站

桃園市龍潭區石門國民小學 課照班「狼人殺冠軍賽」的線上規則總覽。
一頁看懂 **兩場 12 人賽制、角色技能、遊戲流程、勝負判定與名詞解釋**，手機也好讀好操作。

## 🔗 線上網址

> https://cagoooo.github.io/smes-werewolf-rules/

## ✨ 特色

- 📱 **RWD 響應式**：手機 / 平板 / 投影電腦都好讀，導覽列可橫向滑動
- 🌙 **夜色主題 + 亮暗切換**：符合狼人殺氛圍，課堂投影可切亮色
- 🎭 **角色卡片化**：三大陣營（狼人 / 神職 / 平民）技能一目了然，含 EMOJI 與 SVG 狼頭圖示
- ⚔️ **兩場賽制切換**：第一場（騎士）／ 第二場（惡靈騎士 × 守衛）配置與特殊規則分開呈現
- 📖 **名詞解釋**：自爆、悶技能、屠邊、綁票、同守同救、夜槍等關鍵字隨點隨查
- 🔄 **PWA + Service Worker 版本更新通知**：部署新版後，已開著網頁的使用者會自動跳出「重新整理載入最新版」提示

## 🛠️ 維護方式

純靜態網站，無 build step。修改 `index.html` 後若要讓使用者收到更新通知，**務必升版**：

```powershell
# 在專案根目錄執行（會同步 version.json / sw.js / index.html 三處版本號）
powershell -ExecutionPolicy Bypass -File scripts/bump-version.ps1 -Notes "這次改了什麼"
git add -A
git commit -m "更新內容"
git push
```

> SW 的 `BUILD_VERSION` 位元組一定要隨版本改變，瀏覽器才會偵測為新版並觸發更新通知。

## 📁 結構

```
index.html              主頁（含所有規則內容、樣式、SW 註冊與更新通知）
sw.js                   Service Worker（版本控管 + 快取策略）
manifest.webmanifest    PWA manifest
version.json            版本檔（前端輪詢用）
favicon.svg / .ico      狼頭滿月圖示
apple-touch-icon.png    iOS 主畫面圖示
assets/                 app icons（192/512 + maskable）、OG 預覽圖
scripts/                圖示生成、一鍵升版腳本
```

---

Made with ❤️ by [阿凱老師](https://www.smes.tyc.edu.tw/modules/tadnews/page.php?ncsn=11&nsn=16#a5)

---

<!-- BEGIN:PROJECT_GUIDE -->
## 專案導覽

🐺 石門國小課照班狼人殺冠軍賽規則宣導站｜RWD + PWA 更新通知

- 專案定位：互動遊戲／遊戲化學習專案
- Repository：`cagoooo/smes-werewolf-rules`
- 可見性：公開
- 主要技術：HTML
- 線上入口：<https://cagoooo.github.io/smes-werewolf-rules/>

### 可以怎麼應用

- 課堂暖身、複習活動或學習站任務
- 校慶、闖關或社團活動中的互動挑戰
- 替換題庫、美術、音效與規則後，延伸成其他學科或主題遊戲

這些是依目前專案定位整理的延伸方向，不代表所有情境都已內建完成；實作前請先確認現有功能與資料格式。

### 技術與專案結構

- `README.md`
- `apple-touch-icon.png`
- `index.html`
- `scripts`

檔案結構會隨版本演進；若本節與程式碼不一致，以目前預設分支的原始碼為準。

### 本機執行

這是可直接由瀏覽器載入的靜態網站。可用任一靜態檔案伺服器預覽，例如：
```bash
python -m http.server 8000
```
接著開啟 `http://localhost:8000`。請避免直接以 `file://` 測試需要模組、請求或 Service Worker 的功能。

### 給 AI Agent 的接手指南

1. 先閱讀本 README、`AGENTS.md`（若有）、套件腳本與部署設定。
2. 先找出遊戲狀態、關卡／題庫資料與輸入控制的來源，再調整規則。
3. 更換素材時同步檢查授權、載入路徑、碰撞區域與不同螢幕比例。
4. 修改後至少驗證開始、遊玩、計分／勝負、重新開始，以及手機與桌面版面。
5. 不要捏造尚未存在的功能；README 與實作有落差時，應同時更新文件。
6. 提交前只納入本次任務檔案，並記錄實際執行過的驗證。

### 安全與資料注意事項

- 不要提交 `.env`、服務帳號、API 金鑰、token、學生個資或正式環境匯出資料。
- 使用 Firebase、Supabase、Google API 或其他雲端服務時，請建立自己的測試專案並套用最小權限。
- 若要公開衍生作品，請先確認程式碼、圖片、音訊、字型與教材內容的授權。

### 貢獻與客製化

歡迎依教學現場、活動或工作流程需求進行 fork／客製化。建議在變更說明中交代使用情境、主要修改、測試方式，以及是否影響資料格式或部署設定。
<!-- END:PROJECT_GUIDE -->
