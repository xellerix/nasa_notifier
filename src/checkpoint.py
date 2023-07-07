#!/usr/bin/env python3

checkpoint_file = 'data/checkpoint.txt'

# Save the checkpoint ID to a file
def save_checkpoint(checkpoint_id):
    with open(checkpoint_file, 'w') as file:
        file.write(checkpoint_id)

# Load the checkpoint ID from a file
def load_checkpoint():
    try:
        with open(checkpoint_file, 'r') as file:
            checkpoint_id = file.read().strip()
        return checkpoint_id
    except FileNotFoundError:
        return None
