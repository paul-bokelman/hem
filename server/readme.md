![Fathom](https://github.com/user-attachments/assets/e6f21d02-8766-419e-b8ef-ae63e918123a)

A tool to help you get a better understanding of any subject you want to learn.

### Core Features

- **Inquisitive**: Similar to talking to a curious student or peer, Fathom will continually ask questions about its lack of understanding of the subject, forcing you to thoroughly and completely explain the concept.
- **Compilation**: Talk freely, and let Fathom compile the information into an optionally user-defined structured format for later reference.

### Philosophy

There is a difference between knowing and truly understanding a concept or idea. Verbally explaining a concept allows you to elevate your unconscious understanding into a conscious state. This elevation enables critical thinking about the previously unconscious information within the realm of consciousness. Furthermore, by explaining a concept to peers, you are compelled to identify errors and inconsistencies in your own understanding. This process fosters a rich, iterative cycle that refines your perspective and cultivates a more holistic grasp of the concept or subject.

### Demo

https://github.com/user-attachments/assets/3ec84679-2a29-478d-b3c8-071fcfc53a0c

### Usage

1. Clone repo
2. Add your Anthropic API key to the .env file with the key `ANTHROPIC_API_KEY`
3. OPTIONAL: Create virtual environment with `python -m venv venv` and install packages (requirements.txt)
   - Activate environment: `source venv/bin/activate` or `venv/Scripts/activate` (Windows)
   - Install packages: `pip install -r requirements.txt`
4. OPTIONAL: Tweak 'constants' as needed, notably:
   - Add compilation templates under /templates
   - Control max audio length
   - Adjust max number of output tokens for each mode
   - Preferred input type
   - Which model is being used
5. Run with `python main.py` in selected environment or `venv/bin/python main.py`

### Additional Information

#### Compilation Templates

Custom templates use special blocks to inform the AI where to put certain information. A breakdown of the included `basic-notes.md` is as follows:

```md
# {{Header}} // Signifies the main purpose of the topic (appears once)

## {{Subsection}}... // Any subsection of the topic (appears multiples times because of '...')

- {{Point}}... // Any piece of information related to the subsection (appears multiples times because of '...')

## Questions

+Generate some thought provoking questions based on the notes+ // custom prompt that is answered and replaced by the AI
```
