<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });
</script>

<body class="flex flex-col h-screen border-reddit border-2">
	<header class="text-center p-6 text-reddit font-nova-square text-2xl font-bold">TRENDDIT</header>
	<slot />
</body>
