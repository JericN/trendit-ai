<script>
	import { getModalStore } from '@skeletonlabs/skeleton';
	const modalStore = getModalStore();

	const subreddits = [
		'AskReddit',
		'sports',
		'movies',
		'boxoffice',
		'NetflixBestOf',
		'worldnews',
		'news',
		'ArtificialInteligence',
		'MachineLearning',
		'artificial'
	];
</script>

{#if $modalStore[0]}
	<div class="h-full max-w-xl min-w-sm w-full bg-slate-600 px-8 py-6 rounded-xl text-white">
		<div class="flex justify-between">
			<div class="font-bold text-lg text-reddit mb-2">Available subreddits</div>
		</div>
		<ol class="list-disc ml-6">
			{#each subreddits as subreddit}
				<li class="mb-2 text-sm">{subreddit}</li>
			{/each}
		</ol>
	</div>
{/if}
