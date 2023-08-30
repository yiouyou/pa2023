# coding=utf-8

from dotenv import load_dotenv
load_dotenv()

import urllib3
urllib3.disable_warnings()

import gradio as gr
from functools import partial


##### Azure price
from module.azure_related import azure_sku_price

##### Chat
from module.gradio_func import chg_btn_color_if_input
from module.chatbot import chat_predict_openai

##### Chainlit iframe

##### Azure Doc
from module.query_vdb import qa_faiss_multi_query

def azure_selected_vdb(_query, _radio):
    _ans, _steps = "", ""
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _pa_path = _pwd.parent
    if _radio == "app_service":
        _db_name = str(_pa_path / "vdb" / "azure_app_service")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "blob_storage":
        _db_name = str(_pa_path / "vdb" / "azure_blob_storage")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "cosmos_db":
        _db_name = str(_pa_path / "vdb" / "azure_cosmos_db")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "databricks":
        _db_name = str(_pa_path / "vdb" / "azure_databricks")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "managed_disk":
        _db_name = str(_pa_path / "vdb" / "azure_vm")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "monitor":
        _db_name = str(_pa_path / "vdb" / "azure_monitor")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "sql_db":
        _db_name = str(_pa_path / "vdb" / "azure_sql_db")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "sql_mi":
        _db_name = str(_pa_path / "vdb" / "azure_sql_mi")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "synapse":
        _db_name = str(_pa_path / "vdb" / "azure_synapse")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "vm":
        _db_name = str(_pa_path / "vdb" / "azure_vm")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "well-architected_framework":
        _db_name = str(_pa_path / "vdb" / "azure_well-architected_framework")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "cache_redis":
        _db_name = str(_pa_path / "vdb" / "azure_cache_redis")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    else:
        _ans = f"ERROR: not supported agent or retriever: {_radio}"
    return [_ans, _steps]

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

##### Search
from module.query_vdb import qa_faiss_multi_query
from module.agents import agent_react_zeroshot
from module.agents import agent_openai_multifunc
from module.agents import agent_selfask_search
from module.agents import agent_react_docstore
from module.agents import agent_plan_execute
from module.tools import tools_googleserp
from module.tools import tools_selfask_googleserp
from module.tools import tools_react_docstore_wiki

def search_selected_agent_retriever(_query, _radio):
    _ans, _steps = "", ""
    if _radio == "react_zeroshot":
        _ans, _steps = agent_react_zeroshot(
            tools_googleserp,
            _query
        )
    elif _radio == "openai_multifunc":
        _ans, _steps = agent_openai_multifunc(
            tools_googleserp,
            _query
        )
    elif _radio == "selfask_search":
        _ans, _steps = agent_selfask_search(
            tools_selfask_googleserp,
            _query
        )
    elif _radio == "react_docstore_wiki":
        _ans, _steps = agent_react_docstore(
            tools_react_docstore_wiki,
            _query
        )
    elif _radio == "plan_execute":
        _ans, _steps = agent_plan_execute(
            tools_googleserp,
            _query
        )
    else:
        _ans = f"ERROR: not supported agent or retriever: {_radio}"
    return [_ans, _steps]

##### Auto-Task
from module.auto_task import run_babyagi
from module.auto_task import run_autogpt
from module.auto_task import run_metaprompt
from module.auto_task import run_camel
from module.auto_task import run_debate

def auto_selected_agent(_task, _radio):
    _ans, _steps = "", ""
    if _radio == "babyagi":
        _ans, _steps = run_babyagi(_task)
    elif _radio == "autogpt":
        _ans, _steps = run_autogpt(_task)
    elif _radio == "metaprompt":
        _ans, _steps = run_metaprompt(_task)
    elif _radio == "camel":
        _ans, _steps = run_camel(_task)
    elif _radio == "debate":
        _ans, _steps = run_debate(_task)
    else:
        _ans = f"ERROR: not supported agent: {_radio}"
    return [_ans, _steps]

