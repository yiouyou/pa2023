def transfer_input(_user_input):
    import gradio as gr
    return _user_input, gr.update(value="", interactive=True)

def reset_status():
    return [], [], "🚩 Reset Status Done"

def reset_textbox():
    import gradio as gr
    return gr.update(value="", interactive=True), "🚩 Reset Textbox Done"

def cancel_output():
    return "🚩 Stop Done"

def delete_last_conversation(_chatbot, _history):
    if len(_chatbot) > 0:
        _chatbot.pop()
    if len(_history) > 0:
        _history.pop()
    return _chatbot, _history, "🚩 Delete Done"

