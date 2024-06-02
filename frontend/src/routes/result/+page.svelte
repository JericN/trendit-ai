<script lang="ts">
	import { ListBox, ListBoxItem, popup } from '@skeletonlabs/skeleton';
	import type { PopupSettings } from '@skeletonlabs/skeleton';
	import Name from './Name.svelte';
	import Group from './Group.svelte';

	export let data;
	$: ({ subreddit, topics } = data);

	let comboboxValue: string;
</script>

<div class="flex flex-col px-20 gap-10">
	<div class="flex flex-col">
		<div class="flex text-3xl justify-between items-center">
			<Name {subreddit} />
			<Group {comboboxValue} />
		</div>
	</div>
	{#each topics as topic}
		<div class="flex justify-between">
			<div class="truncate">{topic.label}</div>
		</div>
	{/each}

	<hr class="border-2 border-surface-100-800-token" />
	<div class="self-center text-2xl w-full h-full">Explore</div>
</div>
