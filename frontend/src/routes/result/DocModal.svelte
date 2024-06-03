<script>
	import { getModalStore } from '@skeletonlabs/skeleton';
	const modalStore = getModalStore();

	function redir(url) {
		window.open(url, '_blank');
	}
</script>

{#if $modalStore[0]}
	<div class="h-full max-w-xl bg-slate-600 px-8 py-6 rounded-xl text-white">
		<div class="font-bold text-lg text-reddit mb-2">Representative Posts</div>
		<ol class="list-disc ml-6">
			{#each $modalStore[0].meta.topic.rep_docs as doc}
				<li class="mb-2">
					<button class="text-sm text-left" on:click={() => redir(doc.url)}>{doc.content}</button>
				</li>
			{/each}
		</ol>
	</div>
{/if}
