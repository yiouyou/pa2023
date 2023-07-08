def auto_py(_task):
    import os
    import json
    import shutil

    from . import _steps
    from ._ai import AI
    from ._db import DB, DBs
    from ._steps import STEPS
    from pathlib import Path

    delete_existing = True
    project_path = "tmp/project"
    model = "gpt-3.5-turbo-0613"
    temperature = 0.1
    steps_config = _steps.Config.MIN
    run_prefix = ""

    input_path = Path(project_path).absolute()
    memory_path = input_path / f"{run_prefix}memory"
    workspace_path = input_path / f"{run_prefix}workspace"
    # print(input_path)
    # print(memory_path)
    # print(workspace_path)

    if delete_existing:
        # Delete files and subdirectories in paths
        shutil.rmtree(memory_path, ignore_errors=True)
        shutil.rmtree(workspace_path, ignore_errors=True)

    ai = AI(
        model=model,
        temperature=temperature
    )

    dbs = DBs(
        memory=DB(memory_path),
        logs=DB(memory_path / "logs"),
        input=DB(input_path),
        workspace=DB(workspace_path),
        preprompts=DB(Path(__file__).parent / "preprompts"),
    )

    ##### write _task to input_path/prompt
    _prompt_path = input_path / f"prompt"
    _prompt_path.write_text(_task, encoding="utf-8")

    for step in STEPS[steps_config]:
        messages = step(ai, dbs)
        dbs.logs[step.__name__] = json.dumps(messages, ensure_ascii=False)

    _generated = ""
    _generated_files = []
    for (dirpath, dirnames, filenames) in os.walk(workspace_path):
        for filename in filenames:
            if filename.endswith(('.txt', '.py')):
                _generated_files.append(os.path.join(dirpath, filename))
    # print(_generated_files)
    import gradio as gr
    _generated = gr.update(value=_generated_files)

    _step = ""
    _all_output_path = workspace_path / f"all_output.txt"
    _step = _all_output_path.read_text()

    return [_generated, _step]
    

if __name__ == "__main__":
    auto_py("Create a file organizer CLI tool in Python that sorts files in a directory based on their file types (e.g., images, documents, audio) and moves them into corresponding folders.")

