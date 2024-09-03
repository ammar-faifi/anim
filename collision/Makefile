# Variables
PYTHON := python3
PIP := pip
MANIM := manim
SCENE_FILE := scene.py
SCENE_CLASS := Intro
OUTPUT_DIR := media

# Phony targets
.PHONY: all setup render clean

# Default target
all: render

# Setup the environment
setup:
	$(PIP) install manim

# Render the scene for preview
render:
	$(MANIM) -pql $(SCENE_FILE) $(SCENE_CLASS)

# Clean up generated files
clean:
	rm -rf $(OUTPUT_DIR)
	find . -type f -name "*.aux" -delete
	find . -type f -name "*.log" -delete
	find . -type f -name "*.tex" -delete
