<script lang="ts">
	import Submit from '~icons/formkit/submit';
	import { goto } from '$app/navigation';

	let subreddit = '';
	let error = '';

	function handleSubmit() {
		if (!subreddit) {
			error = 'Please enter a subreddit.';
			return;
		} else {
			goto(`/result?subreddit=${encodeURIComponent(subreddit)}`);
		}
	}
</script>

<div class="flex flex-col grow justify-center items-center gap-10">
	<div class="font-nova-square text-center text-5xl">
		Explore Top Discussions
		<br />from <span class="text-reddit">Subreddits.</span>
	</div>
	<div class="font-chivo bg-reddit input-group input-group-divider grid-cols-[2fr_auto] w-1/5">
		<input
			type="text"
			class="text-white text-lg px-6 placeholder:text-slate-200"
			placeholder="Enter a subreddit..."
			bind:value={subreddit}
		/>
		<button type="button" class="btn bg-white text-reddit text-bold m-2" on:click={handleSubmit}>
			<Submit class="size-5" />
		</button>
	</div>
	{#if error}
		<div class="text-red-500 font-chivo">{error}</div>
	{/if}
</div>

<footer class="text-center p-6 text-black font-nova-square text-lg">
	Made with BERTopic and ChatGPT4o.
</footer>
