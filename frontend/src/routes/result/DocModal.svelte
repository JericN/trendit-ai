<script>
	import { SlideToggle, getModalStore } from '@skeletonlabs/skeleton';
	const modalStore = getModalStore();

	function redir(url) {
		window.open(url, '_blank');
	}

	$: value = false;
</script>

{#if $modalStore[0]}
	<div class="h-full max-w-xl min-w-sm w-full bg-slate-600 px-8 py-6 rounded-xl text-white">
		<div class="flex justify-between">
			<div class="font-bold text-lg text-reddit mb-2">Representative Posts</div>
			<div class="flex justify-center gap-2">
				<span class=" text-reddit">{value ? 'Keywords' : 'Posts'}</span>
				<SlideToggle bind:checked={value} name="sliderer" active="bg-primary-500" size="sm" />
			</div>
		</div>
		<div class="text-sm mb-4">{$modalStore[0].meta.topic.label}</div>
		<ol class="list-disc ml-6">
			{#if value}
				{#each $modalStore[0].meta.topic.keywords as keyword}
					<li class="mb-2 text-sm">{keyword}</li>
				{/each}
			{:else}
				{#each $modalStore[0].meta.topic.rep_docs as doc}
					<li class="mb-2">
						<button class="text-sm text-left" on:click={() => redir(doc.url)}>{doc.content}</button>
					</li>
				{/each}
			{/if}
		</ol>
	</div>
{/if}
