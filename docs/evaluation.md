# Evaluation Approach

## Goals

The evaluation verifies whether the assistant produces useful, grounded, and safe incident analysis.

## Test Dataset

Each test incident includes:

- Logs
- Metrics
- Alerts
- Deployment events
- Incident ticket
- Expected root cause
- Expected impacted services
- Expected remediation categories

## Metrics

### 1. Root Cause Accuracy

Measures whether the predicted root cause matches the expected root cause.

Scoring:

- 1.0 = Exact or semantically equivalent root cause
- 0.7 = Correct component but incomplete mechanism
- 0.4 = Related but not primary cause
- 0.0 = Incorrect cause

### 2. Evidence Grounding

Checks whether the conclusion is supported by retrieved context.

Scoring:

- 1.0 = All key claims supported
- 0.5 = Some unsupported claims
- 0.0 = Mostly hallucinated

### 3. Timeline Accuracy

Measures correctness of extracted key timestamps and events.

### 4. Remediation Usefulness

Measures whether recommended steps are actionable and relevant.

### 5. Confidence Calibration

Checks whether confidence is high for correct answers and low for uncertain cases.

### 6. Escalation Accuracy

Checks whether low-confidence or severe incidents are flagged for human review.

## Example Golden Dataset

See `src/evaluation/golden_dataset.json`.

## Manual Review

Because incident analysis has subjective elements, final evaluation includes human SRE review.
