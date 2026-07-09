# Step 01 — HL-2A-informed Environment

Назначение шага: проверить базовую reduced-order среду без управления.

Ожидаемый паттерн:

```text
N падает
D растёт
R1 = D - N растёт
R2 = D / (N + epsilon) растёт
mode_amp растёт как скрытая амплитуда доминирующей МГД-моды
collapse наступает
```

Запуск из папки `Step_01_Environment`:

```powershell
python experiments\run_environment_test.py
```

Этот шаг не тестирует контроллер. Он только проверяет, что среда воспроизводит HL-2A-informed сценарий риска.
