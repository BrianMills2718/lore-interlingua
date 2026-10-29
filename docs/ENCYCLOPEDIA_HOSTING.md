# Hosting the encyclopedia on GitHub Pages

**Status:** Deployment workflow prepared for the *public* `main` branch. This document describes how to activate and verify the site; it does **not** claim a live URL until the first successful GitHub Pages deployment.

## Intended URL

- Project entry point: `https://brianmills2718.github.io/lore-interlingua/`
- Full interactive atlas: `https://brianmills2718.github.io/lore-interlingua/encyclopedia/`
- Three-film imagery comparison: `https://brianmills2718.github.io/lore-interlingua/encyclopedia/imagery.html`

These are **expected** URLs following normal GitHub Pages conventions, **not verified working links** until deployment succeeds.

## One-time Pages settings

In the repository, open **Settings → Pages**. Under **Build and deployment → Source**, select **GitHub Actions**. This step may be necessary even after the workflow is merged: the standard `GITHUB_TOKEN` cannot bootstrap an unconfigured Pages site with `actions/configure-pages`'s special `enablement` option.

The [official GitHub instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) explain this setting. A GitHub Actions workflow named **Publish Visual–Semantic Encyclopedia** then builds from `main` and publishes the site; the deployment job uses the `github-pages` environment and only runs on `main` pushes or manual dispatch. Pull requests run the package/asset check but do not deploy.

If the initial run fails because Pages is not configured, select **GitHub Actions** in Pages settings, then use **Actions → Publish Visual–Semantic Encyclopedia → Run workflow** on `main` (or rerun the failed job).

## Publishing scope

The workflow deliberately publishes **only**:

- `encyclopedia/` (the atlas, scripts, styles and local imagery index),
- Experiments **009–013** (the cases and three review MP4 previews),
- selected linked documentation, the v0.2 corpus, the Catholic source-scoped example, and
- the existing historical **v0.4 offline ZIP**.

It does **not** publish the full research repository, `.git`, workflow internals, all tests or the broader conversation/inquiry archive. The repository is already public, but the selection keeps the hosted site focused. The upload includes experimental material; do not treat the film's physical metaphors as empirical astrophysics.

## Maintenance and verification

The public entry point redirects to `encyclopedia/index.html`; the atlas's **Cumulative imagery** link opens `imagery.html`. Asset paths are relative and preserved by the staging directory's mirrored structure. The workflow checks critical assets for both interactive cases and review videos before attempting a deployment.

On a successful deployment, check the **site directly**, not merely the workflow status: atlas navigation, both interactive cases, the three MP4 previews and the offline ZIP. A passing package test does **not** prove a working public site or viewer comprehension.

The historical v0.4 ZIP remains unchanged. The newest hosted site is built from the current `main` commit, not silently merged into the old package.
