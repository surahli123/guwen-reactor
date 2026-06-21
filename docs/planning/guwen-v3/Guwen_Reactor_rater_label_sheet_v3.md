# Guwen Reactor — Human Label Sheet v3

## 1. Recruitment message

Hi! I’m building a Kaggle capstone project that adapts public-domain Classical Chinese stories for English-speaking educators and learners.

Could you spend 20–30 minutes reviewing short pairs of English outputs? You do not need to know Chinese for the clarity task. You’ll choose which version is clearer for a classroom learner and answer one short comprehension question.

No sensitive personal data is collected. Initials are optional.

## 2. Clarity labeling task

For each pair:

1. Read Output A and Output B.
2. Choose which one better helps an English-speaking learner understand:
   - what happened;
   - why the story matters;
   - what a visual panel should show.
3. Choose: A / B / Tie.
4. Confidence: Low / Medium / High.
5. Answer the comprehension question in one sentence.

### Form columns

```text
rater_id
pair_id
choice: A / B / Tie
confidence: Low / Medium / High
comprehension_answer
optional_comment
```

## 3. Faithfulness calibration task

For bilingual/Chinese-literate checker only.

For each `(claim, source fact)` pair, label:

```text
SUPPORTED
VALID_HEDGED_INTERPRETATION
CREATIVE_SAFE_FILLER
UNSUPPORTED_DETAIL
UNSUPPORTED_MOTIVATION
CONTRADICTED
AMBIGUOUS_REVIEW
```

### Minimum target

```yaml
faithfulness_pairs_minimum: 20
faithfulness_pairs_target: 24
clarity_pairs_minimum: 6
clarity_pairs_target: 10
```

## 4. Privacy

Do not collect email addresses, real names, or demographic data. Optional initials are enough.
