import { collection, getDocs } from 'firebase/firestore';
import { db } from '$lib/firebase';
import type { Topic, MonthlyTopics } from '$lib/types';

export async function getData(subreddit: string): Promise<MonthlyTopics[]> {
	const monthlyTopics = [];

	const colRef = collection(db, subreddit);
	const querySnapshot = await getDocs(colRef);

	for (const doc of querySnapshot.docs) {
		const data = doc.data();

		const topicRef = collection(db, subreddit, doc.id, 'topics');
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
