# coding=utf-8

from dotenv import load_dotenv
load_dotenv()

import urllib3
urllib3.disable_warnings()

import gradio as gr
from functools import partial


##### Chat
from module.gradio_func import chg_btn_color_if_input
from module.chatbot import chat_predict_openai

##### GMZY Doc
from module.query_vdb import qa_faiss_multi_query

def gmzy_selected_vdb(_query, _radio):
    _ans, _steps = "", ""
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _pa_path = _pwd.parent
    if _radio == "gmzy":
        _db_name = str(_pa_path / "vdb" / "gmzy_bak")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    else:
        _ans = f"ERROR: not supported agent or retriever: {_radio}"
    return [_ans, _steps]

##### UI
_description = """
# Assistant
"""
with gr.Blocks(title=_description) as demo:
    dh_history = gr.State([])
    dh_user_question = gr.State("")
    gr.Markdown(_description)

    with gr.Tab(label = "光明中医"):
        az_query = gr.Textbox(label="提问", placeholder="Query", lines=10, max_lines=10, interactive=True, visible=True)
        az_radio = gr.Radio(
            ["gmzy"],
            label="https://www.gmzyjc.com/site/",
            info="",
            type="value",
            value="gmzy"
        )
        az_start_btn = gr.Button("开始", variant="secondary", visible=True)
        az_ans = gr.Textbox(label="回答", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        az_steps = gr.Textbox(label="参考信息", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        az_query.change(
            chg_btn_color_if_input,
            [az_query],
            [az_start_btn]
        )
        az_start_btn.click(
            gmzy_selected_vdb,
            [az_query, az_radio],
            [az_ans, az_steps]
        )
    
    # with gr.Tab(label = "Chat3.5"):
    #     gr.ChatInterface(
    #         fn=chat_predict_openai,
    #         submit_btn="提交",
    #         stop_btn="停止",
    #         retry_btn="🔄 重试",
    #         undo_btn="↩️ 撤消",
    #         clear_btn="🗑️ 清除",
    #     )




# from fastapi import FastAPI, Response
# import json
# app = FastAPI()

# @app.get("/health")
# def index():
#     return {"message": "active"}

# app = gr.mount_gradio_app(app, demo.queue(), path="/")
## uvicorn ui_cn_pa:app --reload


if __name__ == "__main__":

    demo.queue(concurrency_count=1).launch(
        server_name="0.0.0.0",
        server_port=8899,
        share=False,
        favicon_path="./asset/favicon_pa.png",
        # auth = ('sz','1123'),
        # auth_message= "欢迎回来！",
        ssl_verify=False,
        # ssl_keyfile="./localhost+2-key.pem",
        # ssl_certfile="./localhost+2.pem",
        # ssl_keyfile="./ssl/key.pem",
        # ssl_certfile="./ssl/cert.pem",
    )

    # import uvicorn
    # uvicorn.run(
    #     app,
    #     host="0.0.0.0",
    #     port=7788,
    #     ssl_keyfile="./localhost+2-key.pem",
    #     ssl_certfile="./localhost+2.pem",
    #     reload=True,
    #     debug=True
    # )

