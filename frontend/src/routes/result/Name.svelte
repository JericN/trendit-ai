<script>
	import RedditIcon from '~icons/logos/reddit-icon';
	export let subreddit;
	$: subreddits = subreddit.split(',');
</script>

<div>
	{#each subreddits as subreddit}
		<a
			href={`https://www.reddit.com/r/${subreddit}`}
			target="_blank"
			rel="noopener noreferrer"
			class="flex gap-4"
		>
			<RedditIcon class="size-8" />
			<span class="text-3xl">r/{subreddit}</span>
		</a>
	{/each}
</div>
