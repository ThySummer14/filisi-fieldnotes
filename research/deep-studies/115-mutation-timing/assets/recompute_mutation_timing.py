#!/usr/bin/env python3
"""Historical count arithmetic and an invented inheritance model.

No biological experiment, culture, selection protocol, or real mutation-rate
prediction is implemented. Python 3 standard library only. All generations
below are abstract, synchronous binary branching steps.
"""
import json
import math
import statistics


def moments(generations, p):
    """A normal parent makes one altered daughter with probability p.

    An altered parent makes two altered daughters. Total population doubles.
    If R is the altered count and N the total, conditional on R:
        R_next = 2*R + Binomial(N-R, p)
    Total expectation/variance give the two recurrences below. They include
    the fact that an already altered parent cannot make a new mutation.
    """
    n, mean, variance = 1, 0.0, 0.0
    for _ in range(generations):
        next_variance = p*(1-p)*(n-mean) + (2-p)**2*variance
        mean = (2-p)*mean + p*n
        variance = next_variance
        n *= 2
    closed_mean = n*(-math.expm1(generations*math.log1p(-p/2)))
    assert math.isclose(mean, closed_mean, rel_tol=1e-12)
    return n, mean, variance


def full_distribution(generations, p):
    """Independent check of moments by enumerating a SMALL branching model."""
    n, law = 1, {0: 1.0}
    for _ in range(generations):
        new_law = {}
        for altered, weight in law.items():
            normal = n-altered
            for new_events in range(normal+1):
                probability = (math.comb(normal, new_events)*p**new_events
                               * (1-p)**(normal-new_events))
                r = 2*altered+new_events
                new_law[r] = new_law.get(r, 0.0) + weight*probability
        law, n = new_law, 2*n
    assert math.isclose(sum(law.values()), 1, abs_tol=1e-12)
    mean = sum(r*w for r, w in law.items())
    variance = sum((r-mean)**2*w for r, w in law.items())
    return mean, variance


def sample_summary(values):
    return {"counts": values, "n": len(values), "sum": sum(values),
            "mean": statistics.mean(values),
            "sample_variance_n_minus_1": statistics.variance(values),
            "sample_variance_divided_by_mean":
                statistics.variance(values)/statistics.mean(values)}


def run():
    # Transcribed from ORIGINAL page images, not the printed summary rows.
    same = [14, 15, 13, 21, 15, 14, 26, 16, 20, 13]
    independent = [1, 0, 0, 7, 0, 303, 0, 0, 3, 48, 1, 4]
    g, p = 10, 1/1023
    n, mean, variance = moments(g, p)
    end_probability = mean/n
    early_zero = (1-p)**(n-1)
    late_zero = (1-end_probability)**n
    # This check does not merely rerun the same recurrence.
    small_mean, small_var = full_distribution(4, 0.1)
    _, check_mean, check_var = moments(4, 0.1)
    assert math.isclose(small_mean, check_mean, rel_tol=1e-12)
    assert math.isclose(small_var, check_var, rel_tol=1e-12)
    return {
        "historical_counts": {
            "source": "Luria & Delbruck (1943), original pages 503 and 504",
            "same_culture_table1_experiment_10a": sample_summary(same),
            "independent_cultures_table2_experiment_17": sample_summary(independent),
            "scope": "Counts per tested sample; samples and conditions differ. "
                     "Mean and n-1 variance are recalculated from listed counts. "
                     "The original paper's summary rows, including its sampling-"
                     "corrected table-2 variances, are NOT copied as these values."
        },
        "invented_inheritance_model": {
            "initial_cells": 1, "generations": g, "final_cells": n,
            "probability_per_normal_parent_division": p,
            "expected_final_altered_cells": mean,
            "variance_of_final_altered_count": variance,
            "probability_of_zero_altered_cells": early_zero,
            "one_event_after_generation_2_descendants_at_10": 2**(10-2),
            "one_event_after_generation_9_descendants_at_10": 2**(10-9),
            "scope": "All parameters invented; same growth, no deaths, no reverse "
                     "change, full detection. No practical biological rate implied."
        },
        "invented_change_at_endpoint_model": {
            "independent_endpoint_probability_per_cell": end_probability,
            "expected_final_altered_cells": n*end_probability,
            "variance_of_final_altered_count": n*end_probability*(1-end_probability),
            "probability_of_zero_altered_cells": late_zero,
            "scope": "Probability chosen to MATCH the first model's mean."
        },
        "zero_class_example": {
            "original_experiment": "Luria & Delbruck table 3, experiment 23",
            "zero_count": 29, "culture_count": 87,
            "estimated_mean_event_count_assuming_poisson": -math.log(29/87),
            "scope": "A mean EVENT count, not a per-division mutation rate; "
                     "requires the detection and survival assumptions described."
        },
        "birth_death_arithmetic": {
            "initial": 100, "final": 200, "deaths": 50,
            "required_binary_divisions": 200-100+50,
            "scope": "An invented count identity, not a culture prescription."
        },
        "small_model_distribution_crosscheck_passed": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
