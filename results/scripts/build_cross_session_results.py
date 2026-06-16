import csv, glob, json, os, time, shutil, collections, hashlib
from pathlib import Path

OUT=Path("/workspace/robomme_cross_session_results")
CAN=Path("/workspace/final_consolidation/canonical_rollouts.csv")
LIVE=Path("/tmp/final_fill_results_v1_hot")
OUT.mkdir(parents=True, exist_ok=True)
(OUT/"protocol").mkdir(exist_ok=True)
(OUT/"scripts").mkdir(exist_ok=True)
(OUT/"logs").mkdir(exist_ok=True)
(OUT/"raw_sources").mkdir(exist_ok=True)

families=["MoveCube","RouteStick","VideoUnmask","VideoUnmaskSwap","VideoRepick","VideoPlaceButton","VideoPlaceOrder","InsertPeg","PatternLock"]
variants=["pi05_baseline","perceptual-framesamp-modul","perceptual-tokendrop-modul","recurrent-ttt-expert","perceptual-framesamp-context","perceptual-framesamp-expert","perceptual-tokendrop-context","perceptual-tokendrop-expert","recurrent-ttt-context"]
conditions=["no-history","k0","k1","k3","k7"]
expected=[]
for v in variants:
    conds=["no-history"] if v=="pi05_baseline" else conditions
    for f in families:
        for c in conds:
            expected.append((v,f,c))

def norm_variant(name):
    if "_tail" in name:
        name=name.split("_tail")[0]
    if "_shard" in name:
        name=name.split("_shard")[0]
    return name

def read_csv(path, variant_override=None, source_label=None):
    rows=[]
    if not Path(path).exists(): return rows
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if not r.get("family") or not r.get("condition") or r.get("episode") in (None,""):
                continue
            if variant_override: r["variant"]=variant_override
            if source_label: r["_source"]=source_label
            rows.append(r)
    return rows

source_files=[]
rows=[]
if CAN.exists():
    source_files.append(str(CAN))
    rows += read_csv(CAN, source_label=str(CAN))
for d in sorted(LIVE.glob("*")):
    if not d.is_dir(): continue
    raw=d/"raw_rollouts.csv"
    if raw.exists():
        v=norm_variant(d.name)
        source_files.append(str(raw))
        rows += read_csv(raw, variant_override=v, source_label=str(raw))

# Dedup by source-of-truth key, preferring live/current rows over older canonical rows.
def source_rank(src):
    return 1 if str(src).startswith(str(LIVE)) else 0
by_key={}
for r in rows:
    try: ep=int(float(r["episode"]))
    except Exception: continue
    key=(r.get("variant"), r.get("family"), r.get("condition"), ep)
    if key[0] not in variants or key[1] not in families or key[2] not in conditions:
        continue
    old=by_key.get(key)
    if old is None or source_rank(r.get("_source","")) >= source_rank(old.get("_source","")):
        r=dict(r); r["episode"]=str(ep); by_key[key]=r

field_order=["variant","family","split","episode","seed","difficulty","condition","success","status","steps","buffer_frames_start","buffer_frames_end","exec_start_idx","distractors","actual_start_lesson","actual_start_filler","actual_start_query","actual_start_lesson_fraction","actual_start_filler_fraction","actual_start_query_fraction","actual_end_lesson","actual_end_filler","actual_end_query","actual_end_lesson_fraction","actual_end_filler_fraction","actual_end_query_fraction","reset_wall_seconds","reset_server_ms","add_buffer_calls","add_buffer_frames","add_buffer_wall_seconds","add_buffer_server_ms","feature_cache_enabled","feature_cache_hits","feature_cache_misses","feature_cache_size","infer_calls","infer_wall_seconds","infer_server_ms","sim_step_wall_seconds","rollout_wall_seconds","_source"]
for r in by_key.values():
    for k in r.keys():
        if k not in field_order: field_order.append(k)
