# AI Usage Documentation

During this project, I used Claude Opus 4.6 as an assistant in planning, code generation, and debugging. Lately, this has almost completely replaced my use of Gemini.

## How I Used AI Throughout the Project

I first talked through with Claude on how I would approach this project. This wasn't all too necessary, as there was a list of sequential instructions to go off of, but I wanted a second opinion on how I may approach the work.

Afterwards, I helped Claude run me through what I needed to have installed for this project, double-checking everything. Having an LLM to double-check these things for you is helpful, because sometimes I may be in a rush and forget things before jumping into a project. I ended up running into some issues with my interaction between MySQL and VSCode, which I was able to solve.

I then moved onto drafting up the basic schema based off the project specifications. I had Claude double check everything afterwards as a quality check.

I designed the CRUD functions for companies before having Claude do all the basic work of copying it over for jobs, applications, and contacts. I also had Claude add the job match route as per specifications during this step, as I wanted to get it out of the way.

I needed more help from Claude when building the HTML for this project. My skills when it comes to building interface or anything frontend is rather weak. I found this part of the project to be harder than any of the Flask routes.

## Prompts

I don't have any specific prompts that I found to be particularly helpful. Designing better prompts is something I want to get better at. I always try to prompt the LLM in a way that encourages it to give a thorough explanation of a task as it completes it, so I am not relying on the LLM with no knowledge of the task at hand.

Additionally, I have been using the prompt format of prompt repetition. You can read about it in this article. https://arxiv.org/abs/2512.14982

## What Worked Well

Using Claude to help me plan out my approach to the project was helpful. It's nice to be able to draft up a plan and then have it expanded upon by an LLM.

Having Claude generate repetitve syntax or foreign subjects was helpful, and was more realistic to my actual development cycle.

## Changes

I did not have to change much. There was a few errors here and there that resulted from my own poor explanations, but LLMs have become advanced enough where this is exceedingly rare.

## Lessons Learned

LLMs are useful for generating simple or repetitive code, but it's integral that I still understand the structure of the code, so I can properly explain it to others or debug it. I had a few issues I had to solve that had nothing to do with the code itself, but rather the structure.