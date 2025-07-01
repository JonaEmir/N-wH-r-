#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# URL de tu API para crear productos
API_URL = 'http://127.0.0.1:8000/api/productos/crear/'

# Mapeo de categorías
categoria_map = {
    "Caballero": 1,
    "Dama": 2,
    "Niños": 3,
}

# Lista completa de productos
productos = [
    {
        "nombre": "Air Jordan 1 x Off-White “UNC”",
        "descripcion": "Diseño icónico. Detalles deconstruidos. Inspirado en los colores UNC.\nEstilo urbano en su máxima expresión.",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 1,
        "variantes": [
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "29"}}
        ]
    },
    {
        "nombre": "Jordan 1 Retro High Off-White \"Chicago\"",
        "descripcion": "Clásico atemporal. El legado de Jordan con la visión de Off-White.\nColorway original, detalles expuestos, esencia streetwear.",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 4,
        "variantes": [
            {"precio": 1299.0, "precio_mayorista": 700.0, "stock": 3, "atributos": {"Talla": "26"}},
            {"precio": 1299.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "27"}}
        ]
    },
    {
        "nombre": "Air Jordan 1 \"Chicago\"",
        "descripcion": "Colorway original. Historia pura del basketball.\nRojo, blanco y negro en su forma más icónica.\nCintas Blancas.",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 3,
        "variantes": [
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 2, "atributos": {"Talla": "26"}},
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "28"}}
        ]
    },
    {
        "nombre": "Air Jordan 1 High \"Chicago\"",
        "descripcion": "Colorway original. Historia pura del basketball.\nRojo, blanco y negro en su forma más icónica.\nCintas negras.",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 7,
        "variantes": [
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 2, "atributos": {"Talla": "25"}},
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 4, "atributos": {"Talla": "26"}},
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "29"}}
        ]
    },
    {
        "nombre": "Jordan Retro 4",
        "descripcion": "Estilo limpio y potente.\nCombinación de blanco y azul en un diseño clásico con aire urbano.",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 2,
        "variantes": [
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "26"}},
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "29"}}
        ]
    },
    {
        "nombre": "Jordan 1 Retro High OG SP Travis Scott",
        "descripcion": "Estilo disruptivo.\nSwoosh invertido, tonos fríos y sello Cactus Jack.",
        "categoria": "Caballero",
        "genero": "H",
        "en_oferta": False,
        "stock_total": 6,
        "variantes": [
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 2, "atributos": {"Talla": "26"}},
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 2, "atributos": {"Talla": "29"}},
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "28"}},
            {"precio": 1199.0, "precio_mayorista": 700.0, "stock": 1, "atributos": {"Talla": "25"}}
        ]
    },
    {
        "nombre": "Dolce & Gabbana New Roma",
        "descripcion": "Lujo urbano en cada paso.\nDiseño limpio, silueta moderna y sello italiano.",
        "categoria": "Caballero",
        "genero": "U",
        "en_oferta": False,
        "stock_total": 9,
        "variantes": [
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 2, "atributos": {"Talla": "29"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 1, "atributos": {"Talla": "28"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 2, "atributos": {"Talla": "26"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 2, "atributos": {"Talla": "25"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 1, "atributos": {"Talla": "24"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 1, "atributos": {"Talla": "23"}}
        ]
    },
    {
        "nombre": "CHRISTIAN DIOR blue & white TOILE DE JOUY WALK'IN",
        "descripcion": "Estilo parisino con sello artístico.\nEstampado icónico y silueta casual de alta gama.",
        "categoria": "Dama",
        "genero": "M",
        "en_oferta": False,
        "stock_total": 7,
        "variantes": [
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 4, "atributos": {"Talla": "37"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 2, "atributos": {"Talla": "39"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 1, "atributos": {"Talla": "36"}}
        ]
    },
    {
        "nombre": "Dior B23 Oblicuo",
        "descripcion": "Diseño emblemático y moderno.\nEl monograma Dior se une a una silueta urbana de lujo.",
        "categoria": "Dama",
        "genero": "M",
        "en_oferta": False,
        "stock_total": 11,
        "variantes": [
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 4, "atributos": {"Talla": "36"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 4, "atributos": {"Talla": "37"}},
            {"precio": 2599.0, "precio_mayorista": 1499.0, "stock": 3, "atributos": {"Talla": "38"}}
        ]
    }
]

def crear_producto(p):
    data = {
        'nombre': p['nombre'],
        'descripcion': p['descripcion'],
        'precio': str(p['variantes'][0]['precio']),
        'precio_mayorista': str(p['variantes'][0]['precio_mayorista']),
        'categoria_id': str(categoria_map.get(p['categoria'], '')),
        'genero': p['genero'],
    }

    if p.get('en_oferta'):
        data['en_oferta'] = 'on'

    tallas = [v['atributos']['Talla'] for v in p['variantes']]
    stocks = [str(v['stock']) for v in p['variantes']]
    if tallas:
        data['tallas'] = tallas
        data['stocks'] = stocks

    response = requests.post(API_URL, data=data)
    if response.status_code in (200, 201):
        print(f"[OK]    {p['nombre']}")
    else:
        print(f"[ERROR] {p['nombre']} → {response.status_code}: {response.text}")

if __name__ == '__main__':
    for producto in productos:
        crear_producto(producto)
