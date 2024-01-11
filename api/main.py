
from fastapi import FastAPI, HTTPException, Request, Depends
from api import models, crud, database
from typing import  List
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()
empresa_1 = models.Empresa(nombre="Empresa A")
empresa_2 = models.Empresa(nombre="Empresa B")

db.add(empresa_1)
db.add(empresa_2)

db.commit()
# modelos Pydantic
templates = Jinja2Templates(directory="api/templates")




                                      
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(database.get_db)):
    users = crud.obtener_usuarios(db)
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.get("/usuarios/ver/{usuario_id}", response_model=models.UsuarioBase)
def leer_usuario(usuario_id: int):
    db = database.SessionLocal()
    return crud.leer_usuario(db, usuario_id)

@app.post("/usuarios/create")
def crear_usuario(usuario: models.UsuarioBase):
    try:
        db = database.SessionLocal()
        usuario_db = models.Usuario(**usuario.dict())
        return crud.crear_usuario(db, usuario_db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@app.put("/usuarios/update/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: models.UsuarioBase):
    db = database.SessionLocal()
    db_usuario = crud.leer_usuario(db, usuario_id)

    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_data = usuario.dict(exclude_unset=True)
    for key, value in usuario_data.items():
        setattr(db_usuario, key, value)

    db.commit()
  

    return db_usuario

@app.delete("/usuarios/delete/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    db = database.SessionLocal()
    return crud.eliminar_usuario(db, usuario_id)

@app.get("/empresas/{empresa_id}/usuarios", response_model=List[models.UsuarioBase])
def obtener_usuarios_por_empresa(empresa_id: int):
    db = database.SessionLocal()
    return crud.obtener_usuarios_por_empresa(db, empresa_id)


