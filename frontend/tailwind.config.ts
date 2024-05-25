import { join } from 'path'
import type { Config } from 'tailwindcss'
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import { skeleton } from '@skeletonlabs/tw-plugin';
import { Trenddit } from './src/Trenddit'

export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}', join(require.resolve('@skeletonlabs/skeleton'), '../**/*.{html,js,svelte,ts}')],
	theme: {
		extend: {
			fontFamily: {
				'chivo': ['Chivo', 'sans-serif'],
				'nova-square': ['"Nova Square"', 'sans-serif'],
			},
			colors: {
				'reddit': '#FF4500',
			},
		},
	},
	plugins: [
		forms,
		typography,
		skeleton({
			themes: {
				custom: [
					Trenddit,
				],
			},
		}),
	],
} satisfies Config;
