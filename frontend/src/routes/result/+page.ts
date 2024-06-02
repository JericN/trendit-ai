import { getData } from '$lib/database.js';
import { initializeFirebase } from '$lib/firebase';

export async function load({ url}) {
    initializeFirebase();

    const subreddit = url.searchParams.get('subreddit');
    if(!subreddit) {
        throw new Error('No subreddit provided');
    }

    const topics = await getData(subreddit);
    return {topics, subreddit};

}