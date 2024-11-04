import { writable } from 'svelte/store';

export interface PaperSection {
	id: string;
	order: number;
	heading: string;
	level: number;
	body: string;
}

export interface Paper {
	title: string;
	sections: PaperSection[];
}

export const paperStore = writable<Paper | null>(null);
