<script lang="ts">
	import { type ModalSettings, type ModalComponent, getModalStore } from '@skeletonlabs/skeleton';
	import DocModal from './DocModal.svelte';
	import Name from './Name.svelte';
	import Group from './Group.svelte';

	const modalStore = getModalStore();

	export let data;
	$: ({ monthlyTopics, subreddit } = data);

	let comboboxValue: string;

	const modalComponent: ModalComponent = {
		ref: DocModal
	};

	const modal: ModalSettings = {
		type: 'component',
		component: modalComponent
	};

	function openDocuments(topic) {
		modalStore.trigger({
			type: 'component',
			component: modalComponent,
			meta: {
				topic: topic
			}
		});
	}
</script>

<div class="flex flex-col px-20 gap-8 max-w-4xl w-full h-full">
	<div class="flex flex-col">
		<div class="flex text-3xl justify-between items-center">
			<Name {subreddit} />
			<Group {comboboxValue} />
		</div>
	</div>
	{#each monthlyTopics as monthlyTopic}
		<div class="flex flex-col gap-2">
			<div class="font-bold text-xl">{monthlyTopic.date}</div>
			<ol class="list-decimal ml-6">
				{#each monthlyTopic.topics as topic}
					<li>
						<div class="flex items-center gap-1">
							<button class="truncate" on:click={() => openDocuments(topic)}>{topic.label}</button>
							<div class="text-xs">[{topic.doc_count}]</div>
						</div>
					</li>
				{/each}
			</ol>
		</div>
		<hr class="-mt-4 border-1" />
	{/each}
</div>
