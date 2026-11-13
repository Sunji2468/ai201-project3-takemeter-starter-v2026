# Taxonomy boundary stress test

All eight posts below are synthetic AI-written tests. They are not real
community posts and must not be added to the training dataset. These are
proposed rule applications, not evidence of human annotation agreement.

| # | Synthetic post | Proposed label | Application of the rule |
|---|---|---|---|
| 1 | I think Rust is better than C++ for everything. | `general_response` | A preference does not report actual use. |
| 2 | I moved our parser from C++ to Rust last month. I think Rust is better for everything. | `firsthand_report` | The concrete migration takes priority over the broad opinion. |
| 3 | You should move to Signal because fewer setup screens make onboarding easier. | `general_response` | Advice and a rationale, but no personal account. |
| 4 | I installed Signal on my parents' phones last Sunday; now they use it daily. You should try it. | `firsthand_report` | A reported action and outcome support the advice. |
| 5 | I will replace our chat server next month if I get approval. | `general_response` | A future plan is not an experienced event or ongoing practice. |
| 6 | Same here. Got three authentication failures this morning before logging in. | `firsthand_report` | First-person experience is clearly implied despite the missing pronoun. |
| 7 | Someone above wrote, "I lost all my files." That sounds like a reason to avoid this tool. | `general_response` | The experience belongs to a quoted writer. |
| 8 | Why does this client crash? I reproduced it twice on my laptop after installing the update. | `firsthand_report` | The question includes the writer's actual reproduction attempts. |

## Refinements made during the exercise

- Defined a concrete personal report separately from “I think” or “I prefer.”
- Included ongoing practices and clearly implied first-person reports.
- Excluded hypothetical future actions and experiences only attributed to
  quoted writers.
- Made firsthand experience take priority when it appears with advice,
  opinion, or a question.

## Remaining uncertainty

The draft needs student review on real comments. Very vague experience
claims may still be ambiguous, and the class distribution is unknown until
annotation. Do not claim the 70% balance requirement has been met yet.
