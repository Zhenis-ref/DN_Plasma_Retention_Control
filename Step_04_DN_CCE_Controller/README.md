# Step 04 — DN/CCE Controller

Назначение шага: проверить DN/CCE-контроллер как сжатую альтернативу brute-force.

Сравниваются четыре режима:

```text
open_loop
baseline
brute_force
dn_cce
```

DN/CCE не перебирает все 61 действие. Он формирует компактный набор кандидатов на основе DN-риска:

```text
R1 = D - N
R2 = D / (N + epsilon)
dD/dt
risk_zone
E
```

Запуск:

```powershell
python experiments\run_dn_cce_test.py
```

Критерий успеха Step 04:

```text
collapse = False
качество близко к brute_force
evals значительно меньше brute_force
```


Fix note: run_controller correctly passes PlasmaState to BaselineController and PlasmaEnvironment to lookahead controllers.