##### Auto-Code
from module.auto_programming import auto_py

##### 语音
from module.voice import txt_to_mp3

##### Photopea iframe
# Initialize Photopea with an empty, 512x512 white image. It's baked as a base64 string with URI encoding.
def get_photopea_url_params():
    return "#%7B%22resources%22:%5B%22data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIAAQMAAADOtka5AAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAANQTFRF////p8QbyAAAADZJREFUeJztwQEBAAAAgiD/r25IQAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfBuCAAAB0niJ8AAAAABJRU5ErkJggg==%22%5D%7D"


##### UI
_description = """
# Assistant
"""
with gr.Blocks(title=_description) as demo:
    dh_history = gr.State([])
    dh_user_question = gr.State("")
    gr.Markdown(_description)

    with gr.Tab(label = "Azure Price"):
        ap_query = gr.Textbox(label="Query", placeholder="Query", lines=10, max_lines=10, interactive=True, visible=True)
        ap_start_btn = gr.Button("Start", variant="secondary", visible=True)
        ap_ans = gr.Textbox(label="Ans", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        ap_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        ap_query.change(
            chg_btn_color_if_input,
            [ap_query],
            [ap_start_btn]
        )
        ap_start_btn.click(
            azure_sku_price,
            [ap_query],
            [ap_ans, ap_steps]
        )

    with gr.Tab(label = "Azure Doc"):
        az_query = gr.Textbox(label="Query", placeholder="Query", lines=10, max_lines=10, interactive=True, visible=True)
        az_radio = gr.Radio(
            ["vm", "app_service", "managed_disk", "blob_storage", "databricks", "cosmos_db", "sql_db", "sql_mi", "monitor", "synapse", "well-architected_framework", "cache_redis"],
            label="Which Azure cloud service do you want to know about?",
            info="",
            type="value",
            value="monitor"
        )
        az_start_btn = gr.Button("Start", variant="secondary", visible=True)
        az_ans = gr.Textbox(label="Ans", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        az_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        az_query.change(
            chg_btn_color_if_input,
            [az_query],
            [az_start_btn]
        )
        az_start_btn.click(
            azure_selected_vdb,
            [az_query, az_radio],
            [az_ans, az_steps]
        )

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

    with gr.Tab(label = "Chat"):
        gr.ChatInterface(
            fn=chat_predict_openai,
            submit_btn="提交",
            stop_btn="停止",
            retry_btn="🔄 重试",
            undo_btn="↩️ 撤消",
            clear_btn="🗑️ 清除",
        )

    with gr.Tab(label = "Chainlit"):
        CHAINLIT_MAIN_URL = "http://137.117.215.27:8000"
        CHAINLIT_IFRAME_ID = "chainlit-iframe"
        CHAINLIT_IFRAME_HEIGHT = 768
        CHAINLIT_IFRAME_WIDTH = "100%"
        CHAINLIT_IFRAME_LOADED_EVENT = "onChainlitLoaded"
        with gr.Row():
            # Add an iframe directly in the tab.
            gr.HTML(
                f"""<iframe id="{CHAINLIT_IFRAME_ID}" 
                src = "{CHAINLIT_MAIN_URL}"
                width = "{CHAINLIT_IFRAME_WIDTH}" 
                height = "{CHAINLIT_IFRAME_HEIGHT}"
                onload = "{CHAINLIT_IFRAME_LOADED_EVENT}(this)">"""
            )

    with gr.Tab(label = "Search"):
        sh_query = gr.Textbox(label="Query", placeholder="Query", lines=10, max_lines=10, interactive=True, visible=True)
        sh_radio = gr.Radio(
            ["react_zeroshot", "openai_multifunc", "selfask_search", "react_docstore_wiki", "plan_execute"],
            label="Agent & Retriever",
            info="What agent or retriever to use?",
            type="value",
            value="react_zeroshot"
        )
        sh_start_btn = gr.Button("Start", variant="secondary", visible=True)
        sh_ans = gr.Textbox(label="Ans", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        sh_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        sh_query.change(
            chg_btn_color_if_input,
            [sh_query],
            [sh_start_btn]
        )
        sh_start_btn.click(
            search_selected_agent_retriever,
            [sh_query, sh_radio],
            [sh_ans, sh_steps]
        )

    with gr.Tab(label = "Auto-Task"):
        ao_query = gr.Textbox(label="Task", placeholder="Task", lines=5, max_lines=5, interactive=True, visible=True)
        ao_radio = gr.Radio(
            ["babyagi", "autogpt", "metaprompt", "camel", "debate"],
            label="Autonomous agents",
            info="What agent to use?",
            type="value",
            value="babyagi"
        )
        ao_start_btn = gr.Button("Start", variant="secondary", visible=True)
        ao_ans = gr.Textbox(label="Ans", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        ao_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        ao_query.change(
            chg_btn_color_if_input,
            [ao_query],
            [ao_start_btn]
        )
        ao_start_btn.click(
            auto_selected_agent,
            [ao_query, ao_radio],
            [ao_ans, ao_steps]
        )

    with gr.Tab(label = "Auto-Code"):
        ap_task = gr.Textbox(label="Task", placeholder="Task", lines=10, max_lines=10, interactive=True, visible=True)
        ap_start_btn = gr.Button("Start", variant="secondary", visible=True)
        ap_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
        ap_generated = gr.File(label="Generated Files", file_count="multiple", type="file", interactive=False, visible=True)
        ap_task.change(
            chg_btn_color_if_input,
            [ap_task],
            [ap_start_btn]
        )
        ap_start_btn.click(
            auto_py,
            [ap_task],
            [ap_generated, ap_steps]
        )

    with gr.Tab(label = "转语音"):
        with gr.Row(equal_height=True):
            with gr.Column(scale=6):
                yy_txt = gr.Textbox(label="输入文字", placeholder="input text", lines=5, max_lines=5, interactive=True, visible=True)
            yy_btn = gr.Button("转换", variant="secondary", visible=True)
            with gr.Column(scale=3):
                yy_mp3 = gr.Audio(label="生成语音", visible=True)
        yy_txt.change(
            chg_btn_color_if_input,
            [yy_txt],
            [yy_btn]
        )
        yy_btn.click(
            txt_to_mp3,
            [yy_txt],
            [yy_mp3]
        )

    with gr.Tab(label = "Photopea"):
        PHOTOPEA_MAIN_URL = "https://www.photopea.com/"
        PHOTOPEA_IFRAME_ID = "photopea-iframe"
        PHOTOPEA_IFRAME_HEIGHT = 768
        PHOTOPEA_IFRAME_WIDTH = "100%"
        PHOTOPEA_IFRAME_LOADED_EVENT = "onPhotopeaLoaded"
        with gr.Row():
            # Add an iframe directly in the tab.
            gr.HTML(
                f"""<iframe id="{PHOTOPEA_IFRAME_ID}" 
                src = "{PHOTOPEA_MAIN_URL}{get_photopea_url_params()}" 
                width = "{PHOTOPEA_IFRAME_WIDTH}" 
                height = "{PHOTOPEA_IFRAME_HEIGHT}"
                onload = "{PHOTOPEA_IFRAME_LOADED_EVENT}(this)">"""
            )




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
        server_port=7788,
        share=False,
        favicon_path="./asset/favicon_pa.png",
        # auth = ('sz','1123'),
        # auth_message= "欢迎回来！",
        ssl_verify=False,
        # ssl_keyfile="./localhost+2-key.pem",
        # ssl_certfile="./localhost+2.pem",
        ssl_keyfile="./ssl/key.pem",
        ssl_certfile="./ssl/cert.pem",
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

