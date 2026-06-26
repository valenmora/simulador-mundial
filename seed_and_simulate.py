import json
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from main import app

BASE_DIR = Path(__file__).parent
DIST_DIR = BASE_DIR / "dist"
DATA_DIR = DIST_DIR / "data"
IMAGES_DIR = DIST_DIR / "images"
STATIC_IMAGES = BASE_DIR / "static" / "images"


def ensure_dirs():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def run_simulation(client):
    res = client.post("/simulator/run")
    res.raise_for_status()
    return res.json()


def fetch_dashboard(client):
    res = client.get("/metrics/dashboard")
    if res.status_code == 200:
        return res.json()
    return {}


def fetch_teams(client):
    res = client.get("/teams/")
    if res.status_code == 200:
        return res.json()
    return []


def fetch_players(client):
    res = client.get("/players/")
    if res.status_code == 200:
        return res.json()
    return []


def save_json(data, filename):
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def copy_images():
    if STATIC_IMAGES.exists():
        for img in STATIC_IMAGES.iterdir():
            if img.is_file():
                shutil.copy2(img, IMAGES_DIR / img.name)
        print(f"Images copied: {len(list(STATIC_IMAGES.iterdir()))}")


def build_html(simulation, dashboard, teams, players):
    champion = simulation.get("champion", "Desconocido")
    groups = simulation.get("groups", [])
    bracket_rounds = [
        ("round_of_16", "Octavos de Final", "round-of-16"),
        ("quarterfinals", "Cuartos de Final", "quarterfinals"),
        ("semifinals", "Semifinales", "semifinals"),
    ]
    third_place = simulation.get("third_place")
    final = simulation.get("final", {})
    top_scorer = dashboard.get("top_scorer", {})
    champion_name = top_scorer.get("player_name", "-")
    champion_team = top_scorer.get("team_name", "-")
    champion_goals = top_scorer.get("goals", 0)

    total_goals = 0
    total_matches = 0
    if dashboard:
        total_goals = dashboard.get("total_goals", 0)
        total_matches = dashboard.get("total_matches", 0)
    else:
        for g in groups:
            for m in g.get("matches", []):
                total_goals += m.get("home_goals", 0) + m.get("away_goals", 0)
                total_matches += 1

    avg_goals = round(total_goals / total_matches, 2) if total_matches else 0

    def render_groups():
        html = '<div class="row g-3">'
        for g in groups:
            gn = g.get("group", "?")
            standings = g.get("standings", [])
            html += f'''
            <div class="col-md-3 col-sm-6">
              <div class="group-card">
                <div class="group-header">Grupo {gn}</div>
                <table class="group-table">
                  <thead><tr><th>#</th><th>Equipo</th><th>Pts</th><th>GF</th><th>GA</th><th>DG</th></tr></thead>
                  <tbody>'''
            for s in standings:
                pos = s.get("position", 0)
                pc = "pos-1" if pos == 1 else ("pos-2" if pos == 2 else "pos-3")
                cls_row = "qualified" if pos <= 2 else "eliminated"
                gd = s.get("gd", 0)
                gd_str = f"+{gd}" if gd >= 0 else str(gd)
                html += f'''
                    <tr class="{cls_row}">
                      <td><span class="position-badge {pc}">{pos}</span></td>
                      <td><span class="team-name" title="{s.get('team', '')}">{s.get("team", "")}</span></td>
                      <td><strong>{s.get("pts", 0)}</strong></td>
                      <td>{s.get("gf", 0)}</td>
                      <td>{s.get("ga", 0)}</td>
                      <td>{gd_str}</td>
                    </tr>'''
            html += '''
                  </tbody>
                </table>
              </div>
            </div>'''
        html += "</div>"
        return html

    def render_match_row(m):
        home = m.get("home_team", "?")
        away = m.get("away_team", "?")
        hg = m.get("home_goals", 0)
        ag = m.get("away_goals", 0)
        winner = m.get("winner", "")
        hw = "winner" if winner == home else ""
        aw = "winner" if winner == away else ""
        return f'''
            <div class="match-card">
              <div class="match-teams">
                <div class="team {hw}">
                  <span class="team-label">{home}</span>
                  <span class="match-score">{hg}</span>
                </div>
                <div class="team {aw}">
                  <span class="team-label">{away}</span>
                  <span class="match-score">{ag}</span>
                </div>
              </div>
            </div>'''

    def render_bracket():
        html = ""
        for key, label, cls in bracket_rounds:
            matches = simulation.get(key, [])
            if not matches:
                continue
            html += f'''
            <div class="knockout-section {cls}">
              <div class="round-header">{label}</div>
              <div class="row">'''
            for m in matches:
                html += f'<div class="col-12 mb-2">{render_match_row(m)}</div>'
            html += "</div></div>"

        if third_place:
            html += f'''
            <div class="knockout-section third-place">
              <div class="round-header">Tercer Puesto</div>
              <div class="row justify-content-center">
                <div class="col-md-4">{render_match_row(third_place)}</div>
              </div>
            </div>'''

        html += f'''
            <div class="knockout-section final-round">
              <div class="round-header">Final</div>
              <div class="row justify-content-center">
                <div class="col-md-5">{render_match_row(final)}</div>
              </div>
            </div>'''
        return html

    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Simulador Mundial 2026</title>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  <style>
    @font-face {{
      font-family: 'Inter'; font-style: normal; font-weight: 400; font-display: swap;
      src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf) format('truetype');
    }}
    @font-face {{
      font-family: 'Inter'; font-style: normal; font-weight: 500; font-display: swap;
      src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuI6fMZg.ttf) format('truetype');
    }}
    @font-face {{
      font-family: 'Inter'; font-style: normal; font-weight: 600; font-display: swap;
      src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYMZg.ttf) format('truetype');
    }}
    @font-face {{
      font-family: 'Inter'; font-style: normal; font-weight: 700; font-display: swap;
      src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf) format('truetype');
    }}
    @font-face {{
      font-family: 'Poppins'; font-style: normal; font-weight: 500; font-display: swap;
      src: url(https://fonts.gstatic.com/s/poppins/v24/pxiByp8kv8JHgFVrLGT9V1s.ttf) format('truetype');
    }}
    @font-face {{
      font-family: 'Poppins'; font-style: normal; font-weight: 600; font-display: swap;
      src: url(https://fonts.gstatic.com/s/poppins/v24/pxiByp8kv8JHgFVrLEj6V1s.ttf) format('truetype');
    }}
    @font-face {{
      font-family: 'Poppins'; font-style: normal; font-weight: 700; font-display: swap;
      src: url(https://fonts.gstatic.com/s/poppins/v24/pxiByp8kv8JHgFVrLCz7V1s.ttf) format('truetype');
    }}
    :root {{
      --cda-primary: #0056a7;
      --cda-primary-dark: #003d7a;
      --cda-secondary: #0096d6;
      --cda-accent: #00a8e0;
      --cda-dark: #002b54;
      --cda-white: #ffffff;
      --cda-light-bg: #f0f4f8;
      --cda-card-bg: #ffffff;
      --cda-text: #1a2332;
      --cda-text-light: #5e6f8d;
      --cda-border: #d0d8e3;
      --cda-border-light: #e8ecf2;
      --cda-success: #16a34a;
      --cda-danger: #dc2626;
      --cda-shadow-sm: 0 1px 3px rgba(0, 30, 60, 0.08);
      --cda-shadow: 0 4px 16px rgba(0, 30, 60, 0.1);
      --cda-shadow-lg: 0 8px 32px rgba(0, 30, 60, 0.12);
      --cda-radius-sm: 4px;
      --cda-radius: 8px;
      --cda-radius-lg: 12px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      background: var(--cda-light-bg);
      color: var(--cda-text);
      font-family: "Inter", "Poppins", system-ui, sans-serif;
      margin: 0;
      min-height: 100vh;
    }}
    .top-bar {{
      background: var(--cda-white);
      border-bottom: 1px solid var(--cda-border-light);
      padding: 0.5rem 0;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .top-bar .navbar-brand {{
      font-family: "Poppins", sans-serif;
      font-weight: 600;
      font-size: 1rem;
      color: var(--cda-text);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .top-bar .navbar-brand img {{ height: 36px; width: auto; }}
    .top-bar .navbar-brand .brand-divider {{
      width: 1px; height: 28px; background: var(--cda-border);
    }}
    .top-bar .navbar-brand .brand-sub {{
      font-weight: 400; font-size: 0.85rem; color: var(--cda-text-light);
    }}
    .hero {{
      background: linear-gradient(135deg, var(--cda-primary) 0%, var(--cda-dark) 100%);
      padding: 3.5rem 0 3rem;
      text-align: center;
      position: relative;
      overflow: hidden;
    }}
    .hero h1 {{
      font-family: "Poppins", sans-serif;
      font-weight: 700;
      font-size: 2.4rem;
      color: var(--cda-white);
    }}
    .hero h1 .highlight {{ color: var(--cda-accent); }}
    .hero p {{ font-size: 1.05rem; color: rgba(255,255,255,0.8); }}
    .section-title {{
      font-family: "Poppins", sans-serif;
      font-weight: 600;
      font-size: 1.3rem;
      color: var(--cda-text);
      text-align: center;
      margin-bottom: 1.25rem;
    }}
    .section-title::after {{
      content: ""; display: block; width: 50px; height: 3px;
      background: var(--cda-primary); margin: 0.5rem auto 0; border-radius: 2px;
    }}
    .group-card {{
      background: var(--cda-card-bg);
      border: 1px solid var(--cda-border-light);
      border-radius: var(--cda-radius);
      overflow: hidden;
      box-shadow: var(--cda-shadow-sm);
    }}
    .group-header {{
      background: var(--cda-primary);
      padding: 0.6rem 1rem;
      font-weight: 700;
      font-size: 0.85rem;
      letter-spacing: 1.5px;
      color: var(--cda-white);
      text-transform: uppercase;
    }}
    .group-table {{ margin: 0; width: 100%; border-collapse: collapse; table-layout: fixed; }}
    .group-table td:nth-child(2) {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .group-table th {{
      border: none; color: var(--cda-text-light); font-weight: 600;
      font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px;
      padding: 0.45rem 0.6rem; border-bottom: 1px solid var(--cda-border-light);
      background: var(--cda-light-bg);
    }}
    .group-table td {{
      border: none; color: var(--cda-text); padding: 0.45rem 0.6rem;
      font-size: 0.8rem; font-weight: 500;
      border-bottom: 1px solid var(--cda-border-light);
    }}
    .group-table .eliminated {{ opacity: 0.35; }}
    .position-badge {{
      display: inline-flex; align-items: center; justify-content: center;
      width: 22px; height: 22px; border-radius: 50%;
      font-size: 0.65rem; font-weight: 700;
    }}
    .pos-1 {{ background: var(--cda-primary); color: var(--cda-white); }}
    .pos-2 {{ background: var(--cda-secondary); color: var(--cda-white); }}
    .pos-3, .pos-4 {{ background: var(--cda-border-light); color: var(--cda-text-light); }}
    .round-header {{
      text-align: center; font-weight: 700; font-size: 0.8rem;
      text-transform: uppercase; letter-spacing: 2px;
      padding: 0.5rem 0; margin-bottom: 0.75rem; border-radius: var(--cda-radius-sm);
      color: var(--cda-white);
    }}
    .round-of-16 .round-header {{ background: var(--cda-primary); }}
    .quarterfinals .round-header {{ background: var(--cda-secondary); }}
    .semifinals .round-header {{ background: #1a7a4a; }}
    .final-round .round-header {{ background: var(--cda-dark); font-size: 0.9rem; }}
    .third-place .round-header {{ background: var(--cda-text-light); }}
    .match-card {{
      background: var(--cda-card-bg);
      border: 1px solid var(--cda-border-light);
      border-radius: var(--cda-radius);
      padding: 0.55rem 0.85rem;
      margin-bottom: 0.5rem;
      box-shadow: var(--cda-shadow-sm);
    }}
    .match-teams .team {{
      display: flex; justify-content: space-between; align-items: center;
      padding: 0.15rem 0; font-size: 0.8rem;
    }}
    .match-teams .team .team-label {{
      font-weight: 500; color: var(--cda-text);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }}
    .match-teams .team.winner .team-label {{
      font-weight: 700; color: var(--cda-primary);
    }}
    .match-score {{
      font-family: "Poppins", sans-serif;
      font-weight: 600; font-size: 0.95rem;
      min-width: 34px; text-align: center;
      background: var(--cda-light-bg);
      padding: 0.1rem 0.3rem; border-radius: var(--cda-radius-sm);
    }}
    .match-teams .team.winner .match-score {{
      background: rgba(0,86,167,0.1); color: var(--cda-primary);
    }}
    .champion-banner {{
      background: linear-gradient(135deg, var(--cda-primary) 0%, var(--cda-dark) 100%);
      border-radius: var(--cda-radius-lg);
      padding: 2rem; text-align: center; margin: 2rem 0; position: relative; overflow: hidden;
    }}
    .champion-banner .champion-name {{
      font-family: "Poppins", sans-serif;
      font-weight: 700; font-size: 2rem; color: var(--cda-white);
    }}
    .champion-banner .champion-sub {{
      font-size: 0.85rem; color: rgba(255,255,255,0.75);
    }}
    .dashboard-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem; margin: 1.5rem 0;
    }}
    .kpi-card {{
      background: var(--cda-card-bg);
      border: 1px solid var(--cda-border-light);
      border-radius: var(--cda-radius);
      padding: 1.25rem 1rem; text-align: center;
      box-shadow: var(--cda-shadow-sm);
    }}
    .kpi-card .kpi-icon {{ font-size: 1.6rem; margin-bottom: 0.35rem; }}
    .kpi-card .kpi-value {{
      font-family: "Poppins", sans-serif;
      font-weight: 700; font-size: 1.3rem; color: var(--cda-primary);
    }}
    .kpi-card .kpi-label {{
      font-size: 0.7rem; color: var(--cda-text-light);
      text-transform: uppercase; letter-spacing: 0.8px;
    }}
    .kpi-card .kpi-sub {{ font-size: 0.75rem; color: var(--cda-text-light); }}
    .kpi-card.accent-gold {{ border-top: 3px solid #d4a017; }}
    .kpi-card.accent-blue {{ border-top: 3px solid var(--cda-primary); }}
    .kpi-card.accent-green {{ border-top: 3px solid var(--cda-success); }}
    .kpi-card.accent-secondary {{ border-top: 3px solid var(--cda-secondary); }}
    .stats-bar {{
      display: flex; justify-content: center; gap: 2.5rem;
      flex-wrap: wrap; margin: 1.25rem 0;
    }}
    .stat-item {{ text-align: center; }}
    .stat-item .stat-value {{
      font-family: "Poppins", sans-serif;
      font-weight: 700; font-size: 1.4rem; color: var(--cda-primary);
    }}
    .stat-item .stat-label {{
      font-size: 0.7rem; color: var(--cda-text-light);
      text-transform: uppercase; letter-spacing: 1px;
    }}
    hr.divider {{ border: none; height: 1px; background: var(--cda-border-light); margin: 2rem 0; }}
    .footer-cda {{
      background: var(--cda-dark); padding: 1.5rem 0; margin-top: 3rem; text-align: center;
    }}
    .footer-cda .footer-text {{
      color: rgba(255,255,255,0.5); font-size: 0.75rem;
    }}
    .knockout-section {{ margin-top: 1.5rem; }}
    .third-place {{ opacity: 0.65; }}
    @media (max-width: 768px) {{
      .hero h1 {{ font-size: 1.6rem; }}
      .stats-bar {{ gap: 1.25rem; }}
      .champion-banner .champion-name {{ font-size: 1.4rem; }}
      .top-bar .navbar-brand .brand-sub {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="top-bar">
    <div class="container">
      <a class="navbar-brand" href="#">
        <img src="images/logo-color.png" alt="CDA">
        <span class="brand-divider"></span>
        <span>Simulador Mundial 2026</span>
        <span class="brand-sub">| CDA Soluciones Confiables</span>
      </a>
    </div>
  </div>

  <div class="hero">
    <div class="container">
      <h1>Simulador Mundial <span class="highlight">2026</span></h1>
      <p>Resultado de la simulacion &mdash; por CDA Soluciones Confiables</p>
    </div>
  </div>

  <div class="container py-4">
    <div id="teamsSection">
      <h3 class="section-title">Equipos</h3>
      <div id="teamsContainer" class="row g-3">{render_teams(teams)}</div>
    </div>

    <hr class="divider">

    <div id="squadsSection">
      <h3 class="section-title">Plantillas</h3>
      <div id="squadsContainer">{render_squads(teams, players)}</div>
    </div>

    <hr class="divider">

    <h2 class="section-title">Resultados del Torneo</h2>

    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">{len(groups) * 4}</div>
        <div class="stat-label">Equipos</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{total_goals}</div>
        <div class="stat-label">Goles Totales</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{total_matches}</div>
        <div class="stat-label">Partidos</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{champion}</div>
        <div class="stat-label">Campeon</div>
      </div>
    </div>

    <h3 class="section-title">Fase de Grupos</h3>
    {render_groups()}

    <hr class="divider">

    <div id="bracketResult">{render_bracket()}</div>

    <div class="champion-banner">
      <div class="champion-name">{champion}</div>
      <div class="champion-sub">Campeon del Mundo 2026</div>
    </div>

    <hr class="divider">

    <h3 class="section-title">Dashboard Ejecutivo</h3>
    <div class="dashboard-grid">
      <div class="kpi-card accent-gold">
        <div class="kpi-icon">🏆</div>
        <div class="kpi-value">{champion}</div>
        <div class="kpi-label">Campeon</div>
      </div>
      <div class="kpi-card accent-blue">
        <div class="kpi-icon">⚽</div>
        <div class="kpi-value">{champion_name}</div>
        <div class="kpi-label">Boton de Oro</div>
        <div class="kpi-sub">{champion_team} &middot; {champion_goals} goles</div>
      </div>
      <div class="kpi-card accent-green">
        <div class="kpi-icon">📊</div>
        <div class="kpi-value">{avg_goals}</div>
        <div class="kpi-label">Prom. Goles/Partido</div>
      </div>
      <div class="kpi-card accent-secondary">
        <div class="kpi-icon">🥅</div>
        <div class="kpi-value">{total_goals}</div>
        <div class="kpi-label">Goles Totales</div>
        <div class="kpi-sub">en {total_matches} partidos</div>
      </div>
    </div>
  </div>

  <div class="footer-cda">
    <div class="container">
      <div class="footer-text">CDA Informatica &mdash; Todos los derechos reservados</div>
    </div>
  </div>
</body>
</html>'''
    return html_content, champion


def render_teams(teams):
    if not teams:
        return '<div class="col-12"><div class="alert alert-info">No hay equipos cargados.</div></div>'
    groups = {}
    for t in teams:
        g = t.get("group_name") or "X"
        groups.setdefault(g, []).append(t)
    html = ""
    for letter in sorted(groups):
        gteams = groups[letter]
        html += f'''
        <div class="col-md-3 col-sm-6">
          <div class="group-card">
            <div class="group-header">Grupo {letter}</div>
            <table class="group-table">
              <thead><tr><th></th><th>Equipo</th><th>Cod.</th></tr></thead>
              <tbody>'''
        for i, t in enumerate(gteams):
            cls_row = "qualified" if i < 2 else "eliminated"
            pc = "pos-1" if i == 0 else ("pos-2" if i == 1 else "pos-3")
            html += f'''
                <tr class="{cls_row}">
                  <td><span class="position-badge {pc}">{i + 1}</span></td>
                  <td><span class="team-name">{t.get("name", "")}</span></td>
                  <td>{t.get("code", "")}</td>
                </tr>'''
        html += '''
              </tbody>
            </table>
          </div>
        </div>'''
    return html


def render_squads(teams, players):
    if not teams or not players:
        return '<div class="alert alert-info">No hay datos de plantillas.</div>'
    team_map = {t["id"]: t["name"] for t in teams}
    squad_groups = {}
    for p in players:
        tid = p["team_id"]
        squad_groups.setdefault(tid, []).append(p)

    def position_badge(pos):
        colors = {"GK": "#dc3545", "DF": "#0d6efd", "MF": "#198754", "FW": "#ffc107"}
        c = colors.get(pos, "#6c757d")
        return f'<span style="background:{c};color:#000;font-size:0.65rem;padding:0.1rem 0.45rem;border-radius:3px;font-weight:600;">{pos}</span>'

    html = '<div class="row g-3">'
    for tid in sorted(squad_groups):
        tname = team_map.get(tid, f"Equipo {tid}")
        player_list = squad_groups[tid]
        rows = "".join(
            f'<tr><td style="padding:0.25rem 0.5rem;font-size:0.8rem;">{p["name"]}</td><td style="padding:0.25rem 0.5rem;">{position_badge(p["position"])}</td></tr>'
            for p in player_list
        )
        html += f'''
        <div class="col-md-3 col-sm-6">
          <div class="group-card">
            <div class="group-header" style="font-size:0.75rem;">{tname}</div>
            <table class="group-table">
              <thead><tr><th>Jugador</th><th>Pos.</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
        </div>'''
    html += "</div>"
    return html


def main():
    print("=" * 60)
    print("Simulador Mundial 2026 - Generacion de sitio estatico")
    print("=" * 60)

    worldcup_db = BASE_DIR / "worldcup.db"
    if worldcup_db.exists():
        worldcup_db.unlink()
        print("  Base de datos local limpiada")

    ensure_dirs()

    client = TestClient(app)

    print("\n[1/5] Ejecutando simulacion...")
    simulation = run_simulation(client)
    champion = simulation.get("champion", "Desconocido")
    print(f"  Simulacion completada. Campeon: {champion}")

    print("\n[2/5] Obteniendo dashboard, equipos y jugadores...")
    dashboard = fetch_dashboard(client)
    teams = fetch_teams(client)
    players = fetch_players(client)
    print(f"  Dashboard: {len(dashboard)} metricas")
    print(f"  Equipos: {len(teams)}")
    print(f"  Jugadores: {len(players)}")

    print("\n[3/5] Guardando archivos...")
    save_json(simulation, "simulation.json")
    save_json(dashboard, "dashboard.json")
    save_json(teams, "teams.json")
    save_json(players, "players.json")
    copy_images()
    print("  JSON guardados en dist/data/")
    print("  Imagenes copiadas a dist/images/")

    print("\n[4/5] Generando HTML estatico...")
    html, champion = build_html(simulation, dashboard, teams, players)
    (DIST_DIR / "index.html").write_text(html, encoding="utf-8")
    print("  dist/index.html generado")

    print("\n[5/5] Verificando archivos...")
    files = ["index.html", "data/simulation.json", "data/dashboard.json", "data/teams.json", "data/players.json"]
    for f in files:
        p = DIST_DIR / f
        print(f"  {'[OK]' if p.exists() else '[MISSING]'} {f}")

    print("\n" + "=" * 60)
    print(f"  CAMPEON DEL MUNDO 2026: {champion}")
    print("=" * 60)
    print("\nSitio estatico generado en: dist/")
    print("  dist/index.html")
    print("  dist/data/simulation.json")
    print("  dist/data/dashboard.json")
    print("  dist/data/teams.json")
    print("  dist/data/players.json")
    print("  dist/images/")


if __name__ == "__main__":
    main()
