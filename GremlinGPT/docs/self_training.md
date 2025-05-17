# Self-Training Loop

GremlinGPT watches logs and retrains itself using failures.

### Trigger System

- Uses `watchdog` to monitor `data/logs/`
- Triggered if new lines include:
  - FAIL
  - LOW_CONF
  - INVALID

### Mutation Engine

1. Raw failures extracted from logs
2. Mutation performed via pattern replacement
3. NLP retraining initiated every 15 minutes

### Integration

- Mutated data embedded and tagged
- New memory used in future inference
- Continuous feedback loop

### Key Files

- `generate_dataset.py`: Gathers logs
- `mutation_engine.py`: Applies transformations
- `feedback_loop.py`: Pushes embeddings to memory
