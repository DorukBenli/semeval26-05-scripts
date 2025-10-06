# semeval26-05-scripts
(WIP) Some scripts for Semeval 2026 Task 5. More baseline predictions, format checker and link to submission website will be added soon.

# How to evaluate predictions

First, remember to install the requirements.

To evaluate a prediction, please bring it in line with the "predictions/random_predictions_dev.jsonl" file.
Each prediction must be in its own line. The "id" key corresponds to the keys of the samples in the gold data ("0", "1", etc).
The prediction key should be an integer between 1 and 5.

Once you prepare your prediction data, call the evaluation script like this:

```
python evaluate.py <predictions/your_predictions.jsonl> <train/dev/test>
```

Test set is yet unreleased, so you can only test on train and dev sets for now.