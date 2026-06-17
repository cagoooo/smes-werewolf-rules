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
