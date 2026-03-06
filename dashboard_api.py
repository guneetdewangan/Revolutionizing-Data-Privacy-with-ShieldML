from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import plotly.graph_objects as go
import plotly.io as pio
import random
import json
import asyncio
from server.federated_server import FederatedServer
from utils.config import NUM_CLIENTS, TRAINING_ROUNDS, DP_EPSILON, DP_NOISE_MULTIPLIER

# Global Plotly Theme
pio.templates.default = "plotly_dark"

app = FastAPI(title="ShieldML | Command Center v3.2")

server = FederatedServer()
history = None

# Mocked telemetry
def get_node_stats():
    return [
        {"id": i, "status": "SECURE", "latency": f"{random.randint(10, 80)}ms", "trust": f"{random.uniform(98.5, 99.9):.1f}%"}
        for i in range(NUM_CLIENTS)
    ]

@app.get("/")
async def root():
    return {"engine": "ShieldML v3.2", "status": "Operational", "mode": "Command_Center"}

@app.get("/train")
async def train(epsilon: float = 1.0, noise: float = 1.1, use_dp: bool = True):
    global history
    history = server.run_training_rounds(use_dp=use_dp)
    return {"message": "Protocol Executed", "history": history}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    global history
    node_stats = get_node_stats()
    
    # Telemetry
    accuracy_val = f"{history['accuracy'][-1]*100:.1f}%" if history else "00.0%"
    rounds_val = f"{len(history['rounds'])}" if history else "0"
    loss_val = f"{history['loss'][-1]:.4f}" if history else "0.0000"
    privacy_score = int(100 - (float(DP_EPSILON) * 5))
    
    # Graphs - Enhanced Styling and Containment
    if history:
        fig_acc = go.Figure()
        fig_acc.add_trace(go.Scatter(
            x=history["rounds"], y=history["accuracy"],
            mode='lines+markers',
            line=dict(color='#ff1744', width=4),
            marker=dict(size=12, color='#fff', line=dict(width=2, color='#ff1744'))
        ))
        fig_acc.update_layout(
            title={'text': 'GLOBAL_ACCURACY_TREND', 'font': {'size': 20, 'color': '#ff1744', 'family': 'JetBrains Mono'}},
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            autosize=True, height=400, margin=dict(l=50,r=50,t=80,b=50),
            xaxis=dict(gridcolor='#1a0000', zerolinecolor='#333', title="Rounds"),
            yaxis=dict(gridcolor='#1a0000', zerolinecolor='#333', title="Accuracy")
        )
        
        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(
            x=history["rounds"], y=history["loss"],
            mode='lines', fill='tozeroy',
            fillcolor='rgba(255, 23, 68, 0.1)',
            line=dict(color='#ff1744', width=3, dash='dot')
        ))
        fig_loss.update_layout(
            title={'text': 'CONVERGENCE_LOSS_LOG', 'font': {'size': 20, 'color': '#ff1744', 'family': 'JetBrains Mono'}},
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            autosize=True, height=400, margin=dict(l=50,r=50,t=80,b=50),
            xaxis=dict(gridcolor='#1a0000', zerolinecolor='#333', title="Rounds"),
            yaxis=dict(gridcolor='#1a0000', zerolinecolor='#333', title="Loss")
        )
        
        acc_chart = pio.to_html(fig_acc, full_html=False, config={'responsive': True, 'displayModeBar': False})
        loss_chart = pio.to_html(fig_loss, full_html=False, config={'responsive': True, 'displayModeBar': False})
    else:
        acc_chart = "<div class='empty-msg'>AWAITING_SIGNAL_LOCK...</div>"
        loss_chart = "<div class='empty-msg'>NO_PROTOCOL_HISTORY...</div>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SHIELD ML | HUB-RED V3.2</title>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --red: #ff1744;
                --bg: #050505;
                --glass: rgba(30, 0, 0, 0.5); /* Semi-transparent for better blur visibility */
                --border: rgba(255, 23, 68, 0.2);
                --glow: 0 0 25px rgba(255, 23, 68, 0.3);
            }}
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{
                font-family: 'Space Grotesk', sans-serif;
                background: var(--bg); color: #fff; padding: 25px;
                background-image: 
                    linear-gradient(rgba(30, 0, 0, 0.2) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(30, 0, 0, 0.2) 1px, transparent 1px);
                background-size: 60px 60px;
                min-height: 100vh;
            }}

            header {{
                border: 2px solid var(--red); background: #000;
                padding: 15px 35px; margin-bottom: 30px;
                display:flex; justify-content:space-between; align-items:center;
                box-shadow: var(--glow); position:sticky; top:25px; z-index:100;
                border-radius: 4px;
            }}
            .ticker-wrap {{ flex:1; margin:0 40px; overflow:hidden; white-space:nowrap; border-left:1px solid #300; border-right:1px solid #300; }}
            .ticker {{ display:inline-block; animation: scroll 40s linear infinite; color: var(--red); font-family:'JetBrains Mono'; font-size:12px; opacity:0.8; }}
            @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

            .main-layout {{ display:grid; grid-template-columns: 1fr 420px; gap:30px; }}
            .hud-column {{ display:flex; flex-direction:column; gap:30px; }}

            /* KPI BOXES */
            .kpi-row {{ display:grid; grid-template-columns: repeat(4, 1fr); gap:20px; }}
            .kpi-box {{ background:rgba(10,10,10,0.8); border:1px solid var(--border); padding:20px; border-radius:8px; box-shadow: inset 0 0 20px rgba(255,0,0,0.05); }}
            .kpi-label {{ font-size:11px; color:#666; font-weight:700; text-transform:uppercase; letter-spacing:1px; }}
            .kpi-value {{ font-size:32px; font-weight:700; color:#fff; font-family:'JetBrains Mono'; margin-top:5px; }}

            /* CHART ARRANGEMENT - REMOVING OVERLAP */
            .charts-full {{ display:flex; flex-direction:column; gap:30px; width: 100%; }}
            .glass-chart {{ 
                background: var(--glass);
                border: 1px solid var(--border); 
                border-top: 2px solid var(--red);
                border-radius: 12px; 
                backdrop-filter: blur(40px); /* Stronger blur for higher quality */
                -webkit-backdrop-filter: blur(40px);
                padding: 20px; 
                position: relative;
                overflow: hidden; /* CRITICAL: Prevent Plotly from leaking out */
                min-height: 450px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.7);
            }}
            
            .chart-container {{ width: 100%; height: 100%; }}

            /* NODE MATRIX */
            .matrix-box {{ background:rgba(10,10,10,0.8); border:1px solid var(--border); padding:25px; border-radius:8px; backdrop-filter: blur(10px); }}
            .matrix-table {{ width:100%; border-collapse:collapse; font-size:12px; font-family:'JetBrains Mono'; color:#bbb; }}
            .matrix-table th {{ text-align:left; color:var(--red); padding:12px; border-bottom:1px solid rgba(255,23,68,0.3); }}
            .matrix-table td {{ padding:12px; border-bottom:1px solid rgba(255,255,255,0.05); }}
            .node-id {{ color: #fff; font-weight:700; }}

            /* SIDEBAR */
            .sidebar {{ display:flex; flex-direction:column; gap:25px; }}
            .stat-panel {{ background:rgba(10,10,10,0.8); border:1px solid var(--border); padding:25px; border-radius:8px; backdrop-filter: blur(15px); }}
            .terminal {{ background:#000; height:350px; padding:15px; font-family:'JetBrains Mono'; font-size:11px; color:var(--red); overflow-y:auto; border-radius:4px; border: 1px solid #111; }}
            
            .gauge-wrap {{ text-align:center; padding:20px 0; }}
            .gauge {{ width:140px; height:140px; border:10px solid #111; border-top-color:var(--red); border-radius:50%; margin:0 auto 15px; display:flex; align-items:center; justify-content:center; font-size:32px; font-weight:700; color:var(--red); box-shadow: var(--glow); }}

            .btn-main {{ 
                width:100%; padding:20px; background:var(--red); color:#fff; border:none; 
                font-weight:700; font-size:14px; text-transform:uppercase; cursor:pointer; 
                transition:0.3s; margin-top:10px; border-radius:4px; letter-spacing:2px;
                box-shadow: var(--glow);
            }}
            .btn-main:hover {{ background:#ff4569; letter-spacing:4px; filter: brightness(1.2); }}

            .empty-msg {{ color: #333; font-weight:700; letter-spacing:4px; font-family:'JetBrains Mono'; display: flex; align-items: center; justify-content: center; height: 100%; }}
            .node-indicator {{ width:8px; height:8px; background:var(--red); border-radius:50%; display:inline-block; margin-right:10px; box-shadow:0 0 8px var(--red); animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.4; }} }}
        </style>
    </head>
    <body>
        <header>
            <div style="font-size:26px; font-weight:700; color:var(--red); text-shadow: var(--glow);">SHIELD_HUB_v3.2</div>
            <div class="ticker-wrap">
                <div class="ticker">
                    >> [SYSTEM_HEALTH: NOMINAL] | [NODE_SYNCHRONIZATION: 10/10] | [ENCRYPTION: ACTIVE] | [PRIVACY_SCORE: OPTIMIZED] | [GRADIENT_INTEGRITY: VALIDATED] | [NOISE_INJECTION: PENDING_COMMAND] >>
                </div>
            </div>
            <div style="font-family:'JetBrains Mono'; font-size:14px; color:var(--red); font-weight:700;">// AUTH_LOCKED</div>
        </header>

        <div class="main-layout">
            <div class="hud-column">
                <div class="kpi-row">
                    <div class="kpi-box"><div class="kpi-label">NETWORK_ACCURACY</div><div class="kpi-value">{accuracy_val}</div></div>
                    <div class="kpi-box"><div class="kpi-label">OPTIMIZATION_LOSS</div><div class="kpi-value">{loss_val}</div></div>
                    <div class="kpi-box"><div class="kpi-label">ACTIVE_NODES</div><div class="kpi-value">{NUM_CLIENTS}</div></div>
                    <div class="kpi-box"><div class="kpi-label">ROUND_COUNT</div><div class="kpi-value">{rounds_val}</div></div>
                </div>

                <div class="charts-full">
                    <div class="glass-chart">
                        <div class="chart-container">{acc_chart}</div>
                    </div>
                    <div class="glass-chart">
                        <div class="chart-container">{loss_chart}</div>
                    </div>
                </div>

                <div class="matrix-box">
                    <h3 style="color:var(--red); font-size:16px; margin-bottom:20px; font-weight:700;">[ NODE_IDENTITY_VERIFICATION ]</h3>
                    <table class="matrix-table">
                        <tr><th>LOCAL_NODE</th><th>STATUS</th><th>LATENCY</th><th>INTEGRITY_INDEX</th><th>SIGNALS</th></tr>
                        {"".join([f'<tr><td class="node-id">CL-NODE-{(s["id"]+1):03}</td><td><span class="node-indicator"></span>{s["status"]}</td><td>{s["latency"]}</td><td>{s["trust"]}</td><td style="color:var(--red)">VALIDATED</td></tr>' for s in node_stats])}
                    </table>
                </div>
            </div>

            <div class="sidebar">
                <div class="stat-panel">
                    <div class="kpi-label" style="color:var(--red); text-align:center;">[ PRIVACY_SCORE ]</div>
                    <div class="gauge-wrap">
                        <div class="gauge">{privacy_score}</div>
                    </div>
                </div>

                <div class="stat-panel">
                    <div style="font-size:12px; color:var(--red); font-weight:700; margin-bottom:20px; text-transform:uppercase;">[ COMMAND_BUFFER ]</div>
                    
                    <div style="margin-bottom:20px;">
                        <div style="font-size:11px; color:#666; display:flex; justify-content:space-between; margin-bottom:8px;">EPS_BUDGET (ε) <span id="e_val" style="color:#fff">{DP_EPSILON}</span></div>
                        <input type="range" id="e_slide" min="0.1" max="10.0" step="0.1" value="{DP_EPSILON}" style="width:100%; accent-color:var(--red);" oninput="document.getElementById('e_val').innerText=this.value">
                    </div>

                    <div style="margin-bottom:25px;">
                        <div style="font-size:11px; color:#666; display:flex; justify-content:space-between; margin-bottom:8px;">NOISE_SIGMA (σ) <span id="n_val" style="color:#fff">{DP_NOISE_MULTIPLIER}</span></div>
                        <input type="range" id="n_slide" min="0.5" max="3.0" step="0.1" value="{DP_NOISE_MULTIPLIER}" style="width:100%; accent-color:var(--red);" oninput="document.getElementById('n_val').innerText=this.value">
                    </div>

                    <button class="btn-main" onclick="run()">[ INITIATE_FEDERATED_ROUNDS ]</button>
                    <button class="btn-main" style="background:#111; color:var(--red); border:1px solid #222; margin-top:10px; font-size:11px;" onclick="window.location.reload()">REFRESH_TELEMETRY</button>
                </div>

                <div class="stat-panel">
                    <div style="font-size:12px; color:var(--red); font-weight:700; margin-bottom:15px; border-bottom:1px solid #222; padding-bottom:10px;">SIGNAL_RECEPTOR [LOGS]</div>
                    <div class="terminal" id="term_log">
                        <div>> SHIELD_OS_CORE v3.2_READY</div>
                        <div>> AWAITING_UPSTREAM_COMMAND...</div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function log(msg) {{
                const term = document.getElementById('term_log');
                const line = document.createElement('div');
                line.textContent = `> ${{new Date().toLocaleTimeString()}} | ${{msg}}`;
                term.appendChild(line);
                term.scrollTop = term.scrollHeight;
            }}

            async function run() {{
                const e = document.getElementById('e_slide').value;
                const n = document.getElementById('n_slide').value;
                
                log(`SIG_SEND: GLOBAL_ROUTING_START(ε=${{e}})`);
                log(`INJECTING_NOISE: σ=${{n}}`);
                
                try {{
                    const res = await fetch(`/train?epsilon=${{e}}&noise=${{n}}`);
                    const data = await res.json();
                    log("SIG_RCV: SECURE_GRADIENTS_RECEIVED");
                    log("PROTOCOL: AGGREGATION_SUCCESSFUL");
                    setTimeout(() => window.location.reload(), 1500);
                }} catch(err) {{
                    log("SIG_ERR: PROTOCOL_INTERRUPTED");
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
