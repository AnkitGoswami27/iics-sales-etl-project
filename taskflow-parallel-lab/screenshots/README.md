# Screenshots Guide — Parallel Taskflow Lab

Place your IICS screenshots in this folder with these exact names:

## Required Screenshots (8 total)

### 1. Taskflow Canvas — Full View
**File:** `01_taskflow_canvas_full.png`  
**What to capture:** Entire Taskflow1 canvas showing:
- Start circle
- Init_Variables step
- Fork diamond (Parallel Paths 1)
- 3 mapping task boxes (Customers, Products, Orders)
- Join diamond
- Sales_Fact step
- Decision step (optional)
- End circle
**Why:** Shows the complete parallel architecture

### 2. My Jobs — Execution Result
**File:** `02_myjobs_execution_success.png`  
**What to capture:** My Jobs list showing `Taskflow1` run with:
- Instance Name
- Status: Success ✓ (green checkmark)
- Subtasks count (should show 4)
- Duration
- Rows Processed
**Why:** Provides execution proof — the "green box" HCL wants to see

### 3. Taskflow Run Details Panel
**File:** `03_taskflow_run_details.png`  
**What to capture:** Click into the Taskflow run to show:
- Task Name, Instance ID
- Status: Success
- Start Date/Time, End Date/Time
- Duration
- Runtime Environment: AnkitGoswami
- Secure Agent: AnkitGoswami
**Why:** Shows full execution details and agent used

### 4. M_Load_Customers Mapping Canvas
**File:** `04_mapping_customers.png`  
**What to capture:** Open M_Load_Customers mapping, show:
- Source object (flat file icon with DIM_CUSTOMERS_SOURCE.csv)
- Target object (TGT_CUSTOMERS.csv)
- Fields auto-mapped between them
**Why:** Example of simple pass-through mapping

### 5. M_Load_Products Mapping Canvas
**File:** `05_mapping_products.png`  
**What to capture:** Same as above but for Products

### 6. M_Load_Orders Mapping Canvas
**File:** `06_mapping_orders.png`  
**What to capture:** Same as above but for Orders

### 7. M_Load_Sales_Fact Mapping Canvas
**File:** `07_mapping_salesfact.png`  
**What to capture:** Same as above but for Fact table

### 8. Parallel Gateway Configuration
**File:** `08_parallel_paths_config.png`  
**What to capture:** Click the Fork diamond → Properties panel showing:
- Step Type: Parallel Paths
- Parallel Paths tab
- Path 1, Path 2, Path 3 listed
**Why:** Shows you understand the fork/join mechanics

---

## Optional but Strong Bonus Screenshots

**09_decision_step_condition.png**
- Decision step properties showing the condition formula

**10_mapping_task_properties.png**
- One of the 4 Mapping Task properties showing Task assignment

**11_taskflow_variables.png**
- Taskflow Temp Fields showing v_STATUS variable definition

---

## How to Take Screenshots

1. **In IICS**, use **Print Screen** or **Snipping Tool**
   - Windows: `Win + Shift + S` → drag to select area
   
2. **Save to this folder:** 
   - `C:\Users\ag354\OneDrive\Desktop\iics-project\taskflow-parallel-lab\screenshots\`
   
3. **Naming:** Use exactly as listed (01_, 02_, etc.)

4. **Once all are added**, message me: 
   > "Screenshots ready. Push to GitHub."

---

## Pro Tips for Good Screenshots

✅ **DO:**
- Zoom out so full object is visible
- Include step names/labels
- Capture status indicators (green ✓, red ✗)
- Show property panels for configuration proof

❌ **DON'T:**
- Cut off important parts
- Include personal info/emails
- Make dark screenshots (use print screen, not phone photos)
- Include error messages or failures

---

**Once you have 6+ screenshots here, I will add, commit, and push everything to GitHub.**
