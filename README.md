<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SOC Command Center | Live Threat Intelligence</title>

  <!-- Tailwind CDN -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root{
      --bg0:#020617;         /* deep slate */
      --bg1:#050b1d;         /* inner */
      --card: rgba(10, 15, 30, .62);
      --card2: rgba(7, 12, 28, .58);
      --stroke: rgba(148,163,184,.14);

      --teal:#22d3ee;
      --purple:#a855f7;
      --blue:#3b82f6;
      --green:#34d399;
      --amber:#fbbf24;
      --red:#fb7185;

      --glowTeal: 0 0 24px rgba(34,211,238,.22);
      --glowPurple: 0 0 26px rgba(168,85,247,.20);
    }

    html, body { height: 100%; background: radial-gradient(1200px 700px at 18% 12%, rgba(34,211,238,.10), transparent 55%),
                                  radial-gradient(900px 500px at 78% 18%, rgba(168,85,247,.12), transparent 55%),
                                  radial-gradient(900px 650px at 58% 82%, rgba(59,130,246,.10), transparent 60%),
                                  var(--bg0);
                 color:#e5e7eb; }

    /* subtle grid */
    .grid-bg{
      background-image:
        linear-gradient(to right, rgba(148,163,184,.06) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(148,163,184,.06) 1px, transparent 1px);
      background-size: 52px 52px;
      mask-image: radial-gradient(circle at 30% 20%, rgba(0,0,0,.98), rgba(0,0,0,.35) 60%, transparent 78%);
    }

    .glass{
      background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
      border: 1px solid var(--stroke);
      backdrop-filter: blur(14px);
      box-shadow: 0 18px 60px rgba(0,0,0,.42);
      border-radius: 22px;
    }
    .glass2{
      background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.015));
      border: 1px solid rgba(148,163,184,.12);
      backdrop-filter: blur(16px);
      border-radius: 18px;
      box-shadow: 0 14px 40px rgba(0,0,0,.35);
    }
    .chip{
      border: 1px solid rgba(148,163,184,.16);
      background: rgba(2,6,23,.45);
      border-radius: 999px;
      padding: 6px 10px;
    }
    .neon-line{
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(34,211,238,.45), rgba(168,85,247,.45), transparent);
      filter: drop-shadow(0 0 10px rgba(34,211,238,.15));
    }
    .title-glow{
      text-shadow: 0 0 12px rgba(34,211,238,.18), 0 0 18px rgba(168,85,247,.14);
    }
    .kpi{
      background: linear-gradient(180deg, rgba(10,15,30,.78), rgba(10,15,30,.46));
      border: 1px solid rgba(148,163,184,.14);
      border-radius: 18px;
      box-shadow: 0 16px 40px rgba(0,0,0,.36);
    }

    /* status badges */
    .badge{
      font-size: 11px;
      border-radius: 999px;
      padding: 5px 10px;
      border: 1px solid rgba(148,163,184,.14);
      background: rgba(2,6,23,.55);
      white-space: nowrap;
    }
    .b-critical{ color: #fecaca; border-color: rgba(251,113,133,.35); box-shadow: 0 0 16px rgba(251,113,133,.12); }
    .b-high{ color: #fde68a; border-color: rgba(251,191,36,.30); box-shadow: 0 0 16px rgba(251,191,36,.10); }
    .b-med{ color: #bbf7d0; border-color: rgba(52,211,153,.28); box-shadow: 0 0 16px rgba(52,211,153,.10); }
    .b-low{ color: #bae6fd; border-color: rgba(34,211,238,.28); box-shadow: 0 0 16px rgba(34,211,238,.08); }

    /* scroll */
    .soft-scroll::-webkit-scrollbar{ height: 10px; width: 10px; }
    .soft-scroll::-webkit-scrollbar-thumb{
      background: linear-gradient(180deg, rgba(34,211,238,.25), rgba(168,85,247,.22));
      border: 1px solid rgba(148,163,184,.14);
      border-radius: 999px;
    }
    .soft-scroll::-webkit-scrollbar-track{ background: rgba(255,255,255,.03); border-radius: 999px; }

    /* animate pulse dots */
    .pulse-dot{
      width: 9px; height: 9px; border-radius: 999px;
      background: rgba(34,211,238,.9);
      box-shadow: 0 0 18px rgba(34,211,238,.32);
      position: relative;
    }
    .pulse-dot::after{
      content:""; position:absolute; inset:-7px; border-radius:999px;
      border: 1px solid rgba(34,211,238,.30);
      animation: ping 1.4s infinite;
    }
    @keyframes ping{
      0%{ transform: scale(.75); opacity:.6; }
      100%{ transform: scale(1.5); opacity:0; }
    }

    /* small hover lift */
    .lift { transition: transform .25s ease, box-shadow .25s ease; }
    .lift:hover { transform: translateY(-2px); box-shadow: 0 22px 70px rgba(0,0,0,.50); }

    canvas.threatMap{
      width: 100%; height: 250px;
      border-radius: 18px;
      background: radial-gradient(800px 260px at 20% 20%, rgba(34,211,238,.12), transparent 60%),
                  radial-gradient(760px 260px at 70% 40%, rgba(168,85,247,.12), transparent 55%),
                  rgba(2,6,23,.45);
      border: 1px solid rgba(148,163,184,.14);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.03);
    }

    /* number font feel */
    .mono{ font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; }
  </style>
</head>

<body>
  <div class="absolute inset-0 grid-bg pointer-events-none"></div>

  <div class="max-w-[1500px] mx-auto px-4 py-5">
    <!-- Header -->
    <div class="glass px-5 py-4 mb-4">
      <div class="flex flex-col lg:flex-row gap-3 lg:items-center lg:justify-between">
        <div class="flex items-center gap-3">
          <div class="w-11 h-11 rounded-2xl grid place-items-center"
               style="background: linear-gradient(135deg, rgba(34,211,238,.18), rgba(168,85,247,.16));
                      border:1px solid rgba(148,163,184,.14);
                      box-shadow: var(--glowTeal), var(--glowPurple);">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
              <path d="M12 2l8 4v6c0 5-3.4 9.4-8 10-4.6-.6-8-5-8-10V6l8-4z" stroke="rgba(34,211,238,.95)" stroke-width="1.6"/>
              <path d="M8 12l2.2 2.2L16 8.4" stroke="rgba(168,85,247,.95)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div>
            <div class="text-xl font-semibold title-glow">SOC Command Center</div>
            <div class="text-xs text-slate-300/70">Live Threat Intelligence • Correlation • Incident Triage</div>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <div class="chip flex items-center gap-2">
            <div class="pulse-dot"></div>
            <span class="text-xs text-slate-200/90">LIVE</span>
            <span class="text-xs text-slate-400/70">refresh:</span>
            <span class="text-xs mono text-slate-200/90" id="refreshTick">1s</span>
          </div>

          <div class="chip text-xs text-slate-200/90">
            <span class="text-slate-400/70">Tenant:</span> BT-Enterprise
          </div>

          <div class="chip text-xs text-slate-200/90">
            <span class="text-slate-400/70">Analyst:</span> Tier-1
          </div>

          <button id="btnContain"
                  class="chip text-xs font-semibold lift"
                  style="border-color: rgba(251,113,133,.22); box-shadow: 0 0 18px rgba(251,113,133,.10);">
            ⚠ Quick Containment
          </button>
        </div>
      </div>

      <div class="mt-4 neon-line"></div>

      <!-- Filters -->
      <div class="mt-4 flex flex-col md:flex-row gap-3 md:items-center md:justify-between">
        <div class="flex flex-wrap gap-2">
          <button class="chip text-xs lift filterBtn" data-range="5m">Last 5m</button>
          <button class="chip text-xs lift filterBtn" data-range="15m">Last 15m</button>
          <button class="chip text-xs lift filterBtn active" data-range="1h"
                  style="border-color: rgba(34,211,238,.30); box-shadow: var(--glowTeal);">
            Last 1h
          </button>
          <button class="chip text-xs lift filterBtn" data-range="24h">Last 24h</button>
        </div>

        <div class="flex flex-wrap gap-2">
          <div class="chip text-xs">
            <span class="text-slate-400/70">Threat Level:</span>
            <span id="threatLevel" class="mono font-semibold" style="color: var(--amber)">ELEVATED</span>
          </div>
          <div class="chip text-xs">
            <span class="text-slate-400/70">SOC Health:</span>
            <span id="socHealth" class="mono font-semibold" style="color: var(--green)">NORMAL</span>
          </div>
          <div class="chip text-xs">
            <span class="text-slate-400/70">UTC:</span>
            <span id="utcTime" class="mono"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- KPIs -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-4">
      <div class="kpi p-4 lift">
        <div class="flex items-start justify-between">
          <div>
            <div class="text-xs text-slate-400/80">Attack Attempts / Min</div>
            <div class="text-3xl font-bold mono mt-1" id="kpiAttempts">—</div>
            <div class="text-xs mt-1 text-slate-300/70">
              spike: <span class="mono" id="kpiSpike" style="color: var(--amber)">+0%</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-2xl grid place-items-center"
               style="background: rgba(34,211,238,.08); border:1px solid rgba(34,211,238,.16); box-shadow: var(--glowTeal);">
            ⚡
          </div>
        </div>
        <div class="mt-3">
          <canvas id="sparkAttempts" height="62"></canvas>
        </div>
      </div>

      <div class="kpi p-4 lift">
        <div class="flex items-start justify-between">
          <div>
            <div class="text-xs text-slate-400/80">Suspicious Logins (1h)</div>
            <div class="text-3xl font-bold mono mt-1" id="kpiSuspicious">—</div>
            <div class="text-xs mt-1 text-slate-300/70">
              MFA challenges: <span class="mono" id="kpiMfa" style="color: var(--teal)">0</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-2xl grid place-items-center"
               style="background: rgba(168,85,247,.08); border:1px solid rgba(168,85,247,.16); box-shadow: var(--glowPurple);">
            🔐
          </div>
        </div>
        <div class="mt-3">
          <canvas id="sparkLogins" height="62"></canvas>
        </div>
      </div>

      <div class="kpi p-4 lift">
        <div class="flex items-start justify-between">
          <div>
            <div class="text-xs text-slate-400/80">Blocked IPs (Rolling)</div>
            <div class="text-3xl font-bold mono mt-1" id="kpiBlocked">—</div>
            <div class="text-xs mt-1 text-slate-300/70">
              WAF blocks: <span class="mono" id="kpiWaf" style="color: var(--blue)">0</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-2xl grid place-items-center"
               style="background: rgba(59,130,246,.08); border:1px solid rgba(59,130,246,.16); box-shadow: 0 0 24px rgba(59,130,246,.18);">
            🧱
          </div>
        </div>
        <div class="mt-3">
          <canvas id="sparkBlocks" height="62"></canvas>
        </div>
      </div>

      <div class="kpi p-4 lift">
        <div class="flex items-start justify-between">
          <div>
            <div class="text-xs text-slate-400/80">Open Incidents</div>
            <div class="text-3xl font-bold mono mt-1" id="kpiIncidents">—</div>
            <div class="text-xs mt-1 text-slate-300/70">
              SLA breaches: <span class="mono" id="kpiSla" style="color: var(--red)">0</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-2xl grid place-items-center"
               style="background: rgba(251,113,133,.08); border:1px solid rgba(251,113,133,.16); box-shadow: 0 0 24px rgba(251,113,133,.16);">
            🚨
          </div>
        </div>
        <div class="mt-3">
          <canvas id="sparkInc" height="62"></canvas>
        </div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-12 gap-4">
      <!-- Threat Map -->
      <div class="glass2 p-4 xl:col-span-7 lift">
        <div class="flex items-center justify-between mb-3">
          <div>
            <div class="font-semibold">Global Threat Map</div>
            <div class="text-xs text-slate-400/80">Geo correlation • attack origins → protected assets</div>
          </div>
          <div class="flex gap-2">
            <span class="badge b-low">Port Scan</span>
            <span class="badge b-med">Brute Force</span>
            <span class="badge b-high">Web Exploit</span>
            <span class="badge b-critical">Malware</span>
          </div>
        </div>
        <canvas id="threatMap" class="threatMap"></canvas>

        <div class="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="chip text-xs">
            <span class="text-slate-400/70">Top Attack Country:</span>
            <span class="mono font-semibold" id="topCountry" style="color: var(--teal)">—</span>
          </div>
          <div class="chip text-xs">
            <span class="text-slate-400/70">Top Target Asset:</span>
            <span class="mono font-semibold" id="topAsset" style="color: var(--purple)">—</span>
          </div>
          <div class="chip text-xs">
            <span class="text-slate-400/70">Active Sessions:</span>
            <span class="mono font-semibold" id="activeSessions" style="color: var(--blue)">—</span>
          </div>
        </div>
      </div>

      <!-- Attack Types -->
      <div class="glass2 p-4 xl:col-span-5 lift">
        <div class="flex items-center justify-between mb-3">
          <div>
            <div class="font-semibold">Attack Attempts Breakdown</div>
            <div class="text-xs text-slate-400/80">Events classified (IPS/WAF/EDR/Auth)</div>
          </div>
          <div class="chip text-xs">signal: <span class="mono font-semibold" id="signal" style="color: var(--green)">STABLE</span></div>
        </div>

        <div class="h-[250px]">
          <canvas id="attackChart"></canvas>
        </div>

        <div class="mt-3 grid grid-cols-2 gap-3">
          <div class="chip text-xs">
            <span class="text-slate-400/70">Anomaly Score:</span>
            <span class="mono font-semibold" id="anomaly" style="color: var(--amber)">—</span>
          </div>
          <div class="chip text-xs">
            <span class="text-slate-400/70">Hallucination Risk:</span>
            <span class="mono font-semibold" id="falsePos" style="color: var(--teal)">LOW</span>
          </div>
        </div>
      </div>

      <!-- Suspicious Logins -->
      <div class="glass2 p-4 xl:col-span-6 lift">
        <div class="flex items-center justify-between mb-3">
          <div>
            <div class="font-semibold">Suspicious Logins</div>
            <div class="text-xs text-slate-400/80">Impossible travel • MFA fatigue • TOR/VPN • Unknown devices</div>
          </div>
          <div class="chip text-xs">queue: <span class="mono font-semibold" id="loginQueue" style="color: var(--teal)">—</span></div>
        </div>

        <div class="h-[280px] overflow-auto soft-scroll pr-1" id="loginFeed"></div>
      </div>

      <!-- Blocked IPs -->
      <div class="glass2 p-4 xl:col-span-6 lift">
        <div class="flex items-center justify-between mb-3">
          <div>
            <div class="font-semibold">Blocked IPs</div>
            <div class="text-xs text-slate-400/80">Firewall/WAF/IPS auto-response • threat intel scoring</div>
          </div>
          <div class="chip text-xs">auto-block: <span class="mono font-semibold" style="color: var(--green)">ON</span></div>
        </div>

        <div class="h-[280px] overflow-auto soft-scroll pr-1">
          <table class="w-full text-xs">
            <thead class="sticky top-0" style="background: rgba(2,6,23,.75); backdrop-filter: blur(10px);">
              <tr class="text-slate-300/80">
                <th class="text-left py-2 px-2">IP</th>
                <th class="text-left py-2 px-2">Country</th>
                <th class="text-left py-2 px-2">Reason</th>
                <th class="text-left py-2 px-2">Risk</th>
                <th class="text-left py-2 px-2">Time</th>
              </tr>
            </thead>
            <tbody id="blockedTable"></tbody>
          </table>
        </div>
      </div>

      <!-- Incident Feed -->
      <div class="glass2 p-4 xl:col-span-12 lift">
        <div class="flex items-center justify-between mb-3">
          <div>
            <div class="font-semibold">Incident Feed (Live)</div>
            <div class="text-xs text-slate-400/80">Triage queue • SLA timers • escalation ready</div>
          </div>
          <div class="flex gap-2">
            <button class="chip text-xs lift" id="btnAssign">Assign to me</button>
            <button class="chip text-xs lift" id="btnEscalate" style="border-color: rgba(251,191,36,.22); box-shadow: 0 0 18px rgba(251,191,36,.10);">Escalate</button>
            <button class="chip text-xs lift" id="btnClose" style="border-color: rgba(34,211,153,.18); box-shadow: 0 0 18px rgba(52,211,153,.10);">Close</button>
          </div>
        </div>

        <div class="h-[280px] overflow-auto soft-scroll pr-1" id="incidentFeed"></div>
      </div>
    </div>
  </div>

  <script>
    /***********************
     * Atanu S UI KIT: SOC
     * single HTML + dummy realtime engine
     ***********************/

    const $ = (id) => document.getElementById(id);

    const state = {
      range: "1h",
      tick: 0,
      attacksPerMin: 42,
      suspiciousLogins: 17,
      blockedIps: 83,
      openIncidents: 9,
      slaBreaches: 0,
      mfa: 8,
      waf: 31,

      activeSessions: 3821,
      topCountry: "RU",
      topAsset: "VPN-GW-02",
      signal: "STABLE",
      anomaly: 27,
      hallucination: "LOW",

      loginQueue: 12,

      // chart series
      sparkA: Array.from({length: 24}, () => rand(12, 56)),
      sparkL: Array.from({length: 24}, () => rand(3, 28)),
      sparkB: Array.from({length: 24}, () => rand(8, 50)),
      sparkI: Array.from({length: 24}, () => rand(2, 14))
    };

    const countries = [
      {code:"RU", name:"Russia"}, {code:"CN", name:"China"}, {code:"US", name:"United States"},
      {code:"BR", name:"Brazil"}, {code:"IN", name:"India"}, {code:"DE", name:"Germany"},
      {code:"NL", name:"Netherlands"}, {code:"SG", name:"Singapore"}, {code:"TR", name:"Turkey"},
      {code:"IR", name:"Iran"}, {code:"FR", name:"France"}, {code:"GB", name:"United Kingdom"}
    ];

    const assets = ["VPN-GW-02","AD-DC-01","APP-EDGE-03","SQL-PROD-01","WAF-CLUSTER","K8S-NODE-07","MAIL-EXCH-01","API-GW","AZURE-SSO","JUMP-BOX"];

    const loginReasons = [
      "Impossible travel detected", "MFA fatigue pattern", "Login from TOR exit node",
      "New device fingerprint", "Multiple failed attempts", "Suspicious ASN",
      "Password spray signature", "Legacy auth attempt"
    ];

    const blockReasons = [
      "WAF: SQLi pattern", "WAF: RCE attempt", "IPS: Port scan", "EDR: C2 callback",
      "Rate-limit exceeded", "Auth: brute force", "Threat intel match", "Geo policy block"
    ];

    const incidentTypes = [
      "Credential Stuffing Attack", "Web Exploit Attempt", "Malware Beacon Detected",
      "Suspicious Privilege Escalation", "Data Exfiltration Anomaly", "Impossible Travel + MFA spam",
      "New IOC matched on endpoint", "Brute force on VPN gateway"
    ];

    const severityPool = ["LOW","MED","HIGH","CRITICAL"];
    const severityBadge = (sev) => {
      if(sev==="CRITICAL") return `<span class="badge b-critical">CRITICAL</span>`;
      if(sev==="HIGH") return `<span class="badge b-high">HIGH</span>`;
      if(sev==="MED") return `<span class="badge b-med">MED</span>`;
      return `<span class="badge b-low">LOW</span>`;
    };

    function rand(min, max){ return Math.floor(Math.random()*(max-min+1))+min; }
    function pick(arr){ return arr[Math.floor(Math.random()*arr.length)]; }

    function pad(n){ return String(n).padStart(2,"0"); }
    function utcNow(){
      const d = new Date();
      return `${d.getUTCFullYear()}-${pad(d.getUTCMonth()+1)}-${pad(d.getUTCDate())} ${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())}`;
    }
    function timeShort(){
      const d = new Date();
      return `${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())}Z`;
    }

    // ----- FILTERS -----
    document.querySelectorAll(".filterBtn").forEach(btn=>{
      btn.addEventListener("click", ()=>{
        document.querySelectorAll(".filterBtn").forEach(b=>{
          b.classList.remove("active");
          b.style.borderColor = "rgba(148,163,184,.16)";
          b.style.boxShadow = "none";
        });
        btn.classList.add("active");
        btn.style.borderColor = "rgba(34,211,238,.30)";
        btn.style.boxShadow = "0 0 24px rgba(34,211,238,.18)";

        state.range = btn.dataset.range;
        // small re-seed for realism
        state.attacksPerMin = rand(18, 92);
        state.anomaly = rand(12, 78);
        renderAll();
      });
    });

    // ----- QUICK ACTION buttons -----
    $("btnContain").addEventListener("click", ()=>{
      toast("Containment action triggered: pushed temp WAF rule set + EDR isolate candidates.");
      // reduce open incidents slightly
      state.openIncidents = Math.max(0, state.openIncidents - rand(0,2));
      renderAll();
    });

    $("btnAssign").addEventListener("click", ()=> toast("Assigned top incident to Analyst (You)."));
    $("btnEscalate").addEventListener("click", ()=> toast("Escalated to Tier-2. Added IOC evidence pack."));
    $("btnClose").addEventListener("click", ()=>{
      toast("Incident closed: marked as False Positive with evidence notes.");
      state.openIncidents = Math.max(0, state.openIncidents - 1);
      renderAll();
    });

    // ----- TOAST -----
    const toastBox = document.createElement("div");
    toastBox.className = "fixed bottom-5 left-1/2 -translate-x-1/2 z-[9999] space-y-2";
    document.body.appendChild(toastBox);

    function toast(msg){
      const el = document.createElement("div");
      el.className = "glass2 px-4 py-3 text-sm max-w-[780px] lift";
      el.style.borderColor = "rgba(34,211,238,.18)";
      el.innerHTML = `<div class="flex gap-2 items-start">
        <div class="mt-0.5">🛰️</div>
        <div><div class="font-semibold">SOC Action</div><div class="text-slate-300/80 text-xs mt-0.5">${msg}</div></div>
      </div>`;
      toastBox.appendChild(el);
      setTimeout(()=>{ el.style.opacity="0"; el.style.transform="translateY(6px)"; }, 2800);
      setTimeout(()=> el.remove(), 3300);
    }

    // ----- CHARTS -----
    Chart.defaults.color = "rgba(226,232,240,.82)";
    Chart.defaults.font.family = "ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial";
    Chart.defaults.plugins.legend.labels.usePointStyle = true;

    function sparkConfig(labels, data){
      return {
        type: "line",
        data: {
          labels,
          datasets: [{
            data,
            tension: .35,
            borderWidth: 2,
            pointRadius: 0,
            fill: true,
            borderColor: "rgba(34,211,238,.85)",
            backgroundColor: "rgba(34,211,238,.10)"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { enabled: false } },
          scales: {
            x: { display: false },
            y: { display: false }
          }
        }
      };
    }

    const sparkLabels = Array.from({length: 24}, (_,i)=>i+1);

    const chSparkA = new Chart($("sparkAttempts"), sparkConfig(sparkLabels, state.sparkA));
    const chSparkL = new Chart($("sparkLogins"),  sparkConfig(sparkLabels, state.sparkL));
    const chSparkB = new Chart($("sparkBlocks"),  sparkConfig(sparkLabels, state.sparkB));
    const chSparkI = new Chart($("sparkInc"),     sparkConfig(sparkLabels, state.sparkI));

    // Attack breakdown bar
    const attackTypes = ["Brute Force","Port Scan","Web Exploit","Malware","DDoS","Auth Abuse"];
    const chAttack = new Chart($("attackChart"), {
      type: "bar",
      data: {
        labels: attackTypes,
        datasets: [{
          label: "events",
          data: attackTypes.map(()=>rand(40,220)),
          borderWidth: 1,
          borderColor: "rgba(168,85,247,.55)",
          backgroundColor: "rgba(168,85,247,.12)",
          borderRadius: 10
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display:false },
          tooltip: {
            backgroundColor: "rgba(2,6,23,.92)",
            borderColor: "rgba(148,163,184,.18)",
            borderWidth: 1
          }
        },
        scales: {
          x: {
            grid: { color: "rgba(148,163,184,.08)" }
          },
          y: {
            grid: { color: "rgba(148,163,184,.08)" },
            ticks: { precision:0 }
          }
        }
      }
    });

    // ----- THREAT MAP (Canvas animation) -----
    const map = $("threatMap");
    const ctx = map.getContext("2d");
    let W, H;

    const nodes = [
      // pseudo map anchor points (x,y are normalized)
      {name:"US", x:.18, y:.44}, {name:"EU", x:.46, y:.36}, {name:"IN", x:.64, y:.52},
      {name:"SG", x:.74, y:.62}, {name:"BR", x:.26, y:.70}, {name:"RU", x:.60, y:.28},
      {name:"AU", x:.86, y:.80}, {name:"AF", x:.58, y:.52}
    ];

    const protectedHub = { name:"Protected DC", x:.56, y:.58 };

    let rays = [];
    function resizeMap(){
      const r = map.getBoundingClientRect();
      map.width = Math.floor(r.width * devicePixelRatio);
      map.height = Math.floor(r.height * devicePixelRatio);
      W = map.width; H = map.height;
    }
    window.addEventListener("resize", resizeMap);
    resizeMap();

    function addRay(){
      const origin = pick(nodes);
      const sev = pick(severityPool);
      const col = sev==="CRITICAL" ? "rgba(251,113,133,.85)"
                : sev==="HIGH" ? "rgba(251,191,36,.80)"
                : sev==="MED" ? "rgba(52,211,153,.78)"
                : "rgba(34,211,238,.82)";
      rays.push({
        ox: origin.x*W, oy: origin.y*H,
        tx: protectedHub.x*W, ty: protectedHub.y*H,
        t: 0,
        speed: (0.012 + Math.random()*0.010) * devicePixelRatio,
        col,
        sev
      });
      if(rays.length > 42) rays.shift();
    }

    function drawMap(){
      ctx.clearRect(0,0,W,H);

      // soft stars
      for(let i=0;i<60;i++){
        const x = (i*97 % W);
        const y = (i*191 % H);
        ctx.fillStyle = "rgba(226,232,240,.06)";
        ctx.fillRect(x,y,1*devicePixelRatio,1*devicePixelRatio);
      }

      // draw nodes
      nodes.forEach(n=>{
        const x = n.x*W, y = n.y*H;
        ctx.beginPath();
        ctx.arc(x,y, 3.8*devicePixelRatio, 0, Math.PI*2);
        ctx.fillStyle = "rgba(34,211,238,.38)";
        ctx.fill();
      });

      // protected hub
      ctx.beginPath();
      ctx.arc(protectedHub.x*W, protectedHub.y*H, 6.5*devicePixelRatio, 0, Math.PI*2);
      ctx.fillStyle = "rgba(168,85,247,.38)";
      ctx.fill();

      // rays
      rays.forEach(r=>{
        // line
        ctx.beginPath();
        ctx.moveTo(r.ox, r.oy);
        ctx.lineTo(r.tx, r.ty);
        ctx.strokeStyle = r.col.replace(".85", ".18").replace(".80",".16").replace(".78",".14").replace(".82",".14");
        ctx.lineWidth = 1.2*devicePixelRatio;
        ctx.stroke();

        // moving packet
        const px = r.ox + (r.tx - r.ox) * r.t;
        const py = r.oy + (r.ty - r.oy) * r.t;

        ctx.beginPath();
        ctx.arc(px,py, 2.5*devicePixelRatio, 0, Math.PI*2);
        ctx.fillStyle = r.col;
        ctx.shadowColor = r.col;
        ctx.shadowBlur = 18*devicePixelRatio;
        ctx.fill();
        ctx.shadowBlur = 0;

        r.t += r.speed;
      });

      // cleanup
      rays = rays.filter(r=> r.t < 1.02);

      requestAnimationFrame(drawMap);
    }
    drawMap();

    // ----- FEEDS -----
    function buildLoginItem(){
      const c = pick(countries);
      const user = `user.${rand(10,99)}@tenant.com`;
      const reason = pick(loginReasons);
      const asset = pick(assets);
      const risk = rand(42, 98);
      const mfa = Math.random() < .55;
      const sev = risk > 88 ? "HIGH" : risk > 70 ? "MED" : "LOW";

      return {
        time: timeShort(),
        user,
        country: c.code,
        ip: `${rand(11,223)}.${rand(0,255)}.${rand(0,255)}.${rand(0,255)}`,
        reason,
        asset,
        risk,
        mfa,
        sev
      };
    }

    function loginRow(l){
      return `
        <div class="kpi p-3 mb-2">
          <div class="flex items-start justify-between gap-2">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span class="badge ${l.sev==="HIGH" ? "b-high" : l.sev==="MED" ? "b-med" : "b-low"}">${l.sev}</span>
                <span class="text-xs text-slate-200/90 mono">${l.time}</span>
                <span class="text-xs text-slate-400/80">•</span>
                <span class="text-xs font-semibold">${l.user}</span>
              </div>
              <div class="text-xs text-slate-300/70 mt-1">
                <span class="text-slate-400/70">Reason:</span> ${l.reason}
              </div>
              <div class="text-xs text-slate-300/70 mt-1 flex flex-wrap gap-x-3 gap-y-1">
                <span class="mono"><span class="text-slate-400/70">IP:</span> ${l.ip}</span>
                <span class="mono"><span class="text-slate-400/70">Geo:</span> ${l.country}</span>
                <span class="mono"><span class="text-slate-400/70">Target:</span> ${l.asset}</span>
              </div>
            </div>

            <div class="text-right">
              <div class="text-xs text-slate-400/80">Risk</div>
              <div class="text-lg font-bold mono" style="color:${l.risk>88?'var(--amber)':'var(--teal)'}">${l.risk}</div>
              <div class="text-[11px] mt-1">${l.mfa ? `<span class="badge b-med">MFA</span>` : `<span class="badge b-low">NO-MFA</span>`}</div>
            </div>
          </div>
        </div>
      `;
    }

    function buildBlocked(){
      const c = pick(countries);
      const reason = pick(blockReasons);
      const risk = rand(40, 99);
      return {
        ip: `${rand(11,223)}.${rand(0,255)}.${rand(0,255)}.${rand(0,255)}`,
        country: c.code,
        reason,
        risk,
        time: timeShort()
      };
    }

    function blockedRow(b){
      const badge = b.risk > 88 ? "b-critical" : b.risk > 72 ? "b-high" : b.risk > 56 ? "b-med" : "b-low";
      return `
        <tr class="border-b" style="border-color: rgba(148,163,184,.09)">
          <td class="py-2 px-2 mono text-slate-200/90">${b.ip}</td>
          <td class="py-2 px-2 mono text-slate-300/70">${b.country}</td>
          <td class="py-2 px-2 text-slate-300/70">${b.reason}</td>
          <td class="py-2 px-2"><span class="badge ${badge} mono">${b.risk}</span></td>
          <td class="py-2 px-2 mono text-slate-400/80">${b.time}</td>
        </tr>
      `;
    }

    function buildIncident(){
      const type = pick(incidentTypes);
      const sev = pick(severityPool);
      const id = `INC-${rand(100320, 999980)}`;
      const asset = pick(assets);
      const country = pick(countries).code;
      const status = pick(["NEW","TRIAGE","INVESTIGATING","CONTAINING"]);
      const evidence = rand(3, 22);
      const slaMin = sev==="CRITICAL" ? rand(8, 18) : sev==="HIGH" ? rand(18, 45) : sev==="MED" ? rand(45, 120) : rand(90, 240);

      return {
        id, type, sev, asset, country, status,
        evidence,
        createdAt: Date.now(),
        slaMin
      };
    }

    function incidentRow(inc){
      const elapsedMin = Math.floor((Date.now() - inc.createdAt)/60000);
      const remaining = Math.max(0, inc.slaMin - elapsedMin);
      const breach = remaining === 0;

      const statusColor = inc.status==="NEW" ? "var(--teal)" :
                          inc.status==="TRIAGE" ? "var(--blue)" :
                          inc.status==="INVESTIGATING" ? "var(--amber)" : "var(--red)";

      const slaColor = breach ? "var(--red)" : remaining < 10 ? "var(--amber)" : "var(--green)";
      const slaText = breach ? "BREACH" : `${remaining}m`;

      return `
        <div class="kpi p-4 mb-2">
          <div class="flex flex-col lg:flex-row lg:items-start gap-3 lg:justify-between">
            <div class="min-w-0">
              <div class="flex flex-wrap items-center gap-2">
                ${severityBadge(inc.sev)}
                <span class="mono text-xs text-slate-400/80">${timeShort()}</span>
                <span class="text-xs text-slate-400/70">•</span>
                <span class="text-sm font-semibold mono">${inc.id}</span>
                <span class="text-xs text-slate-400/70">•</span>
                <span class="badge mono" style="color:${statusColor}">${inc.status}</span>
              </div>

              <div class="mt-1 text-sm text-slate-200/90 font-semibold truncate">${inc.type}</div>

              <div class="mt-2 text-xs text-slate-300/70 flex flex-wrap gap-x-4 gap-y-1">
                <span class="mono"><span class="text-slate-400/70">Asset:</span> ${inc.asset}</span>
                <span class="mono"><span class="text-slate-400/70">Geo:</span> ${inc.country}</span>
                <span class="mono"><span class="text-slate-400/70">Evidence:</span> ${inc.evidence} logs</span>
              </div>
            </div>

            <div class="flex gap-3 items-center justify-between lg:justify-end">
              <div class="text-right">
                <div class="text-xs text-slate-400/80">SLA</div>
                <div class="text-2xl font-bold mono" style="color:${slaColor}">${slaText}</div>
              </div>
              <button class="chip text-xs lift" onclick="toast('IOC pack exported + containment ready for ${inc.asset}.')">Action</button>
            </div>
          </div>
        </div>
      `;
    }

    // in-memory feeds
    const loginFeed = [];
    const blockedFeed = [];
    const incidents = [];

    // seed
    for(let i=0;i<10;i++) loginFeed.unshift(buildLoginItem());
    for(let i=0;i<14;i++) blockedFeed.unshift(buildBlocked());
    for(let i=0;i<10;i++) incidents.unshift(buildIncident());

    // ----- RENDER -----
    function renderKPIs(){
      $("kpiAttempts").textContent = state.attacksPerMin;
      $("kpiSpike").textContent = `${rand(-12, 64)}%`;
      $("kpiSuspicious").textContent = state.suspiciousLogins;
      $("kpiMfa").textContent = state.mfa;
      $("kpiBlocked").textContent = state.blockedIps;
      $("kpiWaf").textContent = state.waf;
      $("kpiIncidents").textContent = state.openIncidents;
      $("kpiSla").textContent = state.slaBreaches;

      $("utcTime").textContent = utcNow();
      $("activeSessions").textContent = state.activeSessions.toLocaleString();
      $("topCountry").textContent = state.topCountry;
      $("topAsset").textContent = state.topAsset;
      $("signal").textContent = state.signal;
      $("anomaly").textContent = state.anomaly;

      $("falsePos").textContent = state.hallucination;
      $("loginQueue").textContent = state.loginQueue;

      // threat level
      const tl = state.anomaly > 65 ? "CRITICAL" : state.anomaly > 45 ? "HIGH" : state.anomaly > 25 ? "ELEVATED" : "GUARDED";
      $("threatLevel").textContent = tl;
      $("threatLevel").style.color = tl==="CRITICAL" ? "var(--red)" : tl==="HIGH" ? "var(--amber)" : tl==="ELEVATED" ? "var(--teal)" : "var(--green)";

      $("socHealth").textContent = state.openIncidents > 16 ? "STRAINED" : state.openIncidents > 10 ? "BUSY" : "NORMAL";
      $("socHealth").style.color = state.openIncidents > 16 ? "var(--red)" : state.openIncidents > 10 ? "var(--amber)" : "var(--green)";
    }

    function renderFeeds(){
      $("loginFeed").innerHTML = loginFeed.slice(0, 18).map(loginRow).join("");

      $("blockedTable").innerHTML = blockedFeed.slice(0, 18).map(blockedRow).join("");

      // incident SLA breach count
      let breaches = 0;
      const html = incidents.slice(0, 18).map(inc=>{
        const elapsedMin = Math.floor((Date.now() - inc.createdAt)/60000);
        const remaining = Math.max(0, inc.slaMin - elapsedMin);
        if(remaining === 0) breaches++;
        return incidentRow(inc);
      }).join("");
      $("incidentFeed").innerHTML = html;

      state.slaBreaches = breaches;
    }

    function renderCharts(){
      // sparklines update
      chSparkA.data.datasets[0].data = state.sparkA;
      chSparkL.data.datasets[0].data = state.sparkL;
      chSparkB.data.datasets[0].data = state.sparkB;
      chSparkI.data.datasets[0].data = state.sparkI;
      chSparkA.update(); chSparkL.update(); chSparkB.update(); chSparkI.update();

      // attack chart update
      chAttack.data.datasets[0].data = attackTypes.map(()=>rand(40,240));
      chAttack.update();
    }

    function renderAll(){
      renderKPIs();
      renderFeeds();
      renderCharts();
    }

    // ----- REALTIME ENGINE -----
    function shiftSeries(arr, next){
      arr.push(next);
      if(arr.length > 24) arr.shift();
    }

    function stepEngine(){
      state.tick++;

      $("refreshTick").textContent = `${(state.tick%60)||60}s`;

      // map rays
      const raysToAdd = rand(1, 4);
      for(let i=0;i<raysToAdd;i++) addRay();

      // KPIs drift
      const drift = (v, min, max, step=6) => Math.max(min, Math.min(max, v + rand(-step, step)));

      state.attacksPerMin = drift(state.attacksPerMin, 10, 140, 10);
      state.suspiciousLogins = drift(state.suspiciousLogins, 2, 90, 6);
      state.blockedIps = drift(state.blockedIps, 10, 320, 10);
      state.openIncidents = drift(state.openIncidents, 1, 26, 2);

      state.mfa = drift(state.mfa, 1, 50, 4);
      state.waf = drift(state.waf, 3, 130, 6);

      state.activeSessions = drift(state.activeSessions, 900, 9800, 340);

      // anomaly + signal
      state.anomaly = drift(state.anomaly, 8, 92, 9);
      state.signal = state.anomaly > 72 ? "VOLATILE" : state.anomaly > 45 ? "ACTIVE" : "STABLE";
      state.hallucination = state.anomaly > 82 ? "MED" : "LOW";

      // top country / asset changes
      if(Math.random() < .20) state.topCountry = pick(countries).code;
      if(Math.random() < .18) state.topAsset = pick(assets);

      // sparkline shifting
      shiftSeries(state.sparkA, state.attacksPerMin);
      shiftSeries(state.sparkL, state.suspiciousLogins);
      shiftSeries(state.sparkB, Math.floor(state.blockedIps / 6));
      shiftSeries(state.sparkI, state.openIncidents);

      // feeds additions
      if(Math.random() < .65) loginFeed.unshift(buildLoginItem());
      if(loginFeed.length > 60) loginFeed.pop();

      if(Math.random() < .60) blockedFeed.unshift(buildBlocked());
      if(blockedFeed.length > 80) blockedFeed.pop();

      if(Math.random() < .35) incidents.unshift(buildIncident());
      if(incidents.length > 40) incidents.pop();

      state.loginQueue = Math.max(0, Math.min(38, Math.floor((loginFeed.length/4) + rand(-4, 7))));

      // render
      renderAll();
    }

    renderAll();
    setInterval(stepEngine, 1000);
  </script>
</body>
</html>
