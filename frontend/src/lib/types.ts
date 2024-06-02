export interface Docs {
    content: string;
    url: string;
}

export interface Topic {
    label: string;
    rank: number;
    rep_docs: Docs[];
    keywords: string[];
}

