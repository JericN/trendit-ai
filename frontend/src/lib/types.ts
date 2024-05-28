export interface Docs {
    content: string;
    url: string;
}

export interface Topic {
    label: string;
    rep_docs: Docs[];
    keywords: string[];
}

