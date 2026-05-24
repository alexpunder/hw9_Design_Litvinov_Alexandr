import numpy as np
from scipy import stats

np.random.seed(42)

current_accuracy = np.random.normal(
    loc=0.95,
    scale=0.02,
    size=1000,
)

new_accuracy = np.random.normal(
    loc=0.80,
    scale=0.02,
    size=1000,
)

ci_curr = np.percentile(
    current_accuracy,
    [2.5, 97.5],
)

ci_new = np.percentile(
    new_accuracy,
    [2.5, 97.5],
)

print("Текущая точность:")
print(f"Среднее = {current_accuracy.mean():.4f}")
print(f"95% CI = [{ci_curr[0]:.4f}, {ci_curr[1]:.4f}]")

print("\nНовая точность:")
print(f"Среднее = {new_accuracy.mean():.4f}")
print(f"95% CI = [{ci_new[0]:.4f}, {ci_new[1]:.4f}]")

_, p_curr = stats.shapiro(current_accuracy)
_, p_new = stats.shapiro(new_accuracy)

print(f"\nShapiro p-value historical: {p_curr:.4f}")
print(f"Shapiro p-value new: {p_new:.4f}")

alpha = 0.05

if p_curr > alpha and p_new > alpha:
    print("\Данные нормально распределены. Используем t-test")
    stat, p_value = stats.ttest_ind(
        current_accuracy,
        new_accuracy,
    )
else:
    print("\Данные распределены ненормально. Используем U-test")
    stat, p_value = stats.mannwhitneyu(
        current_accuracy,
        new_accuracy
    )

print(f"\np-value = {p_value:.4e}")

SLO = 0.85

if (
    p_value < alpha
    and new_accuracy.mean() < SLO
):

    print(
        "\nОбнаружена статистически значимая деградация. "
        "\nSLO нарушено - требуется переобучение."
    )
else:
    print("\nДеградация статистически незначительна.")
