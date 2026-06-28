import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
	type: 'content',
	schema: z.object({
		title: z.string(),
		description: z.string().optional(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		image: z.string().optional(),
		imageCaption: z.string().optional(),
		categories: z.array(z.string()).default([]),
		readTime: z.number().optional(),
		views: z.number().optional(),
		likes: z.number().optional(),
		comments: z.number().optional(),
	}),
});

export const collections = { blog: blogCollection };
