# Research Graphs Assessment

**Date:** 2025-10-30  
**Issue:** research_agent_full and multi_agent_supervisor graphs failing to load

---

## Investigation Results

### Critical Finding: Missing Source File

**File:** `research_agent_scope.py`  
**Status:** ❌ COMPLETELY MISSING from project

**Evidence:**
1. Only compiled `.pyc` files exist in `deep-research-agent/__pycache__/`
2. No `.py` source file found anywhere in project
3. Functions `clarify_with_user` and `write_research_brief` are undefined
4. Comment in `graphs/research/research_agent_full.py` line 22-23 acknowledges this:
   ```python
   # Note: research_agent_scope module needs to be created or imported separately
   # from graphs.research.research_agent_scope import clarify_with_user, write_research_brief
   ```

### Missing Functions

**Function 1: `clarify_with_user`**
- Purpose: User clarification and scoping node
- Used in: research_agent_full workflow
- Status: No source code found

**Function 2: `write_research_brief`**
- Purpose: Research brief generation node
- Used in: research_agent_full workflow
- Status: No source code found

### Search Results

```bash
# Searched entire project
grep -r "def clarify_with_user" .     # No matches
grep -r "def write_research_brief" .  # No matches
```

**Only references found:**
- Import statements (commented out or broken)
- Node additions in graph builder
- Prompt instructions in `prompts.py`

---

## Impact Assessment

### Graphs Affected

1. **research_agent_full** - ❌ BROKEN
   - Missing 2 critical node functions
   - Cannot be loaded by langgraph dev
   - Blocks server startup

2. **multi_agent_supervisor** - ❓ UNKNOWN
   - Not tested yet (blocked by research_agent_full failure)
   - May have similar issues

### Working Graphs (6/8)

✅ **Studio Graphs (4):**
1. parallelization
2. sub_graphs
3. map_reduce
4. research_assistant

✅ **Production Graphs (2):**
5. task_maistro
6. email_assistant

---

## Root Cause Analysis

### Why This Happened

1. **Incomplete Migration:** The `research_agent_scope.py` file was never copied from `deep-research-agent/` to `graphs/research/`

2. **Missing Source:** The source file doesn't exist in `deep-research-agent/` either - only compiled `.pyc` files

3. **Git History:** The file may have been:
   - Deleted accidentally
   - Never committed to git
   - Lost during a previous refactor
   - Part of `.gitignore` (check this)

### Pre-Existing Issue

**This is NOT caused by our consolidation work.**  
The research graphs were already broken before we started Phase 3.

---

## Options Analysis

### Option A: Fix the Research Graphs ⏱️ Time: 2-4 hours

**Approach:**
1. Decompile `.pyc` files to recover source code
2. Recreate `clarify_with_user` and `write_research_brief` functions
3. Test and debug until working
4. Add to `graphs/research/research_agent_scope.py`

**Pros:**
- All 8 graphs working
- Complete consolidation

**Cons:**
- Time-consuming (2-4 hours minimum)
- Decompiled code may be incomplete
- May uncover more missing pieces
- Blocks consolidation progress

**Recommendation:** ❌ NOT RECOMMENDED for current consolidation effort

---

### Option B: Exclude Research Graphs ⏱️ Time: 5 minutes

**Approach:**
1. Remove `research_agent_full` and `multi_agent_supervisor` from `langgraph.json`
2. Document as "Work in Progress - requires code reconstruction"
3. Complete consolidation with 6 working graphs
4. Address research graphs as separate task later

**Pros:**
- Fast - unblocks consolidation immediately
- 6 solid, demo-ready graphs
- Can complete Steps 6-13 today
- Research graphs can be fixed separately

**Cons:**
- Only 75% of graphs working
- Research functionality unavailable for demos

**Recommendation:** ✅ RECOMMENDED - Best path forward

---

### Option C: Stub Out Missing Functions ⏱️ Time: 30 minutes

**Approach:**
1. Create `graphs/research/research_agent_scope.py`
2. Add stub implementations that return placeholder data
3. Get graphs to load (even if not fully functional)
4. Document as "Partial Implementation"

**Pros:**
- All 8 graphs load in Studio
- Can demonstrate graph structure
- Faster than full fix

**Cons:**
- Graphs don't actually work
- Misleading - looks working but isn't
- Still requires full fix later

**Recommendation:** ⚠️ POSSIBLE but not ideal

---

## Final Recommendation

### ✅ PROCEED WITH OPTION B: Exclude Research Graphs

**Rationale:**
1. **Time-Efficient:** Unblocks consolidation immediately
2. **Quality Focus:** 6 fully working graphs > 8 partially broken graphs
3. **Separation of Concerns:** Research graph reconstruction is a separate project
4. **Demo-Ready:** 6 graphs cover all major patterns (studio demos + production)

**Implementation:**
1. Remove 2 lines from `langgraph.json`:
   ```json
   "research_agent_full": "./graphs/research/research_agent_full.py:graph",
   "multi_agent_supervisor": "./graphs/research/multi_agent_supervisor.py:graph"
   ```

2. Update documentation to note research graphs are WIP

3. Continue with Steps 6-13 (archive old folders, final validation)

4. Create separate task: "Reconstruct Research Agent Scope Module"

---

## Success Metrics After Option B

- ✅ ONE `langgraph dev` command launches 6 graphs
- ✅ All 6 graphs fully functional and demo-ready
- ✅ Zero errors on server startup
- ✅ Clean, consolidated project structure
- ✅ Old folders archived
- ✅ Documentation complete

**Coverage:** 6/8 graphs = 75% (excellent for initial consolidation)

---

## Next Steps (If Option B Approved)

1. **Immediate (5 min):**
   - Remove 2 research graphs from langgraph.json
   - Test `langgraph dev` - should start cleanly with 6 graphs
   - Verify all 6 graphs in Studio UI

2. **Continue Consolidation (Steps 6-13):**
   - Archive old folders
   - Final validation
   - Documentation updates
   - Commit consolidation

3. **Future Task (Separate):**
   - Create issue: "Reconstruct research_agent_scope.py module"
   - Attempt .pyc decompilation
   - Rebuild missing functions
   - Test and integrate

---

**End of Assessment**
