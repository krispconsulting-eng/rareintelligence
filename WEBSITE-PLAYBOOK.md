# Website Playbook — GitHub Desktop + Vercel

A reusable, hand-it-to-anyone guide for editing and publishing **any** of our
websites. Works the same for every site — just swap in that site's name and links
from the **Site Registry** below.

No coding experience needed. Everything is done in **GitHub Desktop** (a free app)
and on two websites (github.com and vercel.com). No command line.

---

## How it all works (read once)

Two tools, two jobs:

| Tool | Its job | Think of it as… |
| --- | --- | --- |
| **GitHub** | Stores the website's files and every saved version | The filing cabinet |
| **GitHub Desktop** | The app on your computer that moves your edits to GitHub | The delivery van |
| **Vercel** | Publishes the files live on the web | The shop window |

**The golden loop — every change follows this path:**

```
Edit a file  →  Commit (save)  →  Push (send to GitHub)  →  Vercel auto-publishes (~30s)
```

Once a site is set up, **publishing = pushing to GitHub.** Vercel does the rest.
You never upload files to Vercel by hand.

**One key word — the branch:**
- **`main`** = the live public website. Treat it as sacred.
- Any other branch = a private **draft** you can experiment on safely. Vercel even
  gives each draft its own preview link. Nothing you do on a draft touches the live
  site until you choose to merge it into `main`.

---

# PART A — First-time setup for a site (do once per site)

> Skip this if the site is already set up in GitHub Desktop and Vercel — go to Part B.

### A1. Get the site onto your computer (GitHub Desktop)
1. Open **GitHub Desktop** → **File → Clone repository**.
2. Pick the site's repo (see **Repo** in the Site Registry) → choose a local folder →
   **Clone**.
3. It now lives on your computer and is linked to GitHub. ✅

### A2. Make sure the site has a `main` branch (on github.com)
Some repos don't have one yet. `main` is the branch Vercel publishes.
1. Go to the repo on **github.com**.
2. Click the **branch dropdown** (top-left) → type **`main`** → **Create branch:
   main from …** (create it from whichever branch currently has the finished site).
3. **Settings → Branches → Default branch** → switch the default to **`main`**.
4. Back in GitHub Desktop, click **Fetch origin**, then the **Current Branch**
   dropdown → choose **`main`**.

### A3. Connect the site to Vercel (on vercel.com)
1. Go to **vercel.com** → sign in with **GitHub** (one time only).
2. **Add New… → Project** → find the site's repo → **Import**.
   - Don't see it? Click **Adjust GitHub App Permissions** and grant access.
3. Settings on the import screen:
   - **Framework Preset:** **Other**
   - **Build Command:** leave **empty**
   - **Output Directory:** leave default (**`.`** / root)
4. Click **Deploy**, wait ~30 seconds.
5. Copy the live URL it gives you (e.g. `the-site.vercel.app`) into the Site Registry.
6. Check **Project → Settings → Git → Production Branch** says **`main`**.

The site is now live and will auto-update on every push. 🎉

---

# PART B — The everyday workflow (do this for every change)

This is the loop you'll repeat forever, on any site. **All in GitHub Desktop.**

### Simple changes — edit directly on `main`
1. **GitHub Desktop** → **Current Branch** dropdown → make sure you're on **`main`**.
2. Click **Fetch origin** (top bar) to grab the latest version first. *(Always do this
   before editing — it prevents conflicts.)*
3. Open the file(s) in your editor, make your changes, **save** in the editor.
4. Back in GitHub Desktop, the **Changes** tab (left) lists what you changed.
5. Bottom-left: type a short **Summary** (e.g. *"Update homepage headline"*) →
   click **Commit to main**.
6. Top bar: click **Push origin**.
7. ~30 seconds later, Vercel has published it. Refresh the live URL. ✅

