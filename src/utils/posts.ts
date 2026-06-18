---
import { getCollection } from 'astro:content';

export interface Post {
	id: string;
	data: {
		title: string;
		description: string;
		pubDate: Date;
		categories: string[];
	};
}

const allPosts = await getCollection('blog');

export function getSortedPosts(): Post[] {
	return allPosts.sort(
		(a, b) => new Date(b.data.pubDate).valueOf() - new Date(a.data.pubDate).valueOf()
	);
}

export function getPostsByCategory(category: string): Post[] {
	if (category === 'everything') return getSortedPosts();
	return getSortedPosts().filter(post => post.data.categories.includes(category));
}

export const CATEGORIES = [
	'everything',
	'design',
	'drawings',
	'readings',
	'skyfi',
	'thinkings',
	'observings',
	'teachings',
	'writings',
];
---
