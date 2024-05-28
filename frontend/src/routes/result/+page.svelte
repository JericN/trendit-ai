<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import RedditIcon from '~icons/logos/reddit-icon';
	import { getData } from '$lib/database';
	import { ListBox, ListBoxItem, popup } from '@skeletonlabs/skeleton';
	import type { PopupSettings } from '@skeletonlabs/skeleton';

	let subreddit = '';

	onMount(async () => {
		const queryParams = new URLSearchParams($page.url.search);
		subreddit = queryParams.get('subreddit') || 'unknown';

		const data = await getData();
		console.log(data);
	});

	let comboboxValue: string;

	const popupCombobox: PopupSettings = {
		event: 'click',
		target: 'popupCombobox',
		placement: 'bottom',
		closeQuery: '.listbox-item'
	};
</script>

<div class="grid grid-cols-3 gap-10 px-40 py-5 font-chivo">
	<div class="col-span-2 flex text-3xl justify-between items-center">
		{#if subreddit}
			<div class="flex gap-4">
				<a href={`https://www.reddit.com/r/${subreddit}`} target="_blank" rel="noopener noreferrer">
					<RedditIcon class="size-10" />
				</a>
				<span>r/{subreddit}</span>
			</div>
		{/if}

		<div>
			<button
				class="btn bg-reddit text-base text-white w-48 justify-between"
				use:popup={popupCombobox}
			>
				<span class="capitalize">{comboboxValue ?? 'View by'}</span>
				<span>↓</span>
			</button>

			<div
				class="card w-48 text-base bg-reddit text-white shadow-xl py-2"
				data-popup="popupCombobox"
			>
				<ListBox rounded="rounded-full m-1">
					<ListBoxItem
						bind:group={comboboxValue}
						name="view"
						value="month"
						active="bg-orange-400 text-white">Month</ListBoxItem
					>
					<ListBoxItem
						bind:group={comboboxValue}
						name="view"
						value="week"
						active="bg-orange-400 text-white">Week</ListBoxItem
					>
				</ListBox>
				<div class="arrow bg-surface-100-800-token" />
			</div>
		</div>
	</div>

	<div class="self-center text-2xl">Explore</div>
</div>
