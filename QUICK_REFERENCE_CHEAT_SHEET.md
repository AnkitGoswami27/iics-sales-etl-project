# Quick Reference Cheat Sheet — Hackathon Edition

## PL/SQL One-Liners

### Variables
```sql
DECLARE v_name VARCHAR2(100); v_count NUMBER := 0;
```

### Select Into
```sql
SELECT column INTO v_variable FROM table WHERE condition;
```

### IF-THEN-ELSE
```sql
IF condition THEN ... ELSIF condition THEN ... ELSE ... END IF;
```

### Loop Through Cursor
```sql
FOR rec IN (SELECT * FROM table) LOOP ... END LOOP;
```

### Function
```sql
CREATE OR REPLACE FUNCTION func_name(p_param IN NUMBER) RETURN VARCHAR2 IS v_var VARCHAR2(100); BEGIN ... RETURN v_var; END;
```

### Exception Handling
```sql
BEGIN ... EXCEPTION WHEN NO_DATA_FOUND THEN ... WHEN OTHERS THEN ... END;
```

### Aggregation
```sql
SELECT category, COUNT(*) cnt, SUM(amount) total FROM table GROUP BY category;
```

---

## IICS Transformation Quick Map

| Need | Use | Field Input | Field Output |
|------|-----|------------|--------------|
| Read data | Source | (file/table) | Auto-mapped |
| Calculate | Expression | Input port | o_FIELD_NAME |
| Split data | Router | Input + Condition | 2 outputs |
| Group & sum | Aggregator | Input | SUM/COUNT/AVG ports |
| Filter rows | Filter | Condition | Matching rows only |
| Write data | Target | Input | (file/table) |

---

## Common Expression Formulas (IICS)

```
Fix null:           IIF(ISNULL(FIELD), 0, FIELD)
Fix negative:       ABS(FIELD)
Cap value:          IIF(FIELD > 100, 100, FIELD)
Calculate revenue:  TO_DECIMAL(Q) * TO_DECIMAL(P) * (1 - TO_DECIMAL(D)/100)
Validate date:      IIF(IS_DATE(FIELD, 'MM/DD/YYYY'), TO_DATE(...), NULL)
Convert to number:  TO_INTEGER(FIELD) or TO_DECIMAL(FIELD)
Reject flag:        IIF(ISNULL(F1) OR ISNULL(F2), 'FAIL', 'PASS')
```

---

## Taskflow Pattern Templates

### Sequential
```
Start → Task1 → Task2 → Task3 → End
        (success)  (success)
```

### Parallel
```
Start → Fork → Task1 ─┐
              Task2  ├→ Join → Final Task → End
              Task3 ─┘
```

### Conditional
```
Start → Task1 → Decision → Branch A → End
                          → Branch B → End
```

---

## Data Validation Quick Queries

```sql
-- Row count
SELECT COUNT(*) FROM target;

-- Percent change
SELECT (SELECT COUNT(*) FROM target) / (SELECT COUNT(*) FROM source) * 100 as pct;

-- Nulls
SELECT COUNT(*) FROM table WHERE COLUMN IS NULL;

-- Duplicates
SELECT COLUMN, COUNT(*) FROM table GROUP BY COLUMN HAVING COUNT(*) > 1;

-- Min/Max
SELECT MIN(amount), MAX(amount) FROM table;

-- Sum/Avg
SELECT SUM(amount), AVG(amount) FROM table;

-- Group count
SELECT category, COUNT(*) FROM table GROUP BY category ORDER BY COUNT(*) DESC;
```

---

## IICS My Jobs Reading Guide

```
Instance Name     = Job run name
Status            = SUCCESS ✓ or FAILED ✗
Subtasks          = How many steps ran
Rows Processed    = Total input rows
Duration          = How long it took
Start/End Time    = When it ran
```

**If Failed:**
1. Click job name
2. Expand subtasks
3. Find red ✗ step
4. Click it → see error message
5. Error message → tells you what went wrong

---

## Expression Debugging Checklist

- [ ] All port names start with `o_`?
- [ ] All TO_DECIMAL/TO_INTEGER conversions done?
- [ ] All IIF conditions properly closed?
- [ ] Any nested IIF parentheses balanced?
- [ ] Date format matches IS_DATE parameter?
- [ ] SELECT INTO statement finds exactly 1 row?

---

## Mapping Validation Checklist

- [ ] Source reads correct # rows?
- [ ] Expression ports all have correct types?
- [ ] Router condition logic is correct?
- [ ] Aggregator has correct GROUP BY?
- [ ] Target writes all rows?
- [ ] No orphan records (FK violations)?
- [ ] Data ranges within expected bounds?

---

## Mentor Question Responses (Memorize These)

**"What did you do?"**
> "I built a pipeline that cleanses dirty data using Expression transformations, 
> splits it with a Router, aggregates by category, and validates the output."

**"Why that approach?"**
> "Expression is flexible for multiple transformations. Router captures both 
> clean and rejected records for audit. Aggregator groups efficiently."

**"How do you know it's correct?"**
> "I validated: (1) row counts match, (2) unique values are expected, 
> (3) aggregate totals make sense."

**"What if direction changes?"**
> "I'd adjust the expression logic and re-run. Since I documented the rules, 
> finding what to change is quick."

**"Can you explain that formula?"**
> "Sure — TO_DECIMAL converts text to number, multiplication is order of operations, 
> and (1 - discount/100) applies the discount percentage."

---

## Timing Reference (for estimation)

Single mapping run: 30-60 seconds  
Parallel 3 tasks: 45-90 seconds (all together)  
Sequential 3 tasks: 2-3 minutes (one after another)  
Data validation query: 5-10 seconds  
Taskflow execution: 2-5 minutes total  

**Hackathon goal:** Build, test, validate all by 2 PM

---

## Last-Minute Reminders (March 23)

✓ Understand your own code  
✓ Validate early and often  
✓ Document what you're doing  
✓ Ask mentor questions (it's allowed!)  
✓ Stay calm when error appears  
✓ Check My Jobs for row counts  
✓ Take screenshots as proof  
✓ Be ready to explain everything  

---

**Print this page. Keep it with you March 23.** 📋
