import allure
import urllib.request
import json

BASE = "http://localhost:8001"


# =============================================================================
# SMOKE TEST FRONTEND — SIMULADOR MUNDIAL 2026
# =============================================================================

@allure.feature("Smoke Test Frontend")
@allure.story("Carga y navegación")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SMK-01: La aplicación carga correctamente")
@allure.label("smoke", "carga")
@allure.tag("frontend", "smoke", "carga")
def test_smk_01_app_loads():
    r = urllib.request.urlopen(f"{BASE}/", timeout=10)
    body = r.read().decode()
    with allure.step("HTTP 200"):
        assert r.status == 200
    with allure.step("Título 'Simulador Mundial 2026' presente"):
        assert "Simulador Mundial 2026" in body
    with allure.step("Botón #btnSimular presente"):
        assert "btnSimular" in body
    with allure.step("Spinner #spinner presente"):
        assert "spinner" in body
    with allure.step("Sección #resultsSection presente"):
        assert "resultsSection" in body
    with allure.step("Contenedor #teamsContainer presente"):
        assert "teamsContainer" in body
    with allure.step("Dashboard #dashboardResult presente"):
        assert "dashboardResult" in body
    with allure.step("Stats bar #statsBar presente"):
        assert "statsBar" in body
    allure.attach(body[:1000], "HTML preview (first 1KB)", allure.attachment_type.TEXT)


@allure.feature("Smoke Test Frontend")
@allure.story("Interacción usuario")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SMK-02: Botón Simular y Spinner funcionan")
@allure.label("smoke", "interacción")
@allure.tag("frontend", "smoke", "boton")
def test_smk_02_button_and_spinner():
    r = urllib.request.urlopen(f"{BASE}/", timeout=10)
    body = r.read().decode()
    with allure.step("JavaScript deshabilita botón al hacer clic"):
        assert "btn.disabled = true" in body
    with allure.step("JavaScript activa spinner overlay"):
        assert "spinner.classList.add" in body
    with allure.step("JavaScript llama POST /simulator/run"):
        assert "/simulator/run" in body
    with allure.step("Spinner tiene texto 'Simulando el Mundial 2026'"):
        assert "Simulando el Mundial 2026" in body
    allure.attach(body, "Full HTML", allure.attachment_type.HTML)


@allure.feature("Smoke Test Frontend")
@allure.story("Simulación")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SMK-03: Simulación y Campeón se muestran correctamente")
@allure.label("smoke", "simulación")
@allure.tag("frontend", "smoke", "campeon")
def test_smk_03_simulation_and_champion():
    req = urllib.request.Request(f"{BASE}/simulator/run", data=b"", method="POST")
    r = urllib.request.urlopen(req, timeout=30)
    data = json.loads(r.read().decode())
    with allure.step("POST /simulator/run → 200"):
        assert r.status == 200
    with allure.step("champion presente en respuesta"):
        assert "champion" in data
    with allure.step("final presente en respuesta"):
        assert "final" in data
    with allure.step("groups presente (8 grupos)"):
        assert len(data.get("groups", [])) == 8
    with allure.step("round_of_16 presente (8 octavos)"):
        assert len(data.get("round_of_16", [])) == 8
    with allure.step("champion coincide con final.winner"):
        assert data["champion"] == data["final"]["winner"]
    alluredata = json.dumps(data, indent=2)
    allure.attach(alluredata, "Respuesta simulación", allure.attachment_type.JSON)


@allure.feature("Smoke Test Frontend")
@allure.story("Dashboard")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SMK-04: Dashboard Ejecutivo muestra datos consistentes")
@allure.label("smoke", "dashboard")
@allure.tag("frontend", "smoke", "dashboard")
def test_smk_04_dashboard():
    r = urllib.request.urlopen(f"{BASE}/metrics/dashboard", timeout=10)
    data = json.loads(r.read().decode())
    with allure.step("GET /metrics/dashboard → 200"):
        assert r.status == 200
    with allure.step("champion presente"):
        assert "champion" in data
    with allure.step("top_scorer con goals > 0"):
        assert data["top_scorer"]["goals"] > 0
    with allure.step("avg_goals_per_match > 0"):
        assert data["avg_goals_per_match"] > 0
    with allure.step("total_goals > 0"):
        assert data["total_goals"] > 0
    with allure.step("total_matches == 64"):
        assert data["total_matches"] == 64
    with allure.step("Fórmula avg_goals correcta"):
        expected = round(data["total_goals"] / data["total_matches"], 2)
        assert data["avg_goals_per_match"] == expected
    alluredata = json.dumps(data, indent=2)
    allure.attach(alluredata, "Dashboard data", allure.attachment_type.JSON)


@allure.feature("Smoke Test Frontend")
@allure.story("Datos")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SMK-05: Equipos agrupados en 8 grupos × 4 equipos")
@allure.label("smoke", "equipos")
@allure.tag("frontend", "smoke", "grupos")
def test_smk_05_teams_grouped():
    r = urllib.request.urlopen(f"{BASE}/teams/", timeout=10)
    teams = json.loads(r.read().decode())
    with allure.step("GET /teams/ → 200"):
        assert r.status == 200
    with allure.step("32 equipos"):
        assert len(teams) == 32
    groups = {}
    for team in teams:
        g = team.get("group_name")
        if g:
            groups.setdefault(g, []).append(team)
    with allure.step("8 grupos (A-H)"):
        assert len(groups) == 8
    for g in "ABCDEFGH":
        with allure.step(f"Grupo {g} = 4 equipos"):
            assert len(groups.get(g, [])) == 4
    alluredata = json.dumps(teams, indent=2)
    allure.attach(alluredata, "Teams data", allure.attachment_type.JSON)


@allure.feature("Smoke Test Frontend")
@allure.story("Responsive")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SMK-06: CSS responsive para mobile 375px")
@allure.label("smoke", "responsive")
@allure.tag("frontend", "smoke", "mobile")
def test_smk_06_responsive_mobile():
    r = urllib.request.urlopen(f"{BASE}/", timeout=10)
    body = r.read().decode()
    with allure.step("Viewport meta presente"):
        assert '<meta name="viewport"' in body
    with allure.step("Media query @media (max-width: 768px) presente"):
        assert "@media (max-width: 768px)" in body
    with allure.step("hero h1 font-size 1.6rem en mobile"):
        assert "font-size: 1.6rem" in body
    with allure.step("brand-sub oculto en mobile (display:none)"):
        assert "display: none" in body and "brand-sub" in body
    with allure.step("Botón 100% ancho en mobile"):
        assert "width: 100%" in body
    with allure.step("[MANUAL] Dashboard en 2 columnas sin scroll horizontal"):
        allure.dynamic.parameter("manual_check", "Abrir DevTools > toggle device toolbar > 375x667")
    allure.attach(body, "Full HTML", allure.attachment_type.HTML)
