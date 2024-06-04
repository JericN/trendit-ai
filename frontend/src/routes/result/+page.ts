import { getData } from '$lib/database.js';
import { initializeFirebase } from '$lib/firebase';

export async function load({ url }) {
	initializeFirebase();

	const subreddit = url.searchParams.get('subreddit');
	if (!subreddit) {
		throw new Error('No subreddit provided');
	}

	const formattedSubreddit = subreddit.split(',').join('&');

	const monthlyTopics = await getData(formattedSubreddit);
	console.log(monthlyTopics);

	return { monthlyTopics, subreddit };
}
