# Publishing Manual — Rare Intelligence

A plain-English guide to getting this website **live on the internet with Vercel**,
and to **saving your work properly in GitHub** so nothing ever gets lost.

No prior coding experience assumed. You can do almost all of this by clicking
buttons on websites — the command-line steps are optional extras at the end.

---

## 0. The big picture (read this once)

There are two services, and they do different jobs:

| Service | Its job | Think of it as… |
| --- | --- | --- |
| **GitHub** | Stores your website files and every saved version of them | The filing cabinet / Google Drive |
| **Vercel** | Takes the files from GitHub and shows them live on the web | The shop window |

The flow is always:

```
You change a file  →  save it to GitHub  →  Vercel notices  →  site updates automatically
```

Once it's set up, **publishing a change = saving to GitHub**. Vercel does the rest
within ~30 seconds. You never "upload" to Vercel by hand.

> Why not GitHub Pages? It can host this too, but it needed a setting toggled that
> your account blocked (that's the **404** you saw). Vercel is simpler for this kind
> of site and gives you a live preview link for every draft — so we're using Vercel.

---

## 1. Tidy up the branches first (one-time, 5 minutes)

A **branch** is just a named version of your project. Right now your repo has two
branches with confusing robot-generated names and **no `main` branch**, which is the
one Vercel expects. Let's fix that so there's one obvious "this is the live site" branch.

> You only ever need **one** main branch for the live site. Everything else is a draft.

### Do this on the GitHub website (easiest):

1. Go to **https://github.com/krispconsulting-eng/rareintelligence**
2. Click the **branch dropdown** (top-left, shows the current branch name).
3. In the box, type **`main`**, then click **"Create branch: main from …"**.
   - Pick it **from** `claude/intelligent-hamilton-J485B` — that branch has the full
     site *plus* the new testimonials page.
4. Make `main` the default:
   - Go to **Settings → Branches** (or **Settings → General → Default branch**).
   - Click the **swap icon**, choose **`main`**, confirm.
5. (Optional, later) Once you're happy, you can delete the two old `claude/…`
   branches to reduce clutter: **Branches** page → trash icon next to each.

After this, **`main` = your live website**. Done.

> 🔒 **Note:** I (Claude) am restricted to working only on the
> `claude/intelligent-hamilton-J485B` branch, so I can't create `main` or change the
> default for you — those four clicks above are yours to make. Everything I build will
> land on that branch, and you merge it into `main` (see Section 3).

---

## 2. Connect Vercel and go live (one-time, 5 minutes)

1. Go to **https://vercel.com** and click **Sign Up** → **Continue with GitHub**.
   (This links the two accounts so Vercel can read your repo.)
2. On the Vercel dashboard, click **Add New… → Project**.
3. Find **`rareintelligence`** in the list and click **Import**.
   - If you don't see it: click **"Adjust GitHub App Permissions"** and grant Vercel
     access to the repo.
4. On the configuration screen:
   - **Framework Preset:** choose **Other**.
   - **Build Command:** leave **empty** (this is a plain HTML site — no build needed).
   - **Output Directory:** leave as the default / **`.`** (the project root).
   - **Root Directory:** leave as is.
5. Click **Deploy**. Wait ~30 seconds.
6. 🎉 You'll get a live URL like **`https://rareintelligence.vercel.app`**.
   - Your homepage: `…vercel.app/`
   - The testimonials page: `…vercel.app/testimonials.html`

### Point Vercel at the right branch
Vercel publishes whatever your **default branch** is. If you did Section 1, that's
`main` — perfect, nothing to change. To check or change it:
- Vercel **Project → Settings → Git → Production Branch** → make sure it says **`main`**.

---

## 3. Your everyday workflow — how to save & publish changes

This is the loop you'll repeat forever. Two ways: the simple website way, or git.

### Option A — All on the GitHub website (no software to install)

1. Go to the repo, make sure you're on the **`main`** branch.
2. Click the file you want to edit (e.g. `index.html`) → click the **pencil ✏️**.
3. Make your change.
4. Scroll down to **"Commit changes"**, type a short note like *"update hero text"*,
   click **Commit**.
5. Vercel auto-redeploys. ~30 seconds later your live site shows the change.

That's it. **Commit = save = publish.**

### Option B — Safer way using a draft branch (recommended for bigger changes)

So you never break the live site while experimenting:

1. On GitHub, create a new branch from `main` — call it something like `edit-pricing`.
2. Make all your edits on that branch (pencil method above, but on `edit-pricing`).
3. Vercel automatically builds a **Preview** for that branch — a separate test URL it
   posts right in the branch/Pull Request. Check your changes there, safely.
4. When happy, open a **Pull Request** (a "please merge my draft into the live site"
   request): **Pull requests → New → base: `main`, compare: `edit-pricing` → Create**.
5. Click **Merge**. Now `main` updates and the live site redeploys.

> **Preview vs Production:** every branch you push gets its own private preview URL.
> Only `main` (production) changes the real public site. This is the big reason to use
> Vercel — you can always look before you leap.

---

## 4. Branch cheat-sheet

| You want to… | Do this |
| --- | --- |
| See your live site | Visit your `…vercel.app` URL (or custom domain) |
| Make a quick safe edit | Edit a file on `main` → Commit |
| Try something risky | New branch → edit there → check the preview URL → merge when happy |
| Undo a bad change | GitHub: open the file → **History** → pick the older version, or revert the commit |
| Throw away a draft | Just delete that branch — `main` is untouched |
| Know what's "live" | Whatever is on **`main`** right now |

**Golden rules**
- `main` is sacred — it's the public site. When unsure, edit on a draft branch first.
- A **commit** is a saved snapshot with a note. Commit often; you can always go back.
- **Pushing** a commit to GitHub is what triggers Vercel to redeploy.

---

## 5. (Optional) Use your own domain

When you own a domain (e.g. `rareintelligence.com`):
1. Vercel **Project → Settings → Domains → Add**.
2. Type your domain, click **Add**.
3. Vercel shows you 1–2 DNS records to paste into your domain registrar (GoDaddy,
   Namecheap, etc.). Add them, wait a few minutes, and Vercel auto-issues HTTPS.

---

## 6. Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| **GitHub Pages 404** ("There isn't a GitHub Pages site here") | Pages was never enabled — ignore it, you're using Vercel now. |
| Vercel deployed but page is blank / missing styles | Make sure **Output Directory** is the root (`.`) and Framework Preset is **Other**. |
| My change isn't showing | Confirm you committed to **`main`** (or merged your branch into it). Check the Vercel **Deployments** tab for the latest build. |
| Vercel can't see the repo | Vercel **Settings → Git → Manage GitHub App** → grant access to `rareintelligence`. |
| Don't see a `main` branch | Do **Section 1** — create it and set it as default. |

---

## 7. (Optional) Doing it from your own computer with Git

If you'd rather edit files locally instead of on the website:

```bash
# one-time: copy the repo to your machine
git clone https://github.com/krispconsulting-eng/rareintelligence.git
cd rareintelligence

# start a draft branch
git checkout -b my-edit

# ... edit files in your code editor ...

# save a snapshot and send it to GitHub
git add .
git commit -m "describe what you changed"
git push -u origin my-edit
```

Then open a Pull Request on GitHub to merge `my-edit` into `main` (Section 3, Option B).
To preview locally before pushing, run `python3 -m http.server 8000` and open
`http://localhost:8000/testimonials.html`.

---

*Questions or stuck on a step? Tell me which section and I'll walk you through it.*
