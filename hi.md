
Hot take: I think that git is great for version-controlled code, but it's the wrong tool for documentation.

The probelm: Contributing small docs improvements to an Open Source project can quickly become a bureaucatic nightmare.

Let's get concrete by an example: Adding a Screenshot of a GeoNodes setup to Blender. Curating the example (fun part) takes 10 minutes. 
Now, contributing this example (NOT fun part) takes 2 hours, spread over multiple weeks.

Why does it take so long? 
First, we have to go though the whole git workflow (fork, clone, & open the IDE).
Adding a screenshot is particually time consuming, because there's overhead: 
Find all the right folders and files. Name the screenshot according to the repo conventions.
Write a git commit. Write a pull request message.
Wait until the docs are ready to be seen.

Now it's time for the review. For a reviewer, it's also not an easy setuation. 
The reviewer won't see how the docs look like, but just how the new docs are wired up under the hood. This can make it difficult to even find a reviewer, becuase it's not just "oh, here's the 'apply suggestion' button ", but instead the reviewer will see an abstraction of the docs that takes more cognetive load to process.



Oh and not to forget, image files are often > 100kB , so not very git friendly.

So currently, it's quite frustating to contribute docs, and I think we need better contribution-friendly open source documenation framworks. They should be more like "Google Docs Suggestions" and without a over-bureaucratic git workflow.

Do you know if something like this already exists? But getting wider adaption would also be difficult. So maybe another soltuion, like an AI agent which you tell "add this screenshot to the docs", and it will figure out the rest on it's own?
