export interface Docs {
	content: string;
	url: string;
}

export interface Topic {
	label: string;
	doc_count: number;
	rep_docs: Docs[];
	keywords: string[];
}

export interface MonthlyTopics {
	date: string;
	doc_count: number;
	topics: Topic[];
}
