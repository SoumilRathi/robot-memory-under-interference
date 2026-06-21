// Qualitative showcase: task tabs -> per-system interference strips.
// Each strip shows one system's clips left-to-right across history conditions
// (no-history -> k0 -> k1 -> k3 -> k7), so the cross-session decay is legible.

const TASK_ORDER = ["VideoPlaceOrder", "VideoRepick", "PatternLock"];

const TASK_COPY = {
  VideoPlaceOrder: {
    title: "VideoPlaceOrder",
    kind: "Object / order memory",
    blurb:
      "The policy watches a prior demonstration, then must place the cube on the target used in that session. Tests placement-order memory across the interference gap.",
  },
  VideoRepick: {
    title: "VideoRepick",
    kind: "Object-identity memory",
    blurb:
      "The policy must re-pick the same object chosen in the demonstrated prior session — object-identity memory that has to survive unrelated intervening sessions.",
  },
  PatternLock: {
    title: "PatternLock",
    kind: "Procedural memory",
    blurb:
      "The policy retraces a demonstrated pattern over a grid — long-horizon procedural memory under increasing cross-session interference.",
  },
};

// Protagonist systems shown by default per task; the rest appear under "show all".
const FEATURED = {
  VideoPlaceOrder: ["perceptual-tokendrop-modul", "perceptual-framesamp-modul"],
  VideoRepick: ["perceptual-framesamp-modul", "perceptual-tokendrop-modul"],
  PatternLock: ["perceptual-framesamp-modul", "perceptual-tokendrop-modul"],
};

const ALL_SYSTEMS = [
  "perceptual-framesamp-modul",
  "perceptual-tokendrop-modul",
  "perceptual-framesamp-context",
  "recurrent-ttt-expert",
  "pi05_baseline",
];

const VARIANT_LABELS = {
  pi05_baseline: "pi0.5 (baseline)",
  "perceptual-framesamp-modul": "FrameSamp-Modul",
  "perceptual-tokendrop-modul": "TokenDrop-Modul",
  "perceptual-framesamp-context": "FrameSamp-Context",
  "perceptual-framesamp-expert": "FrameSamp-Expert",
  "perceptual-tokendrop-context": "TokenDrop-Context",
  "perceptual-tokendrop-expert": "TokenDrop-Expert",
  "recurrent-ttt-expert": "Recurrent-TTT-Expert",
  "recurrent-ttt-context": "Recurrent-TTT-Context",
};

const CONDITION_ORDER = ["no-history", "k0", "k1", "k3", "k7"];
const CONDITION_LABELS = {
  "no-history": "No history",
  k0: "k0",
  k1: "k1",
  k3: "k3",
  k7: "k7",
};
const CONDITION_SUBLABELS = {
  "no-history": "query only",
  k0: "relevant prior",
  k1: "+1 distractor",
  k3: "+3 distractors",
  k7: "+7 distractors",
};

const K_CONDITIONS = ["k0", "k1", "k3", "k7"];
const K_VALUE = { k0: 0, k1: 1, k3: 3, k7: 7 };

function cellKey(family, variant, condition) {
  return `${family}::${variant}::${condition}`;
}

// One IntersectionObserver per render: play clips only while visible.
let visibilityObserver = null;

function resetObserver() {
  if (visibilityObserver) visibilityObserver.disconnect();
  visibilityObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const video = entry.target;
        if (entry.isIntersecting) {
          const playPromise = video.play();
          if (playPromise) playPromise.catch(() => {});
        } else {
          video.pause();
        }
      }
    },
    { threshold: 0.25 },
  );
}

function makeVideo(row, family, variant, condition) {
  const video = document.createElement("video");
  video.muted = true;
  video.loop = true;
  video.autoplay = true;
  video.playsInline = true;
  video.preload = "auto";
  video.src = `assets/showcase-videos/${row.video}`;
  video.setAttribute(
    "aria-label",
    `${VARIANT_LABELS[variant]} on ${family}, ${CONDITION_LABELS[condition]}, ${row.status}`,
  );
  // Seek to a representative frame so a paused clip shows the scene, not the
  // black intro frame (also covers browsers that block muted autoplay).
  video.addEventListener(
    "loadedmetadata",
    () => {
      if (video.currentTime < 0.3) {
        try {
          video.currentTime = Math.min(1.2, (video.duration || 5) * 0.2);
        } catch (e) {}
      }
    },
    { once: true },
  );
  visibilityObserver.observe(video);
  return video;
}

