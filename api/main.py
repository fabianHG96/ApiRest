
from fastapi import FastAPI, HTTPException, Request, Depends, Form, Query
from api import models, crud, database
from typing import  List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session



app = FastAPI()



templates = Jinja2Templates(directory="api/templates")




                                      
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(database.get_db)):
    users = crud.obtener_usuarios(db)
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.get("/usuarios/{usuario_id}/ver", response_class=HTMLResponse)
def ver_usuario(request: Request, usuario_id: int, db: Session = Depends(database.get_db)):
    usuario_con_empresa = crud.obtener_usuario_con_empresa(db, usuario_id)

    if usuario_con_empresa is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario, empresa = usuario_con_empresa

    return templates.TemplateResponse("details.html", {"request": request, "usuario": usuario, "empresa": empresa})

@app.get("/usuarios/create", response_class=HTMLResponse)
def create_user_view(request: Request):
    return templates.TemplateResponse("create_users.html", {"request": request})

@app.post("/usuarios/create")
def crear_usuario(nombre: str = Form(...), email: str = Form(...), id_fk_empresa: int = Form(...)):
    try:
        db = database.SessionLocal()
        usuario = models.Usuario(nombre=nombre, email=email, id_fk_empresa=id_fk_empresa)
        crud.crear_usuario(db, usuario)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@app.get("/usuarios/{usuario_id}/update", response_class=HTMLResponse)
def ver_actualizar_usuario(request: Request, usuario_id: int):
    db = database.SessionLocal()
    db_usuario = crud.leer_usuario(db, usuario_id)

    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return templates.TemplateResponse("update.html", {"request": request, "usuario": db_usuario})

@app.post("/usuarios/{usuario_id}/update")
def actualizar_usuario(usuario_id: int, nombre: str = Form(...), email: str = Form(...), id_fk_empresa: int = Form(...)):
    db = database.SessionLocal()
    db_usuario = crud.leer_usuario(db, usuario_id)

    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_usuario.nombre = nombre
    db_usuario.email = email
    db_usuario.id_fk_empresa = id_fk_empresa
    db.commit()
    db_usuario
    return RedirectResponse(url="/", status_code=303)

@app.delete("/usuarios/{usuario_id}/eliminar")
def eliminar_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    usuario_eliminado = crud.eliminar_usuario(db, usuario_id)
    if usuario_eliminado:
        return {"status": "Usuario eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    


@app.get('/empresas/usuarios')
async def obtener_usuarios_por_empresa(request: Request, db: Session = Depends(database.get_db)):
    empresas = crud.obtener_empresas(db)
    usuario = {"id_fk_empresa": None} 
    return templates.TemplateResponse("usuarios_empresa.html", {"request": request, "empresas": empresas, "usuario": usuario})


@app.get("/empresas/{empresa_id}/usuarios", response_model=List[models.UsuarioBase])
def obtener_usuarios_por_empresa(empresa_id: int):
    db = database.SessionLocal()
    return crud.obtener_usuarios_por_empresa(db, empresa_id)