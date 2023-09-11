import time
import requests
import streamlit as st
import dstack

run_name = "streamlit-llama"

if len(st.session_state) == 0:
    st.session_state.deploying = False
    st.session_state.started = False
    st.session_state.client = dstack.Client.from_config(".")
    st.session_state.run = None
    st.session_state.error = None
    try:
        with st.spinner("Connecting to `dstack`..."):
            run = st.session_state.client.runs.get(run_name)
            if run and run.status().is_unfinished():
                st.session_state.run = run
                st.session_state.deploying = True
    except dstack.api.hub.errors.HubClientError:
        st.info("Can't connect to `dstack`", icon="💤")
        st.text("Make sure the `dstack` server is up:")
        st.code(
            """
                dstack start
            """,
            language="shell",
        )
        st.stop()


def trigger_llm_deployment():
    st.session_state.deploying = True
    st.session_state.error = None


def trigget_llm_undeployment():
    st.session_state.run.stop()
    st.session_state.deploying = False
    st.session_state.started = False
    st.session_state.run = None


with st.sidebar:
    model_option = st.selectbox(
        "Choose an LLM to deploy",
        (
            "Llama-2-13B-chat-GPTQ (GPU 20GB)",
            "Llama-2-70B-chat-GPTQ (GPU 40GB)",
        ),
        disabled=st.session_state.deploying or st.session_state.started,
    )
    if model_option == "Llama-2-13B-chat-GPTQ (GPU 20GB)":
        model_id = "TheBloke/Llama-2-13B-chat-GPTQ"
    elif model_option == "Llama-2-70B-chat-GPTQ (GPU 40GB)":
        model_id = "TheBloke/Llama-2-70B-chat-GPTQ"
    if not st.session_state.deploying:
        st.button("Deploy", on_click=trigger_llm_deployment, type="primary")


def get_configuration():
    return dstack.Task(
        image="ghcr.io/huggingface/text-generation-inference:latest",
        env={"MODEL_ID": model_id},
        commands=[
            "text-generation-launcher --trust-remote-code --quantize gptq",
        ],
        ports=["8080:80"],
    )


def get_resources():
    if model_id == "TheBloke/Llama-2-13B-chat-GPTQ":
        gpu_memory = "20GB"
    elif model_id == "TheBloke/Llama-2-70B-chat-GPTQ":
        gpu_memory = "40GB"
    return dstack.Resources(gpu=dstack.GPU(memory=gpu_memory))


if st.session_state.error:
    with st.sidebar:
        st.error(st.session_state)


if st.session_state.deploying:
    with st.sidebar:
        with st.status(
            "Deploying the LLM..."
            if not st.session_state.run
            else "Attaching to the LLM...",
            expanded=True,
        ) as status:
            if not st.session_state.run:
                st.write("Provisioning...")
                try:
                    run = st.session_state.client.runs.submit(
                        configuration=get_configuration(),
                        run_name=run_name,
                        resources=get_resources(),
                    )
                    st.session_state.run = run
                    st.write("Attaching to the LLM...")
                except Exception as e:
                    if hasattr(e, "message"):
                        st.session_state.error = e.message
                    else:
                        raise e
                    st.session_state.deploying = False
                    st.experimental_rerun()
            if not st.session_state.error:
                placeholder = st.sidebar.empty()
                placeholder.button(
                    "Cancel",
                    type="primary",
                    key="cancel_starting",
                    on_click=trigget_llm_undeployment,
                )
                try:
                    st.session_state.run.attach()
                except dstack.PortUsedError:
                    pass
                while True:
                    time.sleep(0.5)
                    try:
                        r = requests.get("http://localhost:8080/health")
                        if r.status_code == 200:
                            break
                        elif st.session_state.run.status().is_finished():
                            st.session_state.error = "Failed or interrupted"
                            st.session_state.deploying = False
                            st.experimental_rerun()
                            break
                    except Exception:
                        pass
                if not st.session_state.error:
                    status.update(
                        label="The LLM is ready!", state="complete", expanded=False
                    )
                    st.session_state.deploying = False
                    st.session_state.started = True
                    placeholder.empty()

with st.sidebar:
    if st.session_state.started:
        st.button(
            "Undeploy",
            type="primary",
            key="stop",
            on_click=trigget_llm_undeployment,
        )

if not st.session_state.started:
    st.info("The LLM is down.", icon="😴")
else:
    st.info("The LLM is up!", icon="🙌")
    st.markdown(
        "Feel to access the LLM at at [`http://127.0.0.1:8080`](http://127.0.0.1:8080/docs)"
    )
    st.code(
        """curl 127.0.0.1:8080 \\
    -X POST \\
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \\
    -H 'Content-Type: application/json'
            """,
        language="shell",
    )
    st.markdown(
        "Make sure to use the Llama 2 Chat prompt [format](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/discussions/3)."
    )
