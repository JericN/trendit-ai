<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	$: current = $page.url.pathname;
	$: isResult = current.includes('result');
</script>

<body class="flex flex-col h-screen border-reddit border-2 font-chivo">
	<header class="text-center p-6 text-reddit font-nova-square text-2xl font-bold">TRENDDIT</header>
	<slot />
	{#if !isResult}
		<footer class="text-center p-6 text-black font-nova-square text-lg">
			Made with BERTopic and ChatGPT4o.
		</footer>
	{/if}
</body>
