import { collection, getDocs } from 'firebase/firestore';
import { db } from '$lib/firebase';
import type { Topic, MonthlyTopics } from '$lib/types';

export async function getSubreddits(): Promise<string[]> {
	const colRef = collection(db, 'admin_subreddit_collections');
	const querySnapshot = await getDocs(colRef);

	const subreddits = [] as string[];
	querySnapshot.forEach((doc) => {
		subreddits.push(doc.id);
	});

	console.log('subreddits', subreddits);

	return subreddits;
}

export async function getData(subreddit: string): Promise<MonthlyTopics[]> {
	const monthlyTopics = [];

	let res = [] as string[];
	const subreddits = await getSubreddits();
	const searchParams = subreddit.split('&');
	
	res = subreddits.filter((sub) => {
		const subtokens = sub.split('&');
		if(searchParams.length !== subtokens.length) return false;
		for (const param of searchParams) {
			if (!subtokens.includes(param)) {
				return false;
			}
		}
		return true;
	});

	if(res.length != 1) {
		return [];
	}

	const targetSubreddit = res[0];
	const colRef = collection(db, targetSubreddit);
	const querySnapshot = await getDocs(colRef);

	for (const doc of querySnapshot.docs) {
		const data = doc.data();

		const topicRef = collection(db, targetSubreddit, doc.id, 'topics');
		const topicQuerySnapshot = await getDocs(topicRef);

		const topics = [] as Topic[];
		topicQuerySnapshot.forEach((topicDoc) => {
			const topicData = topicDoc.data();
			if (!topicData.label.endsWith('.')) {
				topicData.label += '.';
			}
			topics.push(topicData as Topic);
		});

		// sort topics by doc_count
		topics.sort((a, b) => b.doc_count - a.doc_count);

		const monthlyTopic = {
			date: data.date,
			doc_count: data.doc_count,
			topics: topics
		};
		monthlyTopics.push(monthlyTopic);
	}
	console.log('test', monthlyTopics);
	return monthlyTopics;
}
