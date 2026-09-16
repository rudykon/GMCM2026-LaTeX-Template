#!/usr/bin/env python3
"""Reproducible SYNTHETIC concrete-mix optimization for an academic demo.

All response coefficients, factors, and outputs are assumed/simulated. They
must not be presented as measured material properties or engineering advice.
The ``42`` in the case name is an identifier, not a concrete strength grade.

Run from any directory: python code/nsga2_demo.py --check
Only NumPy and the Python standard library are required.
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LOWER = np.array([300.0, 0.0, 0.32, 0.0])
UPPER = np.array([460.0, 0.55, 0.52, 15.0])
SEEDS = [42, 43, 44, 45, 46]
POPULATION = 80
GENERATIONS = 100
CROSSOVER_PROBABILITY = 0.9
CROSSOVER_ETA = 20.0
MUTATION_PROBABILITY = 0.25
MUTATION_ETA = 20.0
FEASIBILITY_TOLERANCE = 1e-12
MATERIALS = ["cement", "slag", "water", "sand", "coarse", "pasta"]
CARBON_FACTORS = np.array([0.86, 0.12, 0.00035, 0.005, 0.004, 0.10])
COST_FACTORS = np.array([0.50, 0.30, 0.004, 0.09, 0.075, 0.06])


def evaluate(x, absorption=0.8, pasta_carbon=0.10):
    """Vectorized model. Water includes effective water and absorbed water.

    The supplied bookkeeping convention explicitly includes total water AND
    dry pasta volume in the absolute-volume sum. It is a synthetic convention,
    not a calibrated pore-volume/saturated-surface-dry material model.
    """
    x = np.atleast_2d(np.asarray(x, dtype=float))
    binder, slag_fraction, ratio, pasta = x.T
    cement = (1.0 - slag_fraction) * binder
    slag = slag_fraction * binder
    effective_water = ratio * binder
    absorbed_water = absorption * pasta
    water = effective_water + absorbed_water
    sand = 2650.0 * (
        1.0 - 0.02 - 0.38 - cement / 3150.0 - slag / 2900.0
        - water / 1000.0 - pasta / 1350.0
    )
    coarse = np.full(len(x), 0.38 * 2700.0)
    masses = np.column_stack([cement, slag, water, sand, coarse, pasta])
    factors = CARBON_FACTORS.copy()
    factors[-1] = pasta_carbon
    carbon = masses @ factors
    cost = masses @ COST_FACTORS
    strength = (
        68.0 + 0.045 * (binder - 360.0) - 120.0 * (ratio - 0.38)
        - 20.0 * slag_fraction - pasta - 0.03 * pasta**2
    )
    slump = (
        160.0 + 800.0 * (ratio - 0.38) - 60.0 * slag_fraction
        - 1.5 * pasta + 0.1 * (binder - 360.0)
    )
    # Dimensionless sum: strength / 40 MPa, slump / 80 mm, water /
    # 80 kg/m3, sand / 500 kg/m3; zero means every constraint is satisfied.
    violations = np.column_stack([
        np.maximum(40.0 - strength, 0.0) / 40.0,
        np.maximum(140.0 - slump, 0.0) / 80.0,
        np.maximum(slump - 220.0, 0.0) / 80.0,
        np.maximum(140.0 - water, 0.0) / 80.0,
        np.maximum(water - 220.0, 0.0) / 80.0,
        np.maximum(500.0 - sand, 0.0) / 500.0,
        np.maximum(sand - 1000.0, 0.0) / 500.0,
    ])
    volume = (
        cement / 3150.0 + slag / 2900.0 + water / 1000.0
        + sand / 2650.0 + coarse / 2700.0 + pasta / 1350.0 + 0.02
    )
    return {
        "objectives": np.column_stack([carbon, cost, -strength]),
        "cv": violations.sum(axis=1),
        "violations": violations,
        "masses": masses,
        "strength": strength,
        "slump": slump,
        "effective_water": effective_water,
        "absorbed_water": absorbed_water,
        "volume": volume,
    }


def constrained_domination_matrix(objectives, cv):
    """Deb constraint domination: feasible first, then lower total violation."""
    feasible = cv <= FEASIBILITY_TOLERANCE
    objective_domination = (
        (objectives[:, None, :] <= objectives[None, :, :]).all(axis=2)
        & (objectives[:, None, :] < objectives[None, :, :]).any(axis=2)
    )
    return (
        (feasible[:, None] & ~feasible[None, :])
        | (feasible[:, None] & feasible[None, :] & objective_domination)
        | (~feasible[:, None] & ~feasible[None, :] & (cv[:, None] < cv[None, :]))
    )


def fast_non_dominated_sort(objectives, cv):
    """O(M N^2) sort using a vectorized domination adjacency matrix."""
    domination = constrained_domination_matrix(objectives, cv)
    count = domination.sum(axis=0)
    current = np.flatnonzero(count == 0)
    ranks = np.full(len(objectives), -1, dtype=int)
    fronts = []
    while len(current):
        ranks[current] = len(fronts)
        fronts.append(current)
        count -= domination[current].sum(axis=0)
        current = np.flatnonzero((count == 0) & (ranks < 0))
    if (ranks < 0).any():
        raise AssertionError("Non-dominated sorting failed")
    return fronts, ranks


def crowding_distance(objectives, front):
    distance = np.zeros(len(front))
    if len(front) <= 2:
        return np.full(len(front), np.inf)
    for objective in range(objectives.shape[1]):
        order = np.argsort(objectives[front, objective], kind="stable")
        values = objectives[front[order], objective]
        span = values[-1] - values[0]
        if span <= 0.0:
            continue
        distance[order[0]] = distance[order[-1]] = np.inf
        distance[order[1:-1]] += (values[2:] - values[:-2]) / span
    return distance


def rank_and_crowding(objectives, cv):
    fronts, ranks = fast_non_dominated_sort(objectives, cv)
    crowding = np.zeros(len(objectives))
    for front in fronts:
        crowding[front] = crowding_distance(objectives, front)
    return fronts, ranks, crowding


def tournament(rng, ranks, crowding):
    a, b = rng.integers(len(ranks), size=2)
    if ranks[a] != ranks[b]:
        return a if ranks[a] < ranks[b] else b
    if crowding[a] != crowding[b]:
        return a if crowding[a] > crowding[b] else b
    return a if rng.random() < 0.5 else b


def sbx(rng, parent_a, parent_b):
    """Bounded simulated binary crossover (Deb), distribution index 20."""
    a, b = parent_a.copy(), parent_b.copy()
    if rng.random() > CROSSOVER_PROBABILITY:
        return a, b
    power = 1.0 / (CROSSOVER_ETA + 1.0)
    for j in range(len(a)):
        if rng.random() > 0.5 or abs(a[j] - b[j]) <= 1e-14:
            continue
        y1, y2 = sorted([a[j], b[j]])
        rand = rng.random()
        beta = 1.0 + 2.0 * (y1 - LOWER[j]) / (y2 - y1)
        alpha = 2.0 - beta ** (-(CROSSOVER_ETA + 1.0))
        betaq = (
            (rand * alpha) ** power if rand <= 1.0 / alpha
            else (1.0 / (2.0 - rand * alpha)) ** power
        )
        child_a = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
        beta = 1.0 + 2.0 * (UPPER[j] - y2) / (y2 - y1)
        alpha = 2.0 - beta ** (-(CROSSOVER_ETA + 1.0))
        betaq = (
            (rand * alpha) ** power if rand <= 1.0 / alpha
            else (1.0 / (2.0 - rand * alpha)) ** power
        )
        child_b = 0.5 * ((y1 + y2) + betaq * (y2 - y1))
        child_a = np.clip(child_a, LOWER[j], UPPER[j])
        child_b = np.clip(child_b, LOWER[j], UPPER[j])
        a[j], b[j] = (
            (child_a, child_b) if rng.random() < 0.5 else (child_b, child_a)
        )
    return a, b


def polynomial_mutation(rng, x):
    result = x.copy()
    power = 1.0 / (MUTATION_ETA + 1.0)
    for j in range(len(x)):
        if rng.random() > MUTATION_PROBABILITY:
            continue
        delta1 = (result[j] - LOWER[j]) / (UPPER[j] - LOWER[j])
        delta2 = (UPPER[j] - result[j]) / (UPPER[j] - LOWER[j])
        rand = rng.random()
        if rand <= 0.5:
            value = 2.0 * rand + (1.0 - 2.0 * rand) * (1.0 - delta1) ** (MUTATION_ETA + 1.0)
            deltaq = value**power - 1.0
        else:
            value = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * (1.0 - delta2) ** (MUTATION_ETA + 1.0)
            deltaq = 1.0 - value**power
        result[j] = np.clip(result[j] + deltaq * (UPPER[j] - LOWER[j]), LOWER[j], UPPER[j])
    return result


def rank_zero(objectives):
    """Extract an unconstrained front without a large N-by-N allocation.

    Lexicographic order ensures later points cannot dominate earlier ones;
    exact duplicates are retained once. This is used on feasible points only.
    """
    order = np.lexsort(tuple(objectives[:, j] for j in reversed(range(objectives.shape[1]))))
    accepted = []
    for idx in order:
        if accepted and np.any(np.all(objectives[accepted] <= objectives[idx], axis=1)):
            continue
        accepted.append(int(idx))
    return np.asarray(accepted, dtype=int)


def feasible_front(x):
    result = evaluate(x)
    feasible = np.flatnonzero(result["cv"] <= FEASIBILITY_TOLERANCE)
    if not len(feasible):
        raise ValueError("No feasible candidates under the supplied model")
    return x[feasible[rank_zero(result["objectives"][feasible])]]


def nsga2(seed, population=POPULATION, generations=GENERATIONS):
    if population % 2:
        raise ValueError("An even population is required")
    rng = np.random.default_rng(seed)
    x = rng.uniform(LOWER, UPPER, size=(population, 4))
    result = evaluate(x)
    evaluation_count = population
    feasible_evaluations = int((result["cv"] <= FEASIBILITY_TOLERANCE).sum())
    history = []
    for generation in range(generations + 1):
        fronts, ranks, crowding = rank_and_crowding(result["objectives"], result["cv"])
        if generation % 10 == 0 or generation == generations:
            mask = result["cv"] <= FEASIBILITY_TOLERANCE
            history.append({
                "generation": generation,
                "objective_evaluations": evaluation_count,
                "feasible_population": int(mask.sum()),
                "feasible_front_count": int((mask & (ranks == 0)).sum()),
                "minimum_carbon": float(result["objectives"][mask, 0].min()) if mask.any() else None,
                "minimum_cost": float(result["objectives"][mask, 1].min()) if mask.any() else None,
                "maximum_strength": float(-result["objectives"][mask, 2].min()) if mask.any() else None,
            })
        if generation == generations:
            break
        children = []
        for _ in range(population // 2):
            a = x[tournament(rng, ranks, crowding)]
            b = x[tournament(rng, ranks, crowding)]
            c, d = sbx(rng, a, b)
            children.extend([polynomial_mutation(rng, c), polynomial_mutation(rng, d)])
        children = np.asarray(children)
        child_result = evaluate(children)
        evaluation_count += population
        feasible_evaluations += int((child_result["cv"] <= FEASIBILITY_TOLERANCE).sum())
        union_x = np.vstack([x, children])
        # Reuse parent and offspring model values: no additional objective calls.
        union_result = {key: np.concatenate([result[key], child_result[key]], axis=0) for key in result}
        union_fronts, _, _ = rank_and_crowding(union_result["objectives"], union_result["cv"])
        chosen = []
        for front in union_fronts:
            remaining = population - len(chosen)
            if len(front) <= remaining:
                chosen.extend(front.tolist())
            else:
                distances = crowding_distance(union_result["objectives"], front)
                chosen.extend(front[np.argsort(-distances, kind="stable")[:remaining]].tolist())
                break
            if len(chosen) == population:
                break
        chosen = np.asarray(chosen, dtype=int)
        x = union_x[chosen]
        result = {key: value[chosen] for key, value in union_result.items()}
    return {
        "algorithm": "NSGA-II", "seed": seed, "rng_seed": seed,
        "objective_evaluations": evaluation_count,
        "feasible_evaluations": feasible_evaluations,
        "front_x": feasible_front(x), "history": history,
    }


def random_baseline(seed, budget):
    rng_seed = 10000 + seed
    x = np.random.default_rng(rng_seed).uniform(LOWER, UPPER, size=(budget, 4))
    result = evaluate(x)
    return {
        "algorithm": "uniform_random", "seed": seed, "rng_seed": rng_seed,
        "objective_evaluations": budget,
        "feasible_evaluations": int((result["cv"] <= FEASIBILITY_TOLERANCE).sum()),
        "front_x": feasible_front(x), "history": [],
    }


def solution_record(x, solution_id=None, absorption=0.8, pasta_carbon=0.10):
    value = evaluate(x, absorption=absorption, pasta_carbon=pasta_carbon)
    obj = value["objectives"][0]
    record = {
        "solution_id": solution_id,
        "binder_kg_m3": float(x[0]), "slag_fraction": float(x[1]),
        "effective_water_binder_ratio": float(x[2]), "pasta_kg_m3": float(x[3]),
        "carbon_kgCO2e_m3": float(obj[0]), "cost_CNY_m3": float(obj[1]),
        "strength_MPa": float(-obj[2]), "slump_mm": float(value["slump"][0]),
        "effective_water_kg_m3": float(value["effective_water"][0]),
        "absorbed_water_kg_m3": float(value["absorbed_water"][0]),
        "absolute_volume_m3": float(value["volume"][0]),
        "total_mass_kg_m3": float(value["masses"][0].sum()),
        "constraint_violation": float(value["cv"][0]),
        "feasible": bool(value["cv"][0] <= FEASIBILITY_TOLERANCE),
        "constraint_margins": {
            "strength_above_40_MPa": float(-obj[2] - 40.0),
            "slump_above_140_mm": float(value["slump"][0] - 140.0),
            "slump_below_220_mm": float(220.0 - value["slump"][0]),
            "water_above_140_kg_m3": float(value["masses"][0, 2] - 140.0),
            "water_below_220_kg_m3": float(220.0 - value["masses"][0, 2]),
            "sand_above_500_kg_m3": float(value["masses"][0, 3] - 500.0),
            "sand_below_1000_kg_m3": float(1000.0 - value["masses"][0, 3]),
        },
    }
    record.update({f"{material}_kg_m3": float(mass) for material, mass in zip(MATERIALS, value["masses"][0])})
    return record


def compromise_index(front_x, ideal, span):
    normalized = (evaluate(front_x)["objectives"] - ideal) / span
    # Equal weights; sqrt(mean(square)) differs from Euclidean only by sqrt(3).
    distance = np.sqrt(np.mean(normalized**2, axis=1))
    return int(np.argmin(distance)), distance


def igd(front_objectives, reference_objectives, minimum, span):
    front = (front_objectives - minimum) / span
    reference = (reference_objectives - minimum) / span
    distances = np.linalg.norm(reference[:, None, :] - front[None, :, :], axis=2)
    return float(distances.min(axis=1).mean())


def self_checks(main_x, reference_x):
    objectives = np.array([[1., 1., 1.], [2., 2., 2.], [0., 3., 3.], [-5., -5., -5.], [-9., -9., -9.]])
    cv = np.array([0., 0., 0., 0.1, 0.2])
    fronts, ranks = fast_non_dominated_sort(objectives, cv)
    assert set(fronts[0]) == {0, 2} and np.array_equal(ranks, [0, 1, 0, 2, 3])
    assert np.array_equal(rank_zero(objectives[:3]), [2, 0])
    # A nontrivial interior point must have finite, positive crowding distance.
    distances = crowding_distance(np.array([[0., 2.], [1., 1.], [2., 0.]]), np.arange(3))
    assert np.isinf(distances[[0, 2]]).all() and distances[1] == 2.0
    values = evaluate(main_x)
    assert (values["cv"] <= FEASIBILITY_TOLERANCE).all()
    assert (main_x >= LOWER).all() and (main_x <= UPPER).all()
    assert np.allclose(values["volume"], 1., atol=2e-15, rtol=0.)
    assert not constrained_domination_matrix(values["objectives"], values["cv"]).any()
    assert evaluate(reference_x)["cv"][0] <= FEASIBILITY_TOLERANCE
    # Full main-run determinism is checked by replaying the same 8080 evaluations.
    replay = nsga2(42)["front_x"]
    assert np.array_equal(main_x, replay)
    return {
        "known_constraint_domination_example": "passed",
        "crowding_distance_example": "passed",
        "main_front_feasible_and_within_bounds": "passed",
        "main_front_pairwise_non_dominated": "passed",
        "volume_closure": "passed",
        "max_volume_error_m3": float(np.max(np.abs(values["volume"] - 1.))),
        "reference_feasible": "passed", "full_seed42_replay_deterministic": "passed",
        "replay_evaluations_excluded_from_algorithm_budget": (GENERATIONS + 1) * POPULATION,
    }


def write_csv(path, records):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run model/algorithm checks and full seed42 replay")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    budget = POPULATION * (GENERATIONS + 1)
    runs = []
    for seed in SEEDS:
        run = nsga2(seed)
        runs.append(run)
        print(f"NSGA-II seed={seed}: evaluations={budget}, front={len(run['front_x'])}", flush=True)
    baselines = [random_baseline(seed, budget) for seed in SEEDS]
    main_x = runs[0]["front_x"]
    main_objectives = evaluate(main_x)["objectives"]
    ideal = main_objectives.min(axis=0)
    span = main_objectives.max(axis=0) - ideal
    span[span == 0.] = 1.
    compromise, distances = compromise_index(main_x, ideal, span)
    selected_indices = {
        "minimum_carbon": int(np.argmin(main_objectives[:, 0])),
        "minimum_cost": int(np.argmin(main_objectives[:, 1])),
        "maximum_strength": int(np.argmin(main_objectives[:, 2])),
        "compromise": compromise,
    }
    records = [solution_record(x, f"S{i + 1:03d}") for i, x in enumerate(main_x)]
    for i, record in enumerate(records):
        record["compromise_distance"] = float(distances[i])
        record["selected_roles"] = [role for role, index in selected_indices.items() if i == index]
    union_x = np.vstack([run["front_x"] for run in runs + baselines])
    reference_front_x = feasible_front(union_x)
    reference_objectives = evaluate(reference_front_x)["objectives"]
    igd_minimum = reference_objectives.min(axis=0)
    igd_span = reference_objectives.max(axis=0) - igd_minimum
    igd_span[igd_span == 0.] = 1.
    summaries = []
    for run in runs + baselines:
        x = run["front_x"]
        obj = evaluate(x)["objectives"]
        chosen, _ = compromise_index(x, ideal, span)
        chosen_record = solution_record(x[chosen])
        summaries.append({
            "algorithm": run["algorithm"], "seed": run["seed"], "rng_seed": run["rng_seed"],
            "objective_evaluations": run["objective_evaluations"],
            "feasible_evaluations": run["feasible_evaluations"],
            "feasible_evaluation_fraction": run["feasible_evaluations"] / budget,
            "front_count": len(x),
            "minimum_carbon_kgCO2e_m3": float(obj[:, 0].min()),
            "minimum_cost_CNY_m3": float(obj[:, 1].min()),
            "maximum_strength_MPa": float(-obj[:, 2].min()),
            "igd_joint_empirical_reference": igd(obj, reference_objectives, igd_minimum, igd_span),
            "compromise_carbon_kgCO2e_m3": chosen_record["carbon_kgCO2e_m3"],
            "compromise_cost_CNY_m3": chosen_record["cost_CNY_m3"],
            "compromise_strength_MPa": chosen_record["strength_MPa"],
            "compromise_binder_kg_m3": chosen_record["binder_kg_m3"],
            "compromise_slag_fraction": chosen_record["slag_fraction"],
            "compromise_water_binder_ratio": chosen_record["effective_water_binder_ratio"],
            "compromise_pasta_kg_m3": chosen_record["pasta_kg_m3"],
        })
    reference_mix = np.array([380., 0.15, 0.42, 0.])
    reference_record = solution_record(reference_mix, "reference")
    chosen_x = main_x[compromise]
    chosen_record = records[compromise]
    carbon_delta = (reference_record["carbon_kgCO2e_m3"] - chosen_record["carbon_kgCO2e_m3"]) / reference_record["carbon_kgCO2e_m3"]
    cost_delta = (reference_record["cost_CNY_m3"] - chosen_record["cost_CNY_m3"]) / reference_record["cost_CNY_m3"]
    sensitivity = {
        "interpretation": "Post hoc bookkeeping/stress tests of fixed nominal decision variables; NOT reoptimization or validated uncertainty intervals.",
        "strength_reduction": [{
            "relative_reduction": reduction,
            "strength_MPa": chosen_record["strength_MPa"] * (1. - reduction),
            "strength_constraint_margin_MPa": chosen_record["strength_MPa"] * (1. - reduction) - 40.,
            "feasible": chosen_record["feasible"] and chosen_record["strength_MPa"] * (1. - reduction) >= 40.,
        } for reduction in [0., 0.05, 0.10]],
        "absorption": [{
            "absorption_kg_water_per_kg_dry_pasta": absorption,
            **solution_record(chosen_x, absorption=absorption),
        } for absorption in [0.4, 0.8, 1.2]],
        "absorption_convention": "B, s, effective w/b and dry pasta are fixed; extra water changes with absorption, sand is recomputed to close 1 m3. Strength and slump remain unchanged by construction of the synthetic response.",
        "pasta_carbon_factor": [{
            "pasta_carbon_kgCO2e_kg": factor,
            "carbon_kgCO2e_m3": solution_record(chosen_x, pasta_carbon=factor)["carbon_kgCO2e_m3"],
        } for factor in [0.02, 0.10, 0.50]],
    }
    aggregate = {}
    for algorithm in ["NSGA-II", "uniform_random"]:
        subset = [row for row in summaries if row["algorithm"] == algorithm]
        aggregate[algorithm] = {}
        for metric in ["compromise_carbon_kgCO2e_m3", "compromise_cost_CNY_m3", "compromise_strength_MPa", "igd_joint_empirical_reference"]:
            values = np.array([row[metric] for row in subset])
            aggregate[algorithm][metric] = {
                "minimum": float(values.min()), "maximum": float(values.max()),
                "mean": float(values.mean()), "sample_std": float(values.std(ddof=1)),
            }
    checks = self_checks(main_x, reference_mix) if args.check else {"status": "not_requested"}
    output = {
        "schema_version": 1,
        "data_status": "SYNTHETIC_ACADEMIC_DEMONSTRATION_ONLY",
        "case_identifier": "expired-pasta-42-concrete",
        "case_42_is_strength_grade": False,
        "model": {
            "decision_variables": ["binder_kg_m3", "slag_fraction", "effective_water_binder_ratio", "pasta_kg_m3"],
            "lower_bounds": LOWER.tolist(), "upper_bounds": UPPER.tolist(),
            "strength_formula": "68 + .045*(B-360) - 120*(r-.38) - 20*s - P - .03*P**2",
            "slump_formula": "160 + 800*(r-.38) - 60*s - 1.5*P + .1*(B-360)",
            "water_formula": "r*B + 0.8*P",
            "sand_formula": "2650*(1-.02-.38-(1-s)*B/3150-s*B/2900-(r*B+.8*P)/1000-P/1350)",
            "coarse_aggregate_kg_m3": 1026., "air_volume_m3": 0.02,
            "densities_kg_m3": {"cement": 3150, "slag": 2900, "water": 1000, "sand": 2650, "coarse": 2700, "pasta": 1350},
            "carbon_factors_kgCO2e_kg": dict(zip(MATERIALS, CARBON_FACTORS.tolist())),
            "cost_factors_CNY_kg": dict(zip(MATERIALS, COST_FACTORS.tolist())),
            "constraints": {"strength_MPa": [40., None], "slump_mm": [140., 220.], "water_kg_m3": [140., 220.], "sand_kg_m3": [500., 1000.]},
            "violation_normalization": {"strength_MPa": 40., "slump_mm": 80., "water_kg_m3": 80., "sand_kg_m3": 500.},
            "carbon_boundary": "Assumed material-factor accounting only, including pasta treatment; no carbonation uptake, no avoided-disposal credit, no full validated life-cycle assessment.",
            "all_response_coefficients_and_factors_are_assumed": True,
            "absolute_volume_convention": "Total mix water plus dry-pasta volume; assumed bookkeeping requiring experimental calibration for porous pasta.",
        },
        "algorithm": {
            "name": "NSGA-II", "population": POPULATION, "offspring_per_generation": POPULATION,
            "generations_after_initialization": GENERATIONS, "objective_evaluations_per_run": budget,
            "seeds": SEEDS, "main_seed": 42, "rng": "numpy.random.default_rng/PCG64",
            "crossover": "bounded SBX", "crossover_probability_per_pair": CROSSOVER_PROBABILITY,
            "crossover_probability_per_variable_conditional_on_pair": 0.5, "crossover_distribution_index": CROSSOVER_ETA,
            "mutation": "bounded polynomial", "mutation_probability_per_variable": MUTATION_PROBABILITY,
            "mutation_distribution_index": MUTATION_ETA,
            "selection": "binary tournament by constrained-front rank, crowding distance, random tie break",
            "survival": "parent+offspring elitist constrained sorting; last front truncated by crowding",
            "objectives_minimized": ["carbon_kgCO2e_m3", "cost_CNY_m3", "negative_strength_MPa"],
            "baseline": "Uniform independent sampling within identical bounds; seed=10000+paired_NSGA_seed; same 8080 evaluations; retain feasible nondominated set.",
            "evaluation_budget_note": "Counts sampled candidate evaluations only; reporting re-evaluations and optional deterministic replay are excluded. No outside archive is used in NSGA-II survival.",
        },
        "software": {"python": platform.python_version(), "numpy": np.__version__},
        "compromise_selection": {
            "formula": "argmin sqrt(mean(((f-ideal)/span)**2)); equal weights in minimized-objective coordinates",
            "normalization_source": "Feasible nondominated final population of main NSGA-II seed42; fixed for all NSGA-II and random-baseline compromise selections.",
            "ideal": ideal.tolist(), "span": span.tolist(),
            "limitation": "A preference-dependent selection tied to the sampled set; it is not a unique universal optimum.",
        },
        "quality_indicator": {
            "name": "IGD to joint empirical nondominated reference",
            "formula": "mean over reference points of min Euclidean normalized-objective distance to candidate front",
            "reference_source": "Nondominated union of five NSGA-II final fronts and five equal-budget random fronts",
            "reference_size": len(reference_front_x),
            "normalization_minimum": igd_minimum.tolist(), "normalization_span": igd_span.tolist(),
            "limitation": "The union is an empirical reference, NOT the true Pareto front. Smaller is better relative to this finite reference; there is no global optimality guarantee.",
            "reference_objectives": reference_objectives.tolist(),
        },
        "reference_mix": reference_record,
        "selected_solutions": {role: records[index] for role, index in selected_indices.items()},
        "compromise_comparison_to_reference": {
            "carbon_reduction_fraction": carbon_delta, "cost_reduction_fraction": cost_delta,
            "strength_change_MPa": chosen_record["strength_MPa"] - reference_record["strength_MPa"],
        },
        "main_pareto_front": records,
        "run_summary": summaries, "five_run_aggregate": aggregate,
        "main_run_history": runs[0]["history"], "sensitivity": sensitivity,
        "checks": checks,
    }
    csv_front = []
    for record in records:
        flat = {key: value for key, value in record.items() if key != "constraint_margins"}
        flat["selected_roles"] = ";".join(record["selected_roles"])
        flat["data_status"] = "synthetic"
        flat["seed"] = 42
        csv_front.append(flat)
    write_csv(args.output_dir / "pareto_front.csv", csv_front)
    write_csv(args.output_dir / "run_summary.csv", summaries)
    with (args.output_dir / "optimization_results.json").open("w", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"selected_solutions": output["selected_solutions"], "aggregate": aggregate, "checks": checks}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
