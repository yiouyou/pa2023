def chg_btn_color_if_input(_input):
    import gradio as gr
    if _input:
        return gr.update(variant="primary")
    else:
        return gr.update(variant="secondary")

def chg_btn_color_if_transcribe():
    import gradio as gr
    return gr.update(variant="primary")

def clear_audio_microphone_if_transcribe():
    import gradio as gr
    return gr.update(value=None)

