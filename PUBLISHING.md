# Publishing the dashboard on GitHub Pages

GitHub Pages hosts the `docs/` folder as a public website at no cost. The page is a single self-contained HTML file, so no server or build service is needed. Total time: about 15 minutes the first time.

Two routes are given. Route A uses only the GitHub website. Route B uses Git on your computer and is better for later updates.

---

## Before you start

1. Create a free account at <https://github.com> if you do not have one. Your username becomes part of the page address.
2. Unzip `lebanon-graduate-futures.zip` to a folder on your computer.
3. Open `docs/index.html` in your browser and confirm the dashboard loads. (It needs an internet connection for the chart library and fonts.)
4. Decide with the team whether the repository will be **public**. GitHub Pages on a free account requires a public repository, which means anyone can see the workbook and code. Nothing in it is personal data, but confirm with Dr Zablit if the course has a rule on publishing project work.

---

## Route A: GitHub website only

### Step 1. Create the repository
1. Sign in to GitHub. Click **+** (top right), then **New repository**.
2. Repository name: `lebanon-graduate-futures`
3. Description: `MSBA 325 Team 5: Lebanon Graduate Futures dashboard`
4. Select **Public**.
5. Leave "Add a README", ".gitignore" and "licence" **unticked** (the project already has them).
6. Click **Create repository**.

### Step 2. Upload the files
1. On the new empty repository page, click **uploading an existing file**.
2. Open the unzipped folder on your computer. Select **everything inside it** (`data`, `docs`, `scripts`, `src`, `README.md`, `PUBLISHING.md`, `CHANGELOG.md`, `LICENSE`, `requirements.txt`, `.gitignore`) and drag it into the browser window. Folders upload with their contents.
   - The `.github` folder and `.gitignore` are hidden on most computers. On Mac press `Cmd + Shift + .` in Finder to show them; on Windows tick **View > Hidden items** in File Explorer. If `.github` will not upload, skip it: it is optional.
3. Commit message: `Initial dashboard`. Click **Commit changes**.
4. Check that the repository now shows the `docs` folder containing `index.html`.

### Step 3. Switch on GitHub Pages
1. In the repository, click **Settings** (top bar), then **Pages** (left menu).
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Set **Branch** to `main` and the folder to `/docs`. Click **Save**.
4. Wait one to two minutes, then refresh the Settings > Pages screen. A box appears: "Your site is live at `https://<username>.github.io/lebanon-graduate-futures/`".

### Step 4. Check the live page
1. Open the address. Check that all charts draw, that the buttons switch views, that dark mode works, and that "Data behind this chart" opens a table.
2. Open it on a phone as well.
3. If you see a 404 error, wait two more minutes and confirm the folder in Settings > Pages is `/docs`, not `/ (root)`.

### Step 5. Finish the repository page
1. On the repository's main page, click the gear icon beside **About** (right column).
2. Tick **Use your GitHub Pages website** so the link shows on the repository. Add topics: `data-visualization`, `plotly`, `lebanon`, `labour-market`, `aub`.
3. Edit `README.md` (pencil icon) and replace `<your-github-username>` in the live-page line with your username. Commit.

### Step 6. Add your teammates
**Settings > Collaborators > Add people**: add Amal, Hidaya, Maya and Hassan by GitHub username or email so they can edit.

---

## Route B: Git on your computer

Install Git from <https://git-scm.com> if needed. Then, in a terminal opened in the unzipped folder:

```bash
git init -b main
git add .
git commit -m "Initial dashboard"
```

Create the empty repository on GitHub as in Route A, Step 1, then:

```bash
git remote add origin https://github.com/<username>/lebanon-graduate-futures.git
git push -u origin main
```

GitHub asks you to sign in in the browser the first time. Then follow Route A, Steps 3 to 6.

To rebuild after a data change:

```bash
pip install -r requirements.txt
python scripts/build_dashboard.py
git add data docs
git commit -m "Update data"
git push
```

---

## Updating the data later

**Without Python (uses the included workflow).** If the `.github` folder was uploaded:
1. In the repository, open the `data` folder, click **Add file > Upload files**, and upload the new `Lebanon_Graduate_Futures_Data.xlsx` with exactly the same name. Commit.
2. Click the **Actions** tab. The "Rebuild dashboard" job runs for about a minute and commits a new `docs/index.html`.
3. The first time, if the job fails with a permission error: **Settings > Actions > General > Workflow permissions**, select **Read and write permissions**, Save, then re-run the job from the Actions tab.

**With Python.** Use the Route B rebuild commands above.

Either way, keep tab names and column headers in the workbook unchanged. The build stops with a clear message if a value the page needs is missing, so a broken workbook cannot overwrite a working page.

---

## Optional: a shorter address

The default address works for submission. If the team wants a custom domain (for example `graduatefutures.org`), buy the domain, then in **Settings > Pages > Custom domain** enter it and follow GitHub's DNS instructions. This is not needed for the course.

## Checklist before sharing the link

- [ ] Page loads on desktop and phone
- [ ] All five evidence sections, the model, the scenario console, the explorer and the gaps register display
- [ ] Badges show 16 secondary-source figures until the January 2022 CAS tables are checked
- [ ] README live-page link updated with your username
- [ ] Team members added as collaborators
- [ ] Course guidelines checked for any rule on public posting
