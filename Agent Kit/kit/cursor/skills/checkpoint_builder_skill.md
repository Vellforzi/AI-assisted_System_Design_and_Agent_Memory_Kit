# Checkpoint Builder Skill

Purpose: create compact checkpoints before context becomes risky.

Checkpoint rules:

- checkpoint after meaningful work;
- checkpoint before a long next step;
- checkpoint before switching task;
- checkpoint before Project Map update if the chat is long;
- checkpoint when context compaction is suspected.

Required output fields:

- checkpoint_id;
- task;
- status;
- completed;
- changed_files;
- verification;
- decisions;
- risks;
- open_questions;
- next_safe_step;
- evidence;
- Project Map delta proposal;
- Eval trigger.
