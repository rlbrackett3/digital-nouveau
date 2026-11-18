// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	// canonical URL = live host; flip back to https://blog.digitalnouveau.com at Wix cutover (DNS + A record)
	site: 'https://digital-nouveau.getforge.io',
	integrations: [mdx(), sitemap()],
});
