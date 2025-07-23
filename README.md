# Agentic AI Editor

A CLI tool that:
1. Accepts a coding task (e.g. "something in my code is not working as intended, find and fix the bug")
2. Chooses from a set of predefined function to work on the task
   - list contents of a directory
   - read file's content
   - write to a file
   - execute python interpreter on a file
3. Repeats the step 2 until task is complete 