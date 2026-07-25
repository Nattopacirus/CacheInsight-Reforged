# Rule: Delivery Checklist (API vs UI Integrity)
Before completing any task and presenting it to the user, you MUST verify the following:
1. **Type mismatches:** Ensure there is no type mismatch between the Backend and Frontend (e.g., String from DOM vs Number from DB). If a loose or strict equality check is used, ensure the types match perfectly via casting.
2. **JSON Response Completeness:** Ensure that the JSON response payload from the Backend contains all the fields that the UI expects and uses.
If any risks or mismatches are found, YOU MUST FIX THEM IMMEDIATELY before concluding the implementation.
