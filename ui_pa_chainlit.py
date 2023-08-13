# coding=utf-8

from dotenv import load_dotenv
load_dotenv()

import urllib3
urllib3.disable_warnings()

import gradio as gr
from functools import partial


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


##### Azure Rules/Code
from module.azure_related import chat_azure_rules
from module.azure_related import llm_azure_code


##### Azure VM +
from module.query_vdb import qa_faiss_multi_query
from module.agents import agent_react_zeroshot
from module.agents import agent_openai_multifunc
from module.agents import agent_selfask_search
from module.agents import agent_react_docstore
from module.agents import agent_plan_execute

from module.tools import tools_faiss_azure_googleserp_math
from module.tools import tools_faiss_azure_googleserp
from module.tools import tools_selfask_azure
from module.tools import tools_react_docstore_azure_googleserp

# def azure_vm_selected_agent_retriever(_query, _radio):
#     _ans, _steps = "", ""
#     if _radio == "react_zeroshot":
#         _ans, _steps = agent_react_zeroshot(
#             tools_faiss_azure_googleserp_math,
#             _query
#         )
#     elif _radio == "openai_multifunc":
#         _ans, _steps = agent_openai_multifunc(
#             tools_faiss_azure_googleserp,
#             _query
#         )
#     elif _radio == "selfask_search":
#         _ans, _steps = agent_selfask_search(
#             tools_selfask_azure,
#             _query
#         )
#     elif _radio == "react_docstore":
#         _ans, _steps = agent_react_docstore(
#             tools_react_docstore_azure_googleserp,
#             _query
#         )
#     elif _radio == "plan_execute":
#         _ans, _steps = agent_plan_execute(
#             tools_faiss_azure_googleserp,
#             _query
#         )
#     elif _radio == "qa_multiquery":
#         from pathlib import Path
#         _pwd = Path(__file__).absolute()
#         _pa_path = _pwd.parent
#         _db_name = str(_pa_path / "vdb" / "azure_sql+")
#         _ans, _steps = qa_faiss_multi_query(_query, _db_name)
#     else:
#         _ans = f"ERROR: not supported agent or retriever: {_radio}"
#     return [_ans, _steps]

##### Azure Doc
from module.query_vdb import qa_faiss_multi_query

def azure_selected_vdb(_query, _radio):
    _ans, _steps = "", ""
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _pa_path = _pwd.parent
    if _radio == "vm_disk":
        _db_name = str(_pa_path / "vdb" / "azure_vm")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "sql_db":
        _db_name = str(_pa_path / "vdb" / "azure_sql_db")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "sql_mi":
        _db_name = str(_pa_path / "vdb" / "azure_sql_mi")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    elif _radio == "web_apps":
        _db_name = str(_pa_path / "vdb" / "azure_webapps")
        _ans, _steps = qa_faiss_multi_query(_query, _db_name)
    else:
        _ans = f"ERROR: not supported agent or retriever: {_radio}"
    return [_ans, _steps]

# def azure_sql_selected_agent_retriever(_query, _radio):
#     _ans, _steps = "", ""
#     if _radio == "qa_multiquery":
#         from pathlib import Path
#         _pwd = Path(__file__).absolute()
#         _pa_path = _pwd.parent
#         _db_name = str(_pa_path / "vdb" / "azure_sql+")
#         _ans, _steps = qa_faiss_multi_query(_query, _db_name)
#     else:
#         _ans = f"ERROR: not supported agent or retriever: {_radio}"
#     return [_ans, _steps]


##### Search
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


##### Auto-Code
from module.auto_programming import auto_py


##### 对话
from module.voice import audio_transcribe
from module.gradio_func import chg_btn_color_if_input
from module.gradio_func import clear_audio_microphone_if_transcribe
from module.gradio_func import transfer_input
from module.gradio_func import reset_status
from module.gradio_func import reset_textbox
from module.gradio_func import cancel_output
from module.gradio_func import delete_last_conversation
from module.chatbot import predict
from module.chatbot import retry_bot
from module.chatbot import create_chatopenai
chatagent_openai = create_chatopenai()

