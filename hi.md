Hot take: Git is great for version-controlled code, but it’s the wrong tool for documentation.

The problem: Contributing small doc improvements to an open source project can quickly become a bureaucratic nightmare.

A concrete example:
Let’s say you want to add a screenshot of a Geometry Nodes setup to the Blender docs.
Curating the example (the fun part) takes 10 minutes.
Contributing it (the not so fun part) takes 2 hours, spread over multiple weeks.

Why does it take so long?
You have to go through the entire Git workflow: fork, clone, open the IDE.
Adding a screenshot introduces even more overhead: you need to come up with a filename, create a folder, and figure out how to reference the image in the right place, often in a framework-specific way.

Also, image files are often >100kB, not very git friendly.

Then comes the commit message, the pull request template, and finally the review. But for the reviewer, it’s not easy either. They don’t see the docs as they’ll appear, only the underlying changes: file paths, markdown diffs. 

So what’s the solution?
I think that contributing docs should feel more like suggesting edits in Google Docs, not navigating a full development pipeline.
After a bit of research, I found frameworks like docmost https://docmost.com/. 
But it would be difficult to switch a full framework for already existing docs, so maybe another idea.
what if an AI agent could handle the overhead? Something like:
“Hey, add this screenshot to the docs under ‘Examples → GeoNodes’.”  And it just does the right thing.
