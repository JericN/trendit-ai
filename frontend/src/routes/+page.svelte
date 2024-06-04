<script lang="ts">
	import Submit from '~icons/formkit/submit';
	import { goto } from '$app/navigation';
	import { InputChip } from '@skeletonlabs/skeleton';
	import { type ModalSettings, type ModalComponent, getModalStore } from '@skeletonlabs/skeleton';
	import DocModal from './DocModal.svelte';
	let error = '';

	function handleSubmit() {
		if (subreddits.length === 0) {
			error = 'Please enter a subreddit.';
			return;
		} else {
			goto(`/result?subreddit=${encodeURIComponent(subreddits.toString())}`);
		}
	}
	let subreddits: string[] = [];

	const modalStore = getModalStore();
	const modalComponent: ModalComponent = {
		ref: DocModal
	};

	const modal: ModalSettings = {
		type: 'component',
		component: modalComponent
	};

	function openDocuments() {
		modalStore.trigger({
			type: 'component',
			component: modalComponent
		});
	}
</script>

<div class="flex flex-col h-full justify-center items-center gap-20">
	<div class="font-nova-square text-center text-5xl">
		Explore Top Discussions
		<br />from <button on:click={openDocuments} class="text-reddit">Subreddits.</button>
	</div>
	<div class="flex w-full max-w-sm">
		<InputChip
			bind:value={subreddits}
			name="chips"
			allowUpperCase={true}
			class="bg-reddit text-white border-0"
			regionInput="placeholder-white text-center mt-0.5"
			regionChipList="absolute justify-center max-w-80 w-full"
			rounded="rounded-r-none rounded-l-full"
			placeholder="Enter a subreddit"
		/>
		<button
			type="button"
			class="btn bg-white text-reddit px-2 text-bold rounded-l-none rounded-r-full"
			on:click={handleSubmit}
		>
			<Submit class="size-6" />
		</button>
	</div>

	{#if error}
		<div class="text-red-500 font-chivo">{error}</div>
	{/if}
</div>
