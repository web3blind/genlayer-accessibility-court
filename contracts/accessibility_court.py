# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class AccessibilityCourt(gl.Contract):
    """Adjudicates whether accessibility evidence supports a claim.

    Intended use: an external accessibility auditor collects evidence first
    (URL, WCAG issues, score, manual checks, proof/report hash). GenLayer then
    judges the claim against that evidence, rather than replacing the auditor.
    """

    last_case_id: str
    last_decision_json: str

    def __init__(self):
        self.last_case_id = ""
        self.last_decision_json = "{}"

    @gl.public.write
    def adjudicate_claim(self, case_id: str, evidence_json: str, claim: str) -> typing.Any:
        def leader_fn() -> dict:
            prompt = f"""
You are an accessibility adjudicator. Decide whether the claim is supported by the evidence.

Return a JSON object with exactly these keys:
- verdict: one of "supported", "partially_supported", "not_supported", "insufficient_evidence"
- confidence: integer from 0 to 100
- rationale_en: short English explanation, max 800 characters
- key_findings: array of 1 to 6 short strings
- missing_evidence: array of short strings; empty if nothing important is missing

Rules:
- Do not invent facts outside the evidence.
- Treat WCAG failures, inaccessible controls, missing labels, keyboard traps, and low score as negative evidence.
- A claim like "site is accessible" requires strong positive evidence and no critical blockers.
- If the evidence only contains automated checks, mark manual uncertainty in missing_evidence.

Claim: {claim}
Evidence JSON: {evidence_json}
"""
            result = gl.nondet.exec_prompt(prompt, response_format="json")
            if not isinstance(result, dict):
                raise gl.UserError(f"LLM returned non-dict: {type(result)}")
            return result

        def validator_fn(leader_result: gl.vm.Result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False
            data = leader_result.calldata
            if not isinstance(data, dict):
                return False
            verdict = data.get("verdict")
            confidence = data.get("confidence")
            return (
                verdict in ("supported", "partially_supported", "not_supported", "insufficient_evidence")
                and isinstance(confidence, int)
                and 0 <= confidence <= 100
                and isinstance(data.get("rationale_en"), str)
                and 0 < len(data.get("rationale_en", "")) <= 1000
                and isinstance(data.get("key_findings"), list)
                and 1 <= len(data.get("key_findings", [])) <= 6
                and isinstance(data.get("missing_evidence"), list)
            )

        decision = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_case_id = case_id
        self.last_decision_json = json.dumps(decision, ensure_ascii=False)

    @gl.public.view
    def get_last_case_id(self) -> str:
        return self.last_case_id

    @gl.public.view
    def get_last_decision_json(self) -> str:
        return self.last_decision_json
