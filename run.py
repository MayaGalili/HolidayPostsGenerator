#!/usr/bin/env python3
"""
Simple script to run the Holiday Posts Generator app.
This bypasses the package installation and runs the app directly.
"""

if __name__ == "__main__":
    from app import Me
    import gradio as gr
    
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()