### Bigger / riskier changes — use a draft branch (recommended)
So you can preview without risking the live site:
1. GitHub Desktop → **Current Branch** dropdown → **New Branch** → name it for the job
   (e.g. `new-about-page`) → create it **from `main`**.
2. Edit, save, **Commit**, **Push origin** — exactly like above, but on this branch.
3. GitHub Desktop will show **"Create Pull Request"** → click it (opens your browser).
4. On github.com, Vercel posts a **Preview** link on the Pull Request — open it to
   check your changes on a private test version of the site.
5. Happy? Click **Merge pull request**. Now `main` updates and the **live** site
   republishes automatically.
6. Back in GitHub Desktop: switch **Current Branch** to **`main`** → **Fetch origin**
   to pull the merged result down.

---

## Branch & button cheat-sheet

| You want to… | In GitHub Desktop / GitHub |
| --- | --- |
| Get the latest before editing | **Fetch origin** (then Pull if it offers) |
| Save your edits | Write a Summary → **Commit to <branch>** |
| Send saved edits to GitHub (and publish, if on `main`) | **Push origin** |
| Start a safe draft | **Current Branch → New Branch** (from `main`) |
| Preview a draft | Push it → open the **Vercel preview link** on the Pull Request |
| Make a draft go live | Open a **Pull Request** → **Merge** into `main` |
| Switch what you're working on | **Current Branch** dropdown |
| Undo a bad change | GitHub Desktop **History** tab → right-click a commit → **Revert** |
| Throw a draft away | Delete that branch — `main` is untouched |

**Golden rules**
- `main` = the live public site. When unsure, work on a draft branch and preview first.
- **Fetch origin before you start**, **Push origin when you're done.**
- **Commit** = a saved snapshot with a note. Commit often; you can always go back via History.
- One repo = one Vercel project = one website.

---

## Site Registry

Fill in each site's details once, then this becomes the only reference anyone needs.
(`Repo` = the `owner/name` shown in GitHub Desktop / the github.com URL.
`Live URL` = the Vercel address.)

| Site | Repo (GitHub) | Live URL (Vercel) | Custom domain |
| --- | --- | --- | --- |
| **Rare Intelligence** | `krispconsulting-eng/rareintelligence` | _add after Vercel deploy_ | _optional_ |
| **Kris Pierce Consulting** | _add repo_ | _add after Vercel deploy_ | _optional_ |
| **SCN2A Australia** | _add repo_ | _add after Vercel deploy_ | _optional_ |
| _…(repeat for each of your sites)_ | | | |

> Tip: keep this same table for all 23 sites. Each row is fully independent —
> setting up or editing one site never affects the others.

---

## Using your own domain (optional, per site)

1. Vercel → that site's **Project → Settings → Domains → Add**.
2. Enter the domain (e.g. `kpconsulting.com.au`) → **Add**.
3. Vercel shows 1–2 DNS records → paste them into the domain registrar
   (GoDaddy / Namecheap / Crazy Domains, etc.).
4. Wait a few minutes — Vercel issues HTTPS automatically.

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| **GitHub Pages 404** ("There isn't a GitHub Pages site here") | Ignore — we publish via Vercel, not Pages. |
| My change isn't live | Did you **Push origin**? Was it on **`main`** (or merged into it)? Check Vercel's **Deployments** tab. |
| Page is blank / styles missing on Vercel | Framework Preset = **Other**, Output Directory = root (**`.`**), Build Command empty. |
| Vercel can't see a repo | Vercel **Settings → Git → Manage GitHub App** → grant access to that repo. |
| GitHub Desktop says "conflict" | You edited something that also changed on GitHub. Click **Fetch/Pull** first next time; for now, accept the latest version or ask for help. |
| No `main` branch | Do **Part A2**. |

---

*Hand this whole document to anyone editing the sites. For one specific site, give them
its row from the Site Registry plus Part B. Stuck on a step? Note the site and step
number and we'll sort it.*