from module.chatbot import chat_predict_openai


##### 语音
from module.voice import txt_to_mp3


##### Chainlit iframe


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


    # with gr.Tab(label = "Auto-Task"):
    #     ao_query = gr.Textbox(label="Task", placeholder="Task", lines=5, max_lines=5, interactive=True, visible=True)
    #     ao_radio = gr.Radio(
    #         ["babyagi", "autogpt", "metaprompt", "camel", "debate"],
    #         label="Autonomous agents",
    #         info="What agent to use?",
    #         type="value",
    #         value="babyagi"
    #     )
    #     ao_start_btn = gr.Button("Start", variant="secondary", visible=True)
    #     ao_ans = gr.Textbox(label="Ans", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
    #     ao_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
    #     ao_query.change(
    #         chg_btn_color_if_input,
    #         [ao_query],
    #         [ao_start_btn]
    #     )
    #     ao_start_btn.click(
    #         auto_selected_agent,
    #         [ao_query, ao_radio],
    #         [ao_ans, ao_steps]
    #     )


    # with gr.Tab(label = "Azure Rules/Code"):
    #     ru_text = gr.Textbox(label="Text", placeholder="Text", lines=10, max_lines=10, interactive=True, visible=True)
    #     ru_rules_btn = gr.Button("Generate Rules", variant="secondary", visible=True)
    #     ru_rules = gr.Textbox(label="Rules", placeholder="...", lines=10, max_lines=10, interactive=True, visible=True)
    #     ru_rules_steps = gr.Textbox(label="Info", placeholder="...", lines=5, max_lines=5, interactive=False, visible=True)
    #     ru_code_btn = gr.Button("Generate Code", variant="secondary", visible=True)
    #     ru_code = gr.Textbox(label="Code", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
    #     ru_code_steps = gr.Textbox(label="Info", placeholder="...", lines=10, max_lines=10, interactive=False, visible=True)
    #     ru_text.change(
    #         chg_btn_color_if_input,
    #         [ru_text],
    #         [ru_rules_btn]
    #     )
    #     ru_rules_btn.click(
    #         chat_azure_rules,
    #         [ru_text],
    #         [ru_rules, ru_rules_steps]
    #     )
    #     ru_rules.change(
    #         chg_btn_color_if_input,
    #         [ru_rules],
    #         [ru_code_btn]
    #     )
    #     ru_code_btn.click(
    #         llm_azure_code,
    #         [ru_rules],
    #         [ru_code, ru_code_steps]
    #     )


    # with gr.Tab(label = "Azure VM +"):
    #     az_query = gr.Textbox(label="Query", placeholder="Query", lines=10, max_lines=10, interactive=True, visible=True)
    #     az_radio = gr.Radio(
    #         ["react_zeroshot", "openai_multifunc", "selfask_search", "react_docstore", "plan_execute", "qa_multiquery"],
    #         label="Agent & Retriever",
    #         info="What agent or retriever to use?",
    #         type="value",
    #         value="qa_multiquery"
    #     )
    #     az_start_btn = gr.Button("Start", variant="secondary", visible=True)
    #     az_ans = gr.Textbox(label="Ans", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
    #     az_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=15, interactive=False, visible=True)
    #     az_query.change(
    #         chg_btn_color_if_input,
    #         [az_query],
    #         [az_start_btn]
    #     )
    #     az_start_btn.click(
    #         azure_vm_selected_agent_retriever,
    #         [az_query, az_radio],
    #         [az_ans, az_steps]
    #     )


    with gr.Tab(label = "Azure Doc"):
        az_query = gr.Textbox(label="Query", placeholder="Query", lines=10, max_lines=10, interactive=True, visible=True)
        az_radio = gr.Radio(
            ["vm_disk", "sql_db", "sql_mi", "web_apps"],
            label="Which Azure cloud service do you want to know about?",
            info="",
            type="value",
            value="vm_disk"
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


    with gr.Tab(label = "Auto-Code"):
        # with gr.Row():
        #     openai_api_key = gr.Textbox(label="OpenAI API Key", placeholder="sk-**********, will much better if use gpt-4", lines=1, visible=True)
        # with gr.Row(equal_height=True):
        #     with gr.Column(scale=4):
        #         with gr.Row():
        #             ap_task = gr.Textbox(label="Task", placeholder="Task", lines=3, max_lines=3, interactive=True, visible=True)
        #         # with gr.Row():
        #         #     ap_ans = gr.Textbox(label="Ans", placeholder="...", lines=3, max_lines=3, interactive=False, visible=True)
        #         with gr.Row():
        #             ap_generated = gr.File(label="Generated Files", file_count="multiple", type="file", interactive=False, visible=True)
        #     ap_start_btn = gr.Button("Start", variant="secondary", visible=True)
        #     with gr.Column(scale=4):
        #         ap_steps = gr.Textbox(label="Steps", placeholder="...", lines=15, max_lines=16, interactive=False, visible=True)
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


    with gr.Tab(label = "Chat"):
        # chat_user_input = gr.Textbox(placeholder="...")
        gr.ChatInterface(
            fn=chat_predict_openai,
            # textbox=chat_user_input,
            submit_btn="提交",
            stop_btn="停止",
            retry_btn="🔄 重试",
            undo_btn="↩️ 撤消",
            clear_btn="🗑️ 清除",
        )
        # with gr.Row(equal_height=True):
        #     with gr.Column(scale=9):
        #         chat_audio_microphone = gr.Audio(source="microphone", type="filepath", label="录音", format="mp3")
        #     chat_transcribe_btn = gr.Button("转录", visible=True)
        # chat_audio_microphone.change(
        #     chg_btn_color_if_input,
        #     [chat_audio_microphone],
        #     [chat_transcribe_btn]
        # )
        # chat_transcribe_btn.click(
        #     audio_transcribe,
        #     [chat_audio_microphone],
        #     [chat_user_input],
        #     show_progress=True
        # ).then(
        #     clear_audio_microphone_if_transcribe,
        #     [],
        #     [chat_audio_microphone],
        # ).then(
        #     chg_btn_color_if_input,
        #     [chat_audio_microphone],
        #     [chat_transcribe_btn]
        # )


    with gr.Tab(label = "对话"):
        dh_chatbot = gr.Chatbot([], elem_id="chatbot", height=300)
        with gr.Row(equal_height=True):
            with gr.Column(scale=9):
                dh_user_input = gr.Textbox(show_label=False, placeholder="输入", lines=1, max_lines=1, container=False)
            dh_submit_btn = gr.Button("提问", visible=True)
        with gr.Row(equal_height=True):
            with gr.Column(scale=9):
                dh_audio_microphone = gr.Audio(source="microphone", type="filepath", label="录音", format="mp3")
            dh_transcribe_btn = gr.Button("转录", visible=True)
        with gr.Row(equal_height=True):
            dh_cancel_btn = gr.Button("🛑 停止", visible=False)
            dh_retry_btn = gr.Button("🔃 重答")
            dh_delLast_btn = gr.Button("🔙 回退", visible=False)
            dh_empty_btn = gr.Button("🧹 重启")
        with gr.Row(equal_height=True):
            status_display = gr.Markdown("🚩 Status", elem_id="status_display")
        dh_audio_microphone.change(
            chg_btn_color_if_input,
            [dh_audio_microphone],
            [dh_transcribe_btn]
        )
        dh_transcribe_btn.click(
            audio_transcribe,
            [dh_audio_microphone],
            [dh_user_input],
            show_progress=True
        ).then(
            clear_audio_microphone_if_transcribe,
            [],
            [dh_audio_microphone],
        ).then(
            chg_btn_color_if_input,
            [dh_audio_microphone],
            [dh_transcribe_btn]
        )
        dh_user_input.change(
            chg_btn_color_if_input,
            [dh_user_input],
            [dh_submit_btn]
        )
        predict_event_1 = dh_submit_btn.click(
            transfer_input,
            [dh_user_input],
            [dh_user_question, dh_user_input],
            show_progress=True
            ).then(
                partial(predict, chatagent_openai),
                [dh_user_question, dh_chatbot, dh_history],
                [dh_chatbot, dh_history, status_display],
                show_progress=True
            )
        predict_event_2 = dh_retry_btn.click(
            partial(retry_bot, chatagent_openai),
            [dh_user_input, dh_chatbot, dh_history],
            [dh_chatbot, dh_history, status_display],
            show_progress=True
        )
        dh_delLast_btn.click(
            delete_last_conversation,
            [dh_chatbot, dh_history],
            [dh_chatbot, dh_history, status_display],
            show_progress=True
        )
        dh_empty_btn.click(
            reset_textbox,
            [],
            [dh_user_input, status_display]
        )
        dh_empty_btn.click(
            reset_status,
            [],
            [dh_chatbot, dh_history, status_display],
            show_progress=True
        )
        dh_cancel_btn.click(
            cancel_output,
            [],
            [status_display],
            cancels=[predict_event_1, predict_event_2]
        )


    # with gr.Tab(label = "搜索"):
    #     with gr.Row(equal_height=True):
    #         with gr.Column(scale=5):
    #             with gr.Row():
    #                 gzl_search_ask = gr.Textbox(label="提问", placeholder="提问", lines=3, max_lines=3, interactive=True, visible=True)
    #             with gr.Row():
    #                 gzl_search_ans = gr.Textbox(label="回答", placeholder="...", lines=3, max_lines=3, interactive=False, visible=True)
    #         gzl_search_zero_btn = gr.Button("搜索 zero", variant="secondary", visible=True)
    #         gzl_search_wiki_btn = gr.Button("搜索 wiki", variant="secondary", visible=True)
    #         # gzl_search_serp_btn = gr.Button("搜索 web", variant="secondary", visible=True)
    #         with gr.Column(scale=3):
    #             gzl_search_steps = gr.Textbox(label="中间步骤", placeholder="...", lines=10, max_lines=10, interactive=False, visible=True)
    #     gzl_search_ask.change(
    #         chg_btn_color_if_input,
    #         [gzl_search_ask],
    #         [gzl_search_zero_btn]
    #     )
    #     # gzl_search_ask.change(
    #     #     chg_btn_color_if_input,
    #     #     [gzl_search_ask],
    #     #     [gzl_search_serp_btn]
    #     # )
    #     gzl_search_ask.change(
    #         chg_btn_color_if_input,
    #         [gzl_search_ask],
    #         [gzl_search_wiki_btn]
    #     )
    #     gzl_search_zero_btn.click(
    #         partial(agent_react_zeroshot, tools_faiss_azure_langchain_googleserp_math),
    #         [gzl_search_ask],
    #         [gzl_search_ans, gzl_search_steps]
    #     )
    #     # gzl_search_serp_btn.click(
    #     #     partial(agent_selfask_search, tools_selfask_search),
    #     #     [gzl_search_ask],
    #     #     [gzl_search_ans, gzl_search_steps]
    #     # )
    #     gzl_search_wiki_btn.click(
    #         partial(agent_react_docstore, tools_react_docstore_wiki),
    #         [gzl_search_ask],
    #         [gzl_search_ans, gzl_search_steps]
    #     )


    with gr.Tab(label = "语音"):
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
    # with gr.Tab(label = "工具集"):
    #     with gr.Row():
    #         openai_api_key = gr.Textbox(label="OpenAI API Key", placeholder="sk-**********", lines=1, visible=True)
    # with gr.Tab(label = "设置"):
    #     with gr.Row():
    #         openai_api_key = gr.Textbox(label="OpenAI API Key", placeholder="sk-**********", lines=1, visible=True)
    #     with gr.Row():
    #         _api_key = gr.Textbox(label="API Key", placeholder="**********", lines=1, visible=True)


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

