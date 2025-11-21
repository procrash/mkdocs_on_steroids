#!/bin/bash
export PYTHONPATH="/home/user/mkdocs_on_steroids/plugins/mkdocs-llm-autodoc:/home/user/mkdocs_on_steroids/plugins/mkdocs-chatbot:$PYTHONPATH"
cd /home/user/mkdocs_on_steroids
python -m mkdocs serve -a 0.0.0.0:8005
