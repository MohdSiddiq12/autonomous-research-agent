from graph.graph import build_graph

if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({"question": "What are the latest advances in multi-agent LLM systems?"})
    print(result)