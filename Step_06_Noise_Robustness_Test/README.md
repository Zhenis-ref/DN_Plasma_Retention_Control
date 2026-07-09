# Step 06 — Noise & Robustness Test

Назначение шага: проверить, сохраняется ли преимущество DN/CCE при шуме измерений.

Сравниваются:

```text
baseline
brute_force
dn_cce
```

Уровни шума:

```text
0%
5%
10%
20%
```

Шум добавляется только к наблюдаемым координатам контроллера:

```text
N_obs
D_obs
mode_amp_obs
E_obs
R1_obs
R2_obs
dD_dt_obs
```

Сама среда остаётся истинной. Это моделирует ошибку измерений, а не изменение физики среды.

Запуск:

```powershell
python experiments\run_noise_robustness_test.py
```

Результаты сохраняются:

```text
outputs/tables/noise_summary.csv
outputs/plots/noise_final_E.png
outputs/plots/noise_total_u.png
outputs/plots/noise_evals.png
outputs/plots/noise_collapse.png
```
