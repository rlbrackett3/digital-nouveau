import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: 'src/content/blog' }),
  schema: z.object({
    title: z.string().default('untitled'),
    description: z.string().default(''),
    pubDate: z.coerce.date().default(new Date('2020-01-01')),
    categories: z.array(z.string()).default(['thinkings']),
    image: z.string().optional(),
    author: z.string().optional(),
    views: z.number().default(0),
    likes: z.number().default(0),
    comments: z.number().default(0),
  }),
});

export const collections = { blog };