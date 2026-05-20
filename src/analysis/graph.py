import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

from src.analysis.schemas import RCAState
from src.analysis.retriever import IncidentRetriever, format_context
from src.analysis.anomaly_detector import detect_anomalies
from src.analysis.prompts import (
    SUMMARY_PROMPT,
    TIMELINE_PROMPT,
    ROOT_CAUSE_PROMPT,
    REMEDIATION_PROMPT,
    FINAL_OUTPUT_PROMPT,
)


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


def retrieve_context_node(state: RCAState) -> RCAState:
    
    retriever = IncidentRetriever()

    context = retriever.retrieve_incident_context(
        incident_id=state["incident_id"],
        query=state.get("user_query", "Analyze this production incident"),
    )

    return {
        **state,
        "retrieved_context": context,
    }


def summarize_node(state: RCAState) -> RCAState:
    context = format_context(state["retrieved_context"])
    prompt = SUMMARY_PROMPT.format(context=context)

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        **state,
        "summary": response.content,
    }


def timeline_node(state: RCAState) -> RCAState:
    context = format_context(state["retrieved_context"])
    prompt = TIMELINE_PROMPT.format(context=context)

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        timeline = json.loads(response.content)
    except Exception:
        timeline = [
            {
                "timestamp": "unknown",
                "event": response.content,
                "source": "llm",
            }
        ]

    return {
        **state,
        "timeline": timeline,
    }


def anomaly_node(state: RCAState) -> RCAState:
    anomalies = detect_anomalies(state["retrieved_context"])

    return {
        **state,
        "anomalies": anomalies,
    }


def root_cause_node(state: RCAState) -> RCAState:
    context = format_context(state["retrieved_context"])

    prompt = ROOT_CAUSE_PROMPT.format(
        incident_id=state["incident_id"],
        summary=state["summary"],
        timeline=json.dumps(state["timeline"], indent=2),
        anomalies=json.dumps(state["anomalies"], indent=2),
        context=context,
    )

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        **state,
        "probable_root_cause": response.content,
    }


def remediation_node(state: RCAState) -> RCAState:
    prompt = REMEDIATION_PROMPT.format(
        root_cause=state["probable_root_cause"],
        summary=state["summary"],
        anomalies=json.dumps(state["anomalies"], indent=2),
    )

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        **state,
        "remediation_steps": [
            step.strip("- ").strip()
            for step in response.content.split("\n")
            if step.strip()
        ],
    }


def final_output_node(state: RCAState) -> RCAState:
    prompt = FINAL_OUTPUT_PROMPT.format(
        incident_id=state["incident_id"],
        summary=state["summary"],
        timeline=json.dumps(state["timeline"], indent=2),
        anomalies=json.dumps(state["anomalies"], indent=2),
        root_cause=state["probable_root_cause"],
        remediation=json.dumps(state["remediation_steps"], indent=2),
    )

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        final_result = json.loads(response.content)
    except Exception:
        final_result = {
            "incident_id": state["incident_id"],
            "severity": "UNKNOWN",
            "summary": state["summary"],
            "timeline": state["timeline"],
            "anomalies": state["anomalies"],
            "probable_root_cause": state["probable_root_cause"],
            "remediation_steps": state["remediation_steps"],
            "confidence": 0.5,
            "needs_human_review": True,
            "reasoning": "Final JSON parsing failed. Human review required.",
        }

    return {
        **state,
        "final_result": final_result,
    }


def build_rca_graph():
    graph = StateGraph(RCAState)

    graph.add_node("retrieve_context", retrieve_context_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("timeline", timeline_node)
    graph.add_node("anomaly_detection", anomaly_node)
    graph.add_node("root_cause", root_cause_node)
    graph.add_node("remediation", remediation_node)
    graph.add_node("final_output", final_output_node)

    graph.set_entry_point("retrieve_context")

    graph.add_edge("retrieve_context", "summarize")
    graph.add_edge("summarize", "timeline")
    graph.add_edge("timeline", "anomaly_detection")
    graph.add_edge("anomaly_detection", "root_cause")
    graph.add_edge("root_cause", "remediation")
    graph.add_edge("remediation", "final_output")
    graph.add_edge("final_output", END)

    return graph.compile()
