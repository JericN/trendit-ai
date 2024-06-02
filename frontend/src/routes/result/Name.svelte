<script>
	import RedditIcon from '~icons/logos/reddit-icon';
	export let subreddit;
</script>

<div>
	<a
		href={`https://www.reddit.com/r/${subreddit}`}
		target="_blank"
		rel="noopener noreferrer"
		class="flex gap-4"
	>
		<RedditIcon class="size-10" />
		<span>r/{subreddit}</span>
	</a>
</div>