canonical=OUT/"canonical_rollouts.csv"
with open(canonical,"w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=field_order, extrasaction="ignore")
    w.writeheader()
    for key in sorted(by_key):
        w.writerow(by_key[key])

def is_success(r): return str(r.get("success","")).lower()=="true"
coverage_rows=[]
grid_rows=[]
family_rows=[]
difficulty_rows=[]
for v,f,c in expected:
    vals=[by_key[k] for k in sorted(by_key) if k[:3]==(v,f,c)]
    s=sum(1 for r in vals if is_success(r)); n=len(vals)
    status="complete" if n>=50 else ("partial" if n>0 else "missing")
    coverage_rows.append({"variant":v,"family":f,"condition":c,"successes":s,"n":n,"rate":(s/n if n else ""),"status":status,"missing_episodes":" ".join(map(str, sorted(set(range(50))-set(int(r["episode"]) for r in vals))))})
# variant-condition summary
for v in variants:
    conds=["no-history"] if v=="pi05_baseline" else conditions
    for c in conds:
        vals=[]
        for f in families:
            vals += [by_key[k] for k in sorted(by_key) if k[:3]==(v,f,c)]
        s=sum(1 for r in vals if is_success(r)); n=len(vals)
        grid_rows.append({"variant":v,"condition":c,"successes":s,"n":n,"rate":(s/n if n else "")})
# family-condition table
for f in families:
    for v in variants:
        conds=["no-history"] if v=="pi05_baseline" else conditions
        for c in conds:
            vals=[by_key[k] for k in sorted(by_key) if k[:3]==(v,f,c)]
            s=sum(1 for r in vals if is_success(r)); n=len(vals)
            family_rows.append({"family":f,"variant":v,"condition":c,"successes":s,"n":n,"rate":(s/n if n else ""),"status":"complete" if n>=50 else ("partial" if n else "missing")})
# difficulty
for v in variants:
    conds=["no-history"] if v=="pi05_baseline" else conditions
    vals=[]
    for c in conds:
        for f in families:
            vals += [by_key[k] for k in sorted(by_key) if k[:3]==(v,f,c)]
    for diff in ["easy","medium","hard"]:
        vv=[r for r in vals if (r.get("difficulty") or "")==diff]
        s=sum(1 for r in vv if is_success(r)); n=len(vv)
        difficulty_rows.append({"variant":v,"difficulty":diff,"successes":s,"n":n,"rate":(s/n if n else "")})

def write_table(path, table):
    if not table: return
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(table[0].keys()))
        w.writeheader(); w.writerows(table)
write_table(OUT/"coverage.csv", coverage_rows)
write_table(OUT/"grid_summary.csv", grid_rows)
write_table(OUT/"by_family_condition.csv", family_rows)
write_table(OUT/"by_difficulty.csv", difficulty_rows)

complete=sum(1 for r in coverage_rows if r["status"]=="complete")
partial=sum(1 for r in coverage_rows if r["status"]=="partial")
missing=sum(1 for r in coverage_rows if r["status"]=="missing")
row_cov=sum(min(int(r["n"]),50) for r in coverage_rows)
expected_rows=len(expected)*50
manifest={
    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "output_dir": str(OUT),
    "task_families": families,
    "variants": variants,
    "conditions": conditions,
    "expected_cells": len(expected),
    "complete_cells": complete,
    "partial_cells": partial,
    "missing_cells": missing,
    "row_coverage": row_cov,
    "expected_rows": expected_rows,
    "source_files": source_files,
    "notes": [
        "This folder is the single public-facing source of truth for RoboMME-Interference results.",
        "canonical_rollouts.csv is rebuilt from prior consolidated rows plus the current live fill directory.",
        "Rows are deduplicated by variant, family, condition, episode; live rows override older canonical rows.",
        "Scratch wave directories remain outside this folder until active jobs finish. Do not treat them as canonical."
    ]
}
with open(OUT/"MANIFEST.json","w") as f: json.dump(manifest,f,indent=2)
with open(OUT/"README.md","w") as f:
    f.write("# RoboMME-Interference Results\n\n")
    f.write("This directory is the single source of truth for the RoboMME-Interference cross-session memory evaluation results.\n\n")
    f.write("## Files\n\n")
    f.write("- `canonical_rollouts.csv`: one deduplicated rollout row per `(variant, family, condition, episode)`.\n")
    f.write("- `coverage.csv`: cell-level coverage and missing episodes.\n")
    f.write("- `grid_summary.csv`: success rate by variant and memory condition.\n")
    f.write("- `by_family_condition.csv`: success rate by family, variant, and condition.\n")
    f.write("- `by_difficulty.csv`: success rate by variant and difficulty.\n")
    f.write("- `MANIFEST.json`: source files and build metadata.\n\n")
    f.write("## Current Coverage\n\n")
    f.write(f"- Complete cells: {complete}/{len(expected)}\n")
    f.write(f"- Partial cells: {partial}\n")
    f.write(f"- Missing cells: {missing}\n")
    f.write(f"- Row coverage: {row_cov}/{expected_rows}\n\n")
    f.write("The live rollout may still be running. Rebuild this directory after the live run finishes for final paper numbers.\n")
# copy this builder script into scripts
_src = Path(__file__).resolve()
_dst = (OUT / 'scripts' / 'build_cross_session_results.py').resolve()
if _src != _dst:
    shutil.copyfile(_src, _dst)
print(json.dumps(manifest, indent=2))
