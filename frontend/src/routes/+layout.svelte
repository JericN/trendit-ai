<script lang="ts">
	import '../app.postcss';
	import { initializeStores, Modal } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';

	import { storePopup } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });
	initializeStores();

	$: current = $page.url.pathname;
	$: isResult = current.includes('result');
</script>

<Modal />
<body
	class="flex flex-col h-full border-reddit border-2 font-chivo w-full items-center overflow-y-scroll"
>
	<a href="/" class="text-center p-6 text-reddit font-nova-square text-3xl font-bold">TRENDDIT</a>
	<slot />
	{#if !isResult}
		<footer class="text-center p-6 text-black font-nova-square text-lg">
			Made with BERTopic and ChatGPT4o.
		</footer>
	{/if}
</body>
