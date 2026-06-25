import allure
from fastapi.testclient import TestClient


# =============================================================================
# HAPPY PATH — CRUD EQUIPOS
# =============================================================================

@allure.feature("POST /teams/")
@allure.story("Happy path")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("contract", "creación equipo")
@allure.title("Crear equipo correctamente")
def test_create_team(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": "ARG"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Argentina"
    assert data["code"] == "ARG"


@allure.feature("POST /teams/")
@allure.story("Duplicados")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("contract", "códigos únicos")
@allure.title("Código duplicado exacto → 409")
@allure.issue("QA.md", "Regla: código debe ser único")
def test_create_team_duplicate_code(client: TestClient):
    client.post("/teams/", json={"name": "Argentina", "code": "ARG"})
    res = client.post("/teams/", json={"name": "Brasil", "code": "ARG"})
    assert res.status_code == 409


@allure.feature("GET /teams/")
@allure.story("Happy path")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Listar todos los equipos")
def test_list_teams(client: TestClient):
    client.post("/teams/", json={"name": "Argentina", "code": "ARG"})
    client.post("/teams/", json={"name": "Brasil", "code": "BRA"})
    res = client.get("/teams/")
    assert res.status_code == 200
    assert len(res.json()) == 2


@allure.feature("GET /teams/{id}")
@allure.story("Happy path")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Obtener equipo por ID")
def test_get_team(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": "ARG"})
    team_id = res.json()["id"]
    res = client.get(f"/teams/{team_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Argentina"


@allure.feature("GET /teams/{id}")
@allure.story("Edge cases")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Equipo inexistente → 404")
def test_get_team_not_found(client: TestClient):
    res = client.get("/teams/999")
    assert res.status_code == 404


@allure.feature("PUT /teams/{id}")
@allure.story("Happy path")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Actualizar equipo correctamente")
def test_update_team(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": "ARG"})
    team_id = res.json()["id"]
    res = client.put(f"/teams/{team_id}", json={"name": "Argentina Actualizado"})
    assert res.status_code == 200
    assert res.json()["name"] == "Argentina Actualizado"


@allure.feature("DELETE /teams/{id}")
@allure.story("Happy path")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Eliminar equipo correctamente")
def test_delete_team(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": "ARG"})
    team_id = res.json()["id"]
    res = client.delete(f"/teams/{team_id}")
    assert res.status_code == 204
    res = client.get(f"/teams/{team_id}")
    assert res.status_code == 404


# =============================================================================
# VALIDACION DE CONTRATO — POST /teams/
# =============================================================================

@allure.feature("POST /teams/")
@allure.story("Happy path")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("contract", "normalización mayúsculas")
@allure.title("Código en minúsculas se normaliza a mayúsculas")
def test_create_team_code_uppercase_normalization(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": "arg"})
    assert res.status_code == 201
    assert res.json()["code"] == "ARG"


@allure.feature("POST /teams/")
@allure.story("Validación 422")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("bug", "BUG-01")
@allure.title("Código de 2 caracteres → 422")
@allure.issue("BUG-01", "Backend no valida longitud de código")
def test_create_team_code_too_short(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": "AR"})
    assert res.status_code == 422


@allure.feature("POST /teams/")
@allure.story("Validación 422")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("bug", "BUG-02")
@allure.title("Código de 4 caracteres → 422")
@allure.issue("BUG-02", "Backend no valida longitud de código")
def test_create_team_code_too_long(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": "ARGN"})
    assert res.status_code == 422


@allure.feature("POST /teams/")
@allure.story("Validación 422")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("bug", "BUG-03")
@allure.title("Código vacío → 422")
@allure.issue("BUG-03", "Backend no valida código vacío")
def test_create_team_code_empty(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": ""})
    assert res.status_code == 422


@allure.feature("POST /teams/")
@allure.story("Validación 422")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("bug", "BUG-04")
@allure.title("Nombre vacío → 422")
@allure.issue("BUG-04", "Backend no valida nombre vacío")
def test_create_team_name_empty(client: TestClient):
    res = client.post("/teams/", json={"name": "", "code": "ARG"})
    assert res.status_code == 422


@allure.feature("POST /teams/")
@allure.story("Validación 422")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Name ausente del body → 422")
def test_create_team_missing_name(client: TestClient):
    res = client.post("/teams/", json={"code": "ARG"})
    assert res.status_code == 422


@allure.feature("POST /teams/")
@allure.story("Validación 422")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Code ausente del body → 422")
def test_create_team_missing_code(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina"})
    assert res.status_code == 422


@allure.feature("POST /teams/")
@allure.story("Validación 422")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Code con tipo numérico → 422")
def test_create_team_code_wrong_type(client: TestClient):
    res = client.post("/teams/", json={"name": "Argentina", "code": 123})
    assert res.status_code == 422


@allure.feature("POST /teams/")
@allure.story("Duplicados")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("contract", "códigos únicos case-insensitive")
@allure.title("Código duplicado case-insensitive → 409")
def test_create_team_duplicate_code_case_insensitive(client: TestClient):
    client.post("/teams/", json={"name": "Argentina", "code": "arg"})
    res = client.post("/teams/", json={"name": "Brasil", "code": "ARG"})
    assert res.status_code == 409