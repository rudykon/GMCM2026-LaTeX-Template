"""Synthetic least-squares example used in the template."""
from math import sqrt


def fit_line(x, y):
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Need at least two paired observations.")
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    sxx = sum((xi - x_mean) ** 2 for xi in x)
    if sxx == 0:
        raise ValueError("Input values must not all be equal.")
    slope = sum(
        (xi - x_mean) * (yi - y_mean)
        for xi, yi in zip(x, y)
    ) / sxx
    intercept = y_mean - slope * x_mean
    fitted = [intercept + slope * xi for xi in x]
    rmse = sqrt(sum(
        (yi - pi) ** 2 for yi, pi in zip(y, fitted)
    ) / len(y))
    return intercept, slope, fitted, rmse


if __name__ == "__main__":
    x = [1, 2, 3, 4, 5]
    y = [1.9, 4.1, 5.8, 8.2, 10.0]
    intercept, slope, fitted, rmse = fit_line(x, y)
    print(f"intercept={intercept:.4f}, slope={slope:.4f}")
    print("fitted:", ", ".join(f"{p:.2f}" for p in fitted))
    print(f"RMSE={rmse:.4f}")
