#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os

# URL de tu API para crear productos
API_URL = 'http://127.0.0.1:8000/api/productos/crear/'

# Lista completa de tus 6 productos (igual que antes)
productos = [
    {
        "id": 1,
        "nombre": "New Balance",
        "descripcion": "New balance ",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": True,
        "stock_total": 10,
        "variantes": [
            {"id": 1,  "precio_mayorista":1200,"precio": 2900.0, "stock": 5,  "atributos": {"Talla": "26"}},
            {"id": 2,  "precio_mayorista":1200,"precio": 2900.0, "stock": 5,  "atributos": {"Talla": "28"}}
        ]
    },
    {
        "id": 2,
        "nombre": "AirMax97",
        "descripcion": "Air max 97 vintage",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 40,
        "variantes": [
            {"id": 3,  "precio_mayorista":1200,"precio": 3600.0, "stock": 10, "atributos": {"Talla": "26"}},
            {"id": 4,  "precio_mayorista":1200,"precio": 3600.0, "stock": 30, "atributos": {"Talla": "27"}}
        ]
    },
    {
        "id": 3,
        "nombre": "tenis2",
        "descripcion": "yeey",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": True,
        "stock_total": 32,
        "variantes": [
            {"id": 5,  "precio_mayorista":1200,"precio": 2200.0, "stock": 5,  "atributos": {"Talla": "26"}},
            {"id": 6,  "precio_mayorista":1200,"precio": 2200.0, "stock": 7,  "atributos": {"Talla": "27"}},
            {"id": 7,  "precio_mayorista":1200,"precio": 2200.0, "stock": 20, "atributos": {"Talla": "28"}}
        ]
    },
    {
        "id": 4,
        "nombre": "Jordan 4 retro high",
        "descripcion": "ndjsndksk,",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 2,
        "variantes": [
            {"id": 8,  "precio_mayorista":1200,"precio": 3000.0, "stock": 1, "atributos": {"Talla": "26"}},
            {"id": 9,  "precio_mayorista":1200,"precio": 3000.0, "stock": 1, "atributos": {"Talla": "29"}}
        ]
    },
    {
        "id": 5,
        "nombre": "Air Jordan 1 1985",
        "descripcion": "Air Jordan 1985 cintas blancas",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 3,
        "variantes": [
            {"id": 10, "precio_mayorista":1200,"precio": 1400.0, "stock": 2, "atributos": {"Talla": "26"}},
            {"id": 11, "precio_mayorista":1200,"precio": 1400.0, "stock": 1, "atributos": {"Talla": "28"}}
        ]
    },
    {
        "id": 6,
        "nombre": "jordan 1 off-white chicago",
        "descripcion": "jordan 1 off-white chicago",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": True,
        "stock_total": 4,
        "variantes": [
            {"id": 12, "precio_mayorista":1200,"precio": 2000.0, "stock": 3, "atributos": {"Talla": "26"}},
            {"id": 13, "precio_mayorista":1200,"precio": 2000.0, "stock": 1, "atributos": {"Talla": "27"}}
        ]
    }
]

# Mapea nombre de categoría a su ID en tu sistema.
categoria_map = {
    "Caballero": 1,
    "Dama":      2,
    "Niños":     3,
}

def crear_producto(p):
    # Toma precio y stock total
    precio = p['variantes'][0]['precio'] if p.get('variantes') else 0
    precio_mayorista =  p['variantes'][0]['precio_mayorista'] if p.get('variantes') else 0
    
    # Lo que lee tu vista en request.POST
    data = {
        'nombre':       p['nombre'],
        'descripcion':  p['descripcion'],
        'precio':       str(precio),
        'precio_mayorista': str(precio_mayorista),
        'categoria_id': str(categoria_map.get(p['categoria'], '')),
        'genero':       p['genero'],
    }
    if p.get('en_oferta'):
        data['en_oferta'] = 'on'

    # Listas de tallas y stocks
    tallas = [v['atributos']['Talla'] for v in p['variantes']]
    stocks = [str(v['stock']) for v in p['variantes']]
    if tallas:
        data['tallas'] = tallas
        data['stocks'] = stocks

    # **** SIN files => no imagen enviada ****
    resp = requests.post(API_URL, data=data)

    if resp.status_code in (200, 201):
        print(f"[OK]    {p['nombre']}")
    else:
        print(f"[ERROR] {p['nombre']} → {resp.status_code}: {resp.text}")

if __name__ == '__main__':
    for prod in productos:
        crear_producto(prod)