function conditionCell(row, family, variant, condition) {
  const cell = document.createElement("div");
  cell.className = "ic-cell";

  const head = document.createElement("div");
  head.className = "ic-cell-head";
  const cond = document.createElement("span");
  cond.className = "ic-cond";
  cond.textContent = CONDITION_LABELS[condition];
  const sub = document.createElement("span");
  sub.className = "ic-sub";
  sub.textContent = CONDITION_SUBLABELS[condition];
  head.append(cond, sub);

  const frame = document.createElement("div");
  frame.className = "ic-frame";
  if (row) {
    frame.classList.add(row.status === "pass" ? "is-pass" : "is-fail");
    frame.append(makeVideo(row, family, variant, condition));
    const badge = document.createElement("span");
    badge.className = "ic-badge";
    badge.textContent = row.status === "pass" ? "pass" : "fail";
    const steps = document.createElement("span");
    steps.className = "ic-steps";
    steps.textContent = `${row.steps} steps`;
    frame.append(badge, steps);
  } else {
    frame.classList.add("is-empty");
    const na = document.createElement("span");
    na.className = "ic-na";
    na.textContent = "—";
    frame.append(na);
  }

  cell.append(head, frame);
  return cell;
}

// Concise, data-derived outcome summary for a system on a task.
function outcomeSummary(family, variant, rowsByKey) {
  if (variant === "pi05_baseline") return "no external memory";
  const passed = K_CONDITIONS.filter((c) => {
    const r = rowsByKey.get(cellKey(family, variant, c));
    return r && r.status === "pass";
  });
  if (passed.length === 0) return "no near-session benefit";
  const maxK = Math.max(...passed.map((c) => K_VALUE[c]));
  if (maxK >= 7) return "holds through k7";
  if (maxK >= 3) return "holds to k3, fails at k7";
  if (maxK >= 1) return "holds to k1, fails by k3";
  return "helps at k0 only";
}

function buildStrip(family, variant, rowsByKey) {
  const strip = document.createElement("div");
  strip.className = "ic-strip";
  if (variant === "perceptual-framesamp-modul") strip.classList.add("is-protagonist");

  const head = document.createElement("div");
  head.className = "ic-strip-head";
  const name = document.createElement("span");
  name.className = "ic-sys";
  name.textContent = VARIANT_LABELS[variant];
  const summary = document.createElement("span");
  summary.className = "ic-summary";
  summary.textContent = outcomeSummary(family, variant, rowsByKey);
  head.append(name, summary);

  // Baseline has only no-history: render a single reference cell.
  if (variant === "pi05_baseline") {
    const row = rowsByKey.get(cellKey(family, variant, "no-history"));
    const track = document.createElement("div");
    track.className = "ic-track is-reference";
    track.append(conditionCell(row, family, variant, "no-history"));
    const note = document.createElement("p");
    note.className = "ic-ref-note";
    note.textContent =
      "Reference: the backbone policy with no external history buffer.";
    strip.append(head, track, note);
    return strip;
  }

  const track = document.createElement("div");
  track.className = "ic-track";
  const outcomes = [];
  for (const condition of CONDITION_ORDER) {
    const row = rowsByKey.get(cellKey(family, variant, condition));
    track.append(conditionCell(row, family, variant, condition));
    if (condition !== "no-history") outcomes.push(row ? row.status : null);
  }

  // pass -> fail rail beneath the k-conditions (spacer aligns under no-history).
  const rail = document.createElement("div");
  rail.className = "ic-rail";
  const spacer = document.createElement("span");
  spacer.className = "ic-seg is-spacer";
  rail.append(spacer);
  for (const status of outcomes) {
    const seg = document.createElement("span");
    seg.className = `ic-seg is-${status || "empty"}`;
    rail.append(seg);
  }

  strip.append(head, track, rail);
  return strip;
}

function buildPanel(family, rowsByKey) {
  resetObserver();
  const panel = document.createElement("div");
  panel.className = "ic-panel";
  panel.id = `panel-${family}`;
  panel.setAttribute("role", "tabpanel");

  const copy = TASK_COPY[family];
  const head = document.createElement("div");
  head.className = "ic-panel-head";
  const kind = document.createElement("p");
  kind.className = "ic-kind";
  kind.textContent = copy.kind;
  const blurb = document.createElement("p");
  blurb.className = "ic-blurb";
  blurb.textContent = copy.blurb;
  head.append(kind, blurb);
  panel.append(head);

  // Show the no-memory baseline reference first, then the featured systems.
  const defaultSystems = ["pi05_baseline", ...FEATURED[family]];
  const strips = document.createElement("div");
  strips.className = "ic-strips";
  for (const variant of defaultSystems) {
    strips.append(buildStrip(family, variant, rowsByKey));
  }
  panel.append(strips);

  const rest = ALL_SYSTEMS.filter((v) => !defaultSystems.includes(v));
  if (rest.length) {
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "ic-toggle";
    toggle.textContent = "Show more systems";
    let expanded = false;
    toggle.addEventListener("click", () => {
      expanded = !expanded;
      if (expanded) {
        for (const variant of rest) {
          strips.append(buildStrip(family, variant, rowsByKey));
        }
        toggle.textContent = "Show fewer systems";
      } else {
        resetObserver();
        strips.replaceChildren();
        for (const variant of defaultSystems) {
          strips.append(buildStrip(family, variant, rowsByKey));
        }
        toggle.textContent = "Show more systems";
      }
    });
    panel.append(toggle);
  }

  return panel;
}

