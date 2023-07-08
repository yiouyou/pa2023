import gradio

with gradio.Blocks() as interface:
    recorder = gradio.Audio(source='microphone', type='filepath', visible=False)
    action_btn = gradio.Button('Start')
    def next_line(action, _):
        if action == 'Start':
            return {action_btn: 'Next', recorder: gradio.update(visible=True)}
        else:
            return {action_btn: 'Done', recorder: gradio.update(visible=False)}
    action_btn.click(next_line, inputs=[action_btn, recorder], outputs=[action_btn, recorder])
interface.launch(server_name="0.0.0.0", server_port=7788, share=False, favicon_path="./asset/favicon_pa.png")
