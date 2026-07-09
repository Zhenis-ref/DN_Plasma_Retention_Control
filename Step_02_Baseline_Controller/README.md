# Step 02 — Baseline Controller

Назначение шага: проверить простой реактивный baseline-контроллер в HL-2A-informed reduced-order среде.

Baseline не использует CCE, lookahead, перебор действий или DN-оптимизацию.

Он реагирует только на наблюдаемые индикаторы:

```text
R1 = D - N
R2 = D / (N + epsilon)
D
N
E
```

Запуск из папки `Step_02_Baseline_Controller`:

```powershell
python experiments\run_baseline_test.py
```

Ожидаемый результат:

```text
collapse должен быть предотвращён или отложен по сравнению с open-loop Step 01
```

Но baseline может расходовать ресурс E грубо и неэффективно.
