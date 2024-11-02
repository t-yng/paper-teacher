import { writable } from 'svelte/store';

export interface Paper {
	title: string;
	sections: {
		heading: string;
		level: number;
		body: string;
	}[];
}

export const paperStore = writable<Paper | null>(null);
