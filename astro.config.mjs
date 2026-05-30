// @ts-check
import { defineConfig } from 'astro/config';

// For GitHub Pages.
// - User/org page (repo named <user>.github.io): leave `base` as '/'.
// - Project page (any other repo name): set `base` to '/<repo-name>'.
// Update `site` to your final URL.
export default defineConfig({
  site: 'https://outcomemachines.ai',
  base: '/',
  trailingSlash: 'ignore',
});
