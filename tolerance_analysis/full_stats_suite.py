import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin as pg
# STEP 1: LOAD (Pandas)
# simulate a study: does coffee affect test scores?
np.random.seed(42)
n = 30  # 30 students per group
no_coffee = np.random.normal(72, 10, n)
# no_coffee group: mean 72, spread 10, 30 students
yes_coffee = np.random.normal(78, 10, n)
# yes_coffee group: slightly higher mean (78)
df = pd.DataFrame({
    "score": np.concatenate([no_coffee, yes_coffee]),
    "group": ["No Coffee"] * n + ["Coffee"] * n
})
# STEP 2: WRANGLE (Pandas)
print("=== Quick Data Check ===")
print(df.groupby("group")["score"].describe())
print()
# STEP 3: COMPUTE (NumPy behind the scenes)
diff = (df[df["group"] == "Coffee"]["score"].mean()
        - df[df["group"] == "No Coffee"]["score"].mean())
print(f"Raw difference: {diff:.2f} points")
print()
# STEP 4: TEST (all three options)
# Option A: SciPy (quick check)
t, p = stats.ttest_ind(
    df[df["group"] == "Coffee"]["score"],
    df[df["group"] == "No Coffee"]["score"]
)
print(f"SciPy: t={t:.3f}, p={p:.3f}")
# Option B: Pingouin (full picture, one line)
pg_result = pg.ttest(
    df[df["group"] == "Coffee"]["score"],
    df[df["group"] == "No Coffee"]["score"]
)
print(f"\nPingouin result:")
print(pg_result.to_string())
# Option C: Statsmodels (regression framing)
model = smf.ols("score ~ group", data=df).fit()
print(f"\nStatsmodels p-value: "
      f"{model.pvalues['group[T.No Coffee]']:.4f}")
# STEP 5: VISUALIZE (Seaborn)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# left panel: box plot
sns.boxplot(data=df, x="group", y="score",
            palette="Set2", ax=axes[0])
axes[0].set_title("Score by Group")
# right panel: distribution overlap
sns.histplot(data=df, x="score", hue="group",
             kde=True, alpha=0.4, ax=axes[1])
axes[1].set_title("Score Distributions")
plt.tight_layout()
plt.savefig("coffee_study.png", dpi=150)
plt.show()