function renderShowcase(rows) {
  const root = document.getElementById("showcase-root");
  if (!root) return;
  const rowsByKey = new Map(
    rows.map((r) => [cellKey(r.family, r.variant, r.condition), r]),
  );

  const tablist = document.createElement("div");
  tablist.className = "ic-tabs";
  tablist.setAttribute("role", "tablist");

  const stage = document.createElement("div");
  stage.className = "ic-stage";

  function select(family, button) {
    for (const b of tablist.children) {
      b.classList.toggle("is-active", b === button);
      b.setAttribute("aria-selected", b === button ? "true" : "false");
    }
    stage.replaceChildren(buildPanel(family, rowsByKey));
  }

  TASK_ORDER.forEach((family, i) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ic-tab" + (i === 0 ? " is-active" : "");
    button.setAttribute("role", "tab");
    button.setAttribute("aria-selected", i === 0 ? "true" : "false");
    const t = document.createElement("span");
    t.className = "ic-tab-title";
    t.textContent = TASK_COPY[family].title;
    const k = document.createElement("span");
    k.className = "ic-tab-kind";
    k.textContent = TASK_COPY[family].kind;
    button.append(t, k);
    button.addEventListener("click", () => select(family, button));
    tablist.append(button);
  });

  root.replaceChildren(tablist, stage);
  stage.replaceChildren(buildPanel(TASK_ORDER[0], rowsByKey));
}

// Inline "memory curve" sparklines for the results table (k0 -> k7 decay).
function enhanceResultsTable() {
  const table = document.querySelector("#results table");
  if (!table) return;
  const headRow = table.querySelector("thead tr");
  if (!headRow || headRow.dataset.enhanced) return;
  headRow.dataset.enhanced = "1";

  const th = document.createElement("th");
  th.textContent = "k0→k7";
  headRow.append(th);

  const COLS = { k0: 2, k1: 3, k3: 4, k7: 5 }; // td indices for k-conditions
  const X = { k0: 0, k1: 1, k3: 2, k7: 3 };
  for (const tr of table.querySelectorAll("tbody tr")) {
    const tds = tr.children;
    const pts = [];
    for (const c of K_CONDITIONS) {
      const raw = tds[COLS[c]] ? tds[COLS[c]].textContent.trim() : "-";
      const v = parseFloat(raw);
      if (!Number.isNaN(v)) pts.push([X[c], v]);
    }
    const td = document.createElement("td");
    td.className = "spark-cell";
    if (pts.length >= 2) td.append(sparkline(pts));
    tr.append(td);
  }
}

function sparkline(points) {
  const W = 84;
  const H = 26;
  const pad = 3;
  const xs = points.map((p) => p[0]);
  const maxX = Math.max(...xs) || 1;
  const maxV = 50; // fixed scale so rows are comparable
  const px = (x) => pad + (x / maxX) * (W - 2 * pad);
  const py = (v) => H - pad - (v / maxV) * (H - 2 * pad);
  const d = points
    .map((p, i) => `${i === 0 ? "M" : "L"}${px(p[0]).toFixed(1)},${py(p[1]).toFixed(1)}`)
    .join(" ");
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("width", W);
  svg.setAttribute("height", H);
  svg.setAttribute("class", "spark");
  svg.setAttribute("aria-hidden", "true");
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", d);
  path.setAttribute("fill", "none");
  path.setAttribute("stroke", "currentColor");
  path.setAttribute("stroke-width", "1.5");
  path.setAttribute("stroke-linejoin", "round");
  path.setAttribute("stroke-linecap", "round");
  svg.append(path);
  const last = points[points.length - 1];
  const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  dot.setAttribute("cx", px(last[0]).toFixed(1));
  dot.setAttribute("cy", py(last[1]).toFixed(1));
  dot.setAttribute("r", "1.6");
  dot.setAttribute("fill", "currentColor");
  svg.append(dot);
  return svg;
}

// Hero clips are declared in HTML; give them the same poster-frame treatment
// so they show the scene rather than a black intro frame.
function enhanceHero() {
  for (const v of document.querySelectorAll(".hero-card video")) {
    v.addEventListener(
      "loadedmetadata",
      () => {
        if (v.currentTime < 0.3) {
          try {
            v.currentTime = Math.min(1.2, (v.duration || 5) * 0.2);
          } catch (e) {}
        }
      },
      { once: true },
    );
    const p = v.play();
    if (p) p.catch(() => {});
  }
}

