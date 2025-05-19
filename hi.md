Hot take: Git is great for version-controlled code, but it’s the wrong tool for documentation.

The problem: Contributing small doc improvements to an open source project can quickly become a bureaucratic nightmare.

A concrete example:
Let’s say you want to add a screenshot of a Geometry Nodes setup to the Blender docs.
Curating the example (the fun part) takes 10 minutes.
Contributing it (the not so fun part) takes 2 hours, spread over multiple weeks.

Why does it take so long?
You have to go through the full Git workflow: fork the repo, clone it, open the IDE.
Adding a screenshot brings extra overhead: you need to come up with a filename, create a folder, and figure out how to reference the image in the right place, often in a framework-specific way.

Also, image files are usually >100kB, not very git friendly.

Next, we have the commit message, the pull request template, and finally the review. But for the reviewer, it’s not easy either. They don’t see the docs as they’ll appear, only the underlying changes: file paths, markdown diffs. 

So what’s the solution?
Contributing to documentation should feel more like making suggestions in Google Docs, not like navigating a full dev pipeline.

After a bit of research, I found the framework docmost https://docmost.com/ that use a non-git approach.
(Docmost is the Open Source Alternative to Notion)
But switching frameworks for big projects like Blender seems unrealistic.

Another idea:
What if an AI agent could handle the overhead?
Something like:
"Hey, add this screenshot to the docs under Examples → GeoNodes. " while visiting the docs page, and the AI handels the overhead.

How can we improve the open source docs contribution experience? 
Let me know in the comment.s