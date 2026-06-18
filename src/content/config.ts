import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    categories: z.array(z.string()),
    image: z.string().optional(),
    author: z.string().optional(),
  }),
});

export const collections = { blog };