// ---- Per-family success heatmap (system-selectable) ----
const HEATMAP_FAMILY_ORDER = [
  "MoveCube",
  "RouteStick",
  "VideoUnmask",
  "VideoUnmaskSwap",
  "VideoRepick",
  "VideoPlaceButton",
  "VideoPlaceOrder",
  "InsertPeg",
  "PatternLock",
];

const HEATMAP_SYSTEM_ORDER = [
  "perceptual-framesamp-modul",
  "perceptual-tokendrop-modul",
  "perceptual-framesamp-context",
  "perceptual-framesamp-expert",
  "perceptual-tokendrop-context",
  "perceptual-tokendrop-expert",
  "recurrent-ttt-expert",
  "recurrent-ttt-context",
  "pi05_baseline",
];

function parseFamilyCsv(text) {
  const lines = text.trim().split("\n");
  const header = lines[0].split(",").map((h) => h.trim());
  const idx = {};
  header.forEach((h, i) => (idx[h] = i));
  const map = new Map();
  for (let i = 1; i < lines.length; i++) {
    const c = lines[i].split(",");
    const key = `${c[idx.family]}::${c[idx.variant]}::${c[idx.condition]}`;
    map.set(key, parseFloat(c[idx.rate]));
  }
  return map;
}

// Sequential light -> accent scale; values normalized to a fixed 90% ceiling
// so systems stay comparable when switching.
function heatColor(rate) {
  const t = Math.max(0, Math.min(1, rate / 0.9));
  const lo = [237, 242, 248];
  const hi = [31, 78, 126];
  const ch = lo.map((l, i) => Math.round(l + (hi[i] - l) * t));
  return { bg: `rgb(${ch[0]}, ${ch[1]}, ${ch[2]})`, light: t > 0.5 };
}

function renderHeatmap(grid, variant, map) {
  grid.replaceChildren();
  const corner = document.createElement("div");
  corner.className = "hm-corner";
  grid.append(corner);
  for (const cond of CONDITION_ORDER) {
    const h = document.createElement("div");
    h.className = "hm-colhead";
    h.textContent = CONDITION_LABELS[cond];
    grid.append(h);
  }
  for (const fam of HEATMAP_FAMILY_ORDER) {
    const rh = document.createElement("div");
    rh.className = "hm-rowhead";
    rh.textContent = fam;
    grid.append(rh);
    for (const cond of CONDITION_ORDER) {
      const rate = map.get(`${fam}::${variant}::${cond}`);
      const cell = document.createElement("div");
      cell.className = "hm-cell";
      if (rate == null || Number.isNaN(rate)) {
        cell.classList.add("is-empty");
        cell.textContent = "—";
      } else {
        const c = heatColor(rate);
        cell.style.background = c.bg;
        if (c.light) cell.style.color = "#fff";
        cell.textContent = Math.round(rate * 100);
        cell.title = `${VARIANT_LABELS[variant]} · ${fam} · ${CONDITION_LABELS[cond]}: ${Math.round(rate * 100)}%`;
      }
      grid.append(cell);
    }
  }
}

async function buildHeatmap() {
  const grid = document.getElementById("heatmap-grid");
  const select = document.getElementById("heatmap-system");
  if (!grid || !select) return;
  let map;
  try {
    const resp = await fetch("results/by_family_condition.csv");
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    map = parseFamilyCsv(await resp.text());
  } catch (error) {
    grid.innerHTML =
      '<p class="note">Per-family data could not be loaded here; full per-family results are in the paper.</p>';
    console.error(error);
    return;
  }
  for (const v of HEATMAP_SYSTEM_ORDER) {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = VARIANT_LABELS[v];
    select.append(opt);
  }
  select.value = "perceptual-framesamp-modul";
  select.addEventListener("change", () =>
    renderHeatmap(grid, select.value, map),
  );
  renderHeatmap(grid, select.value, map);
}

// Open every off-page link (paper, code, data, RoboMME, artifacts, footer) in a
// new tab; in-page anchors (#section) stay in place.
function enhanceLinks() {
  for (const a of document.querySelectorAll("a[href]")) {
    const href = a.getAttribute("href");
    if (href && !href.startsWith("#")) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    }
  }
}

async function init() {
  enhanceLinks();
  enhanceHero();
  enhanceResultsTable();
  buildHeatmap();
  const root = document.getElementById("showcase-root");
  if (!root) return;
  try {
    const response = await fetch("assets/showcase-videos/manifest.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    renderShowcase(rows);
  } catch (error) {
    root.innerHTML =
      '<p class="note">Could not load qualitative examples. The video manifest is available at <a href="assets/showcase-videos/manifest.json">assets/showcase-videos/manifest.json</a>.</p>';
    console.error(error);
  }
}

init();